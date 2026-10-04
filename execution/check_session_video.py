"""Video API and browser checks against an isolated database; never record a user's screen."""
import os
import subprocess
import unittest
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from check_heatmap_api import HeatmapApiTests

class VideoTests(HeatmapApiTests):
    def binary(self,path,body=None,headers=None):
        try:
            with urlopen(Request(self.url+path,data=body,headers={'Origin':'http://127.0.0.1:5173',**(headers or {})}),timeout=10) as response:return response.status,response.headers,response.read()
        except HTTPError as e:return e.code,e.headers,e.read()

    def test_chunks_ranges_and_retries(self):
        start={'id':'video-1','study':'leed-local','session':'video-session','startedAt':1000,'mime':'video/webm'}
        self.assertEqual(self.request('/api/recordings/start',start)[0],200)
        data=b'\x1aE\xdf\xa3\x80\x18\x53\x80\x67\xff\x15\x49\xa9\x66\x87\x2a\xd7\xb1\x83\x0f\x42\x40'
        self.assertEqual(self.binary('/api/recordings/chunk?id=video-1&seq=0',data)[0],200)
        self.assertEqual(self.binary('/api/recordings/chunk?id=video-1&seq=0',data)[0],200)
        self.assertEqual(self.binary('/api/recordings/chunk?id=video-1&seq=0',data+b'x')[0],400)
        finish={'id':'video-1','chunks':2,'duration':2.5,'interrupted':False}
        self.assertEqual(self.request('/api/recordings/finish',finish)[0],400)
        finish['chunks']=1
        self.assertEqual(self.request('/api/recordings/finish',finish)[0],200)
        self.assertEqual(self.request('/api/recordings/finish',finish)[0],200)
        self.assertEqual(self.binary('/api/recordings/chunk?id=video-1&seq=0',data)[0],200)
        self.assertEqual(self.request('/api/recordings?session=video-session')[1][0]['status'],'ready')
        status,headers,body=self.binary('/api/recordings/media?id=video-1',headers={'Range':'bytes=0-3'})
        self.assertEqual(status,206);self.assertEqual(body,b'\x1aE\xdf\xa3');self.assertIn('Content-Range',headers)
        self.assertEqual(self.binary('/api/recordings/media?id=video-1',headers={'Range':'bytes=99999-'})[0],416)
        self.assertEqual(self.request('/api/project')[1]['sessions'][0]['recordings'],1)
        self.assertEqual(self.binary('/api/recordings/media?id=video-1',headers={'Origin':'https://example.com'})[0],403)

    def test_browser_capture_upload_and_playback(self):
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_session_video.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=160)

if __name__=='__main__':unittest.main(defaultTest='VideoTests')
