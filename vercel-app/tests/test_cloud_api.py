"""Exercise the actual HTTP handler, clean persistence, atomic retries and bounded media."""
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'execution'))
spec = importlib.util.spec_from_file_location('cloud_api', ROOT / 'api/index.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class CloudApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.database = str(Path(cls.folder.name) / 'cloud.sqlite3')
        os.environ['UXLAB_TEST_DB'] = cls.database
        os.environ['UXLAB_ACCESS_PASSWORD'] = 'test-password-cloud-123'
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), api.handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.cookie = ''
        status, headers, _ = cls.request('POST', '/api/auth', {'password': 'test-password-cloud-123'})
        assert status == 200
        cls.cookie = headers['Set-Cookie'].split(';')[0]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.folder.cleanup()

    @classmethod
    def request(cls, method, path, data=None, extra=None, authenticated=True):
        connection = HTTPConnection('127.0.0.1', cls.port, timeout=15)
        headers = {'Origin': f'http://127.0.0.1:{cls.port}'}
        if authenticated and cls.cookie:
            headers['Cookie'] = cls.cookie
        if data is not None and not isinstance(data, bytes):
            data = json.dumps(data).encode()
            headers['Content-Type'] = 'application/json'
        headers.update(extra or {})
        connection.request(method, path, data, headers)
        response = connection.getresponse()
        body, status, result_headers = response.read(), response.status, dict(response.getheaders())
        connection.close()
        return status, result_headers, body

    def data(self, method, path, body=None, status=200):
        code, _, payload = self.request(method, path, body)
        self.assertEqual(code, status, payload[:300])
        return json.loads(payload)

    def test_auth_and_rewrite(self):
        self.assertEqual(self.request('GET', '/api/project', authenticated=False)[0], 401)
        self.assertEqual(self.request('GET', '/api/project', extra={'Origin': 'https://untrusted.example'})[0], 403)
        self.assertEqual(self.request('POST', '/api/auth', {'password': 'wrong'})[0], 401)
        config = self.data('GET', '/api/index.py?__path=/api/project/config&study=leed-local')
        self.assertTrue(config['url'].startswith(f'http://127.0.0.1:{self.port}/participant/'))
        self.assertNotIn(':5175', config['url'])
        self.assertEqual(self.request('GET', '/api/index.py?__path=/sdk.js')[0], 200)

    def test_clicks_retry_conflict_and_reconnect(self):
        event = dict(id='cloud-event-1',study='leed-local',session='cloud-session-1',seq=1,
                     page='leed-leads-table',version='leed-local-v2',target='test-button',x=.3,y=.4,
                     vw=1280,vh=720,rw=1280,rh=720,scroll_x=0,scroll_y=0,timestamp=1000,
                     context={'signature':'1234567890abcdef','scrolls':[]})
        self.data('POST', '/api/heatmap/events', {'events':[event]})
        self.data('POST', '/api/heatmap/events', {'events':[event]})
        self.data('POST', '/api/heatmap/events', {'events':[{**event,'x':.9}]}, status=400)
        result = self.data('GET', '/api/heatmap?study=leed-local&aggregation=page')
        self.assertEqual(result['total']['clicks'], 1)
        api._migrated = False  # Simulate a cold function initialization, preserve the same database.
        self.assertEqual(self.data('GET', '/api/heatmap?study=leed-local')['total']['clicks'], 1)
        with api.cloud_db.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM clicks').fetchone()[0], 1)
        with self.assertRaises(ValueError):
            with api.cloud_db.connect() as db:
                db.execute("INSERT INTO cloud_schema VALUES (99)")
                raise ValueError('rollback')
        with api.cloud_db.connect() as db:
            self.assertIsNone(db.execute('SELECT version FROM cloud_schema WHERE version=99').fetchone())

    def test_new_study_and_snapshot(self):
        study = self.data('POST', '/api/project/studies', {'studyTitle':'Облачное исследование'})
        self.assertFalse(study['enabled'])
        self.assertIn('/participant/', study['url'])
        self.assertEqual(self.data('GET', '/api/project?study='+study['studyId'])['total']['clicks'], 0)
        snapshot = {'id':'cloud-snapshot','html':'<!doctype html><html><body>Тест</body></html>','width':1280,'height':720}
        self.data('POST', '/api/heatmap/snapshots', snapshot)
        self.assertEqual(self.data('GET', '/api/heatmap/snapshots?id=cloud-snapshot')['html'], snapshot['html'])

    def test_pdf_report(self):
        report = self.data('POST', '/api/project/reports', {'title': 'Облачный отчёт'})
        status, headers, pdf = self.request('GET', '/api/project/report-pdf?id=' + report['id'])
        self.assertEqual(status, 200, pdf[:250])
        self.assertEqual(headers['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.startswith(b'%PDF-'))
        self.assertGreater(len(pdf), 10000)

    @unittest.skipUnless(importlib.util.find_spec('libsql'), 'libsql wheels are exercised by Linux CI')
    def test_libsql_dbapi_compatibility(self):
        import libsql
        raw = libsql.connect(database=':memory:', isolation_level=None)
        try:
            db = api.cloud_db.Connection(raw)
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE sdk_check (id INTEGER, label TEXT, data BLOB)')
            db.execute('INSERT INTO sdk_check VALUES (?,?,?)', (7, 'Кириллица', b'\x00\xff'))
            raw.commit()
            row = db.execute('SELECT * FROM sdk_check').fetchone()
            self.assertEqual(dict(row), {'id':7,'label':'Кириллица','data':b'\x00\xff'})
            self.assertEqual(row[1], 'Кириллица')
        finally:
            raw.close()

    def test_video_chunks_ranges_and_download(self):
        self.data('GET', '/api/project/config')
        record = dict(id='cloud-video',study='leed-local',session='cloud-session-1',startedAt=1000,mime='video/webm')
        self.data('POST', '/api/recordings/start', record)
        # A minimal streaming EBML header plus padding, enough to test our byte transport.
        prefix = b'\x1aE\xdf\xa3\x80\x18\x53\x80\x67\xff\x15\x49\xa9\x66\x87\x2a\xd7\xb1\x83\x0f\x42\x40'
        source = prefix + b'\0' * (api.cloud_video.MAX_RESPONSE + 12345)
        parts = [source[i:i+api.cloud_video.MAX_CHUNK] for i in range(0, len(source), api.cloud_video.MAX_CHUNK)]
        for seq, part in enumerate(parts):
            self.data('POST', f'/api/recordings/chunk?id=cloud-video&seq={seq}', part)
        self.data('POST', '/api/recordings/chunk?id=cloud-video&seq=0', parts[0])
        self.data('POST', '/api/recordings/chunk?id=cloud-video&seq=0', b'conflicting', status=400)
        finished = dict(id='cloud-video',chunks=len(parts),duration=5.0,interrupted=False)
        self.data('POST', '/api/recordings/finish', finished)
        self.data('POST', '/api/recordings/finish', finished)
        self.data('POST', '/api/recordings/chunk?id=cloud-video&seq=0', parts[0])
        assembled = b''
        while True:
            status, headers, body = self.request('GET', '/api/recordings/media?id=cloud-video', extra={'Range':f'bytes={len(assembled)}-'})
            self.assertEqual(status, 206)
            self.assertLessEqual(len(body), api.cloud_video.MAX_RESPONSE)
            assembled += body
            if len(assembled) == int(headers['Content-Range'].split('/')[1]):
                break
        expected = api.session_video.webm_duration(source, 5.0)
        self.assertEqual(assembled, expected)
        self.assertEqual(self.request('GET','/api/recordings/media?id=cloud-video',extra={'Range':'bytes=99999999-'})[0],416)
        self.assertEqual(self.request('GET','/api/recordings/media?id=cloud-video&study=missing')[0],400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
