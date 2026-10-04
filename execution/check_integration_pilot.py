"""Contract and browser checks on isolated SQLite + an independent HTML origin."""
import json
import os
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from serve_integration_pilot import initialize,make_handler
from serve_integration_demo import demo_html,make_handler as demo_handler

ROOT=Path(__file__).resolve().parents[1]


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.db=Path(self.temp.name)/'pilot.sqlite3';initialize(self.db)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(self.db))
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.api=f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()

    def request(self,path,body=None,origin='http://127.0.0.1:5173'):
        req=Request(self.api+path,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':origin})
        try:
            with urlopen(req,timeout=5) as response:return response.status,json.load(response)
        except HTTPError as error:return error.code,json.load(error)

    def create(self,**kwargs):
        status,row=self.request('/api/connections',{'name':'Test website','kind':'web','url':'http://127.0.0.1:5199/',**kwargs})
        self.assertEqual(status,200,row);return row

    def test_origin_isolation_validation_and_retry(self):
        row=self.create();other=self.create();endpoint='/api/events?project='+row['id']+'&study='+row['study']
        event=dict(id='event-1',study=row['study'],session='tab-1',seq=1,version='web-sdk-v1',timestamp=1,page='demo',kind='visit',vw=1280,vh=900)
        self.assertEqual(self.request(endpoint,{'events':[event]},'https://unregistered.example')[0],403)
        self.assertEqual(self.request('/api/connections',origin='http://127.0.0.1:5199')[0],403)
        for _ in range(2):self.assertEqual(self.request(endpoint,{'events':[event]},'http://127.0.0.1:5199')[0],200)
        self.assertEqual(self.request(endpoint,{'events':[{**event,'page':'changed'}]},'http://127.0.0.1:5199')[0],400)
        self.assertEqual(self.request(endpoint,{'events':[{**event,'id':'bad','seq':2,'email':'secret'}]},'http://127.0.0.1:5199')[0],400)
        self.assertEqual(self.request(endpoint,{'events':[{**event,'id':'other','seq':3,'study':other['study']}]},'http://127.0.0.1:5199')[0],400)
        self.assertEqual(self.request('/api/results?project='+row['id'])[1]['total']['events'],1)
        self.assertEqual(self.request('/api/results?project='+other['id'])[1]['total']['events'],0)
        self.request('/api/policy',{'project':row['id'],'enabled':False})
        self.assertEqual(self.request(endpoint,{'events':[{**event,'id':'paused','seq':4}]},'http://127.0.0.1:5199')[0],400)

    def test_figma_schema_and_url(self):
        for url in ('https://example.com/proto/file','https://www.figma.com/design/file','javascript:alert(1)'):
            self.assertEqual(self.request('/api/connections',{'name':'Figma','kind':'figma','url':url})[0],400)
        row=self.create(kind='figma',url='https://www.figma.com/proto/Example/Test?node-id=1-2',clientId='test-client')
        endpoint='/api/events?project='+row['id']+'&study='+row['study']
        event=dict(id='figma-1',study=row['study'],session='session-1',seq=1,version='figma-embed-v1',timestamp=1,page='1:2',kind='PRESENTED_NODE_CHANGED',data={'node':'1:2','history':True})
        self.assertEqual(self.request(endpoint,{'events':[event]})[0],200)
        self.assertEqual(self.request(endpoint,{'events':[{**event,'id':'bad','seq':2,'data':{'node':'1:2','history':'true'}}]})[0],400)

    def test_browser(self):
        site=ThreadingHTTPServer(('127.0.0.1',0),demo_handler(''))
        origin=f'http://127.0.0.1:{site.server_port}'
        row=self.create(url=origin+'/')
        site.RequestHandlerClass=demo_handler(demo_html(self.api,row['id']))
        thread=threading.Thread(target=site.serve_forever,daemon=True);thread.start()
        try:
            env={**os.environ,'PILOT_TEST_API':self.api,'PILOT_TEST_SITE':origin,'PILOT_TEST_CONNECTION':json.dumps(row)}
            subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_integration_pilot.mjs'],cwd=ROOT,env=env,check=True,timeout=180)
        finally:site.shutdown();site.server_close();thread.join()


if __name__=='__main__':unittest.main()
