"""Snapshot replay checks, with all browser traffic routed to a temporary database."""
import os
import subprocess
import unittest
from pathlib import Path
from check_heatmap_api import HeatmapApiTests
from serve_heatmap import initialize


class SnapshotTests(HeatmapApiTests):
    def test_frames_validation_retry_and_session_summary(self):
        frame=dict(id='frame-1',study='leed-local',session='frames-only',seq=1,timestamp=1000,
                   page='leed-leads-table',snapshot='snapshot-1',vw=1280,vh=900,kind='click',label='Кнопка',target={'x':.3,'y':.2,'rect':[.2,.1,.1,.1]})
        self.assertEqual(self.request('/api/project/config',{'recordingMode':'wrong'})[0],400)
        self.assertEqual(self.request('/api/project/config',{'recordingMode':'screenshots'})[0],200)
        for _ in range(2):self.assertEqual(self.request('/api/project/frames',frame)[0],200)
        for changed in ({'target':{'x':2,'y':.5}},{'seq':False},{'study':'other'},{'kind':'private'},{'label':'x'*161},{'target':{'x':.5,'y':.5,'rect':[0,1]}}):
            self.assertEqual(self.request('/api/project/frames',{**frame,**changed})[0],400)
        self.assertEqual(self.request('/api/project/frames',{**frame,'id':'conflict'})[0],400)
        initialize(self.db)
        self.assertEqual(self.request('/api/project/config')[1]['recordingMode'],'screenshots')
        self.assertEqual(self.request('/api/project/frames?session=frames-only')[1]['frames'],[frame])
        self.assertEqual(self.request('/api/project/frames?session=other')[1]['frames'],[])
        result=self.request('/api/project')[1]
        self.assertEqual(result['total']['sessions'],1)
        self.assertEqual(result['total']['clicks'],0)
        self.assertEqual(result['sessions'][0]['frames'],1)
        self.assertEqual(result['sessions'][0]['pages'],['leed-leads-table'])
        self.assertEqual(self.request('/api/project?device=mobile')[1]['sessions'],[])

    def test_browser_snapshots(self):
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_session_snapshots.mjs'],
                       cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=180)


if __name__=='__main__':unittest.main(defaultTest='SnapshotTests')
