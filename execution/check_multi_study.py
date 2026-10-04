"""Study migration and isolation checks. All writes use a temporary SQLite database."""
import json
import os
import subprocess
from pathlib import Path
from check_live_project import LiveProjectTests
from serve_heatmap import connect, initialize


class MultiStudyTests(LiveProjectTests):
    def create(self,title):
        code,data=self.request('/api/project/studies',{'studyTitle':title,'scenario':'Найдите лид и откройте фильтр.'})
        self.assertEqual(code,200)
        return data['studyId']

    def test_study_isolation(self):
        self.seed()
        a,b=self.create('First flow'),self.create('Second flow')
        self.assertNotEqual(a,b)
        self.assertFalse(self.request('/api/project/config?study='+a)[1]['enabled'])
        self.assertIn('ux_study='+a,self.request('/api/project/config?study='+a)[1]['url'])
        self.request('/api/project/config?study='+a,{'enabled':True,'collectClicks':False,'recordingMode':'screenshots','funnel':['leed-dashboard']})
        self.assertTrue(self.request('/api/project/config?study='+b)[1]['collectClicks'])
        for index,study in enumerate((a,b)):
            self.request('/api/project/visit',self.visit(id='v-'+study,study=study,session='shared-session'))
            self.request('/api/heatmap/events',{'events':[self.click(20+index,id='c-'+study,study=study,session='shared-session')]})
            self.request('/api/project/frames',dict(id='f-'+study,study=study,session='shared-session',seq=1,timestamp=3000,page='leed-dashboard',snapshot='sample',vw=1280,vh=900,kind='screen',label='Dashboard',target={}))
        self.assertEqual(len(self.request('/api/project/session?study='+a+'&id=shared-session')[1]['events']),2)
        self.assertEqual(len(self.request('/api/project/frames?study='+a+'&session=shared-session')[1]['frames']),1)
        self.assertEqual(self.request('/api/project?study='+a)[1]['total']['clicks'],1)
        self.assertEqual(self.request('/api/project')[1]['total']['clicks'],4)
        finding=self.request('/api/project/findings?study='+a,{'title':'Only A','observation':'Observation A'})[1]
        self.assertEqual(self.request('/api/project/findings?study='+b,{'id':finding['id'],'resolved':True})[0],400)
        self.assertEqual(self.request('/api/project?study='+b)[1]['findings'],[])
        report=self.request('/api/project/reports?study='+a,{})[1]
        self.assertEqual(report['project']['studyId'],a)
        self.assertEqual(self.request('/api/project?study='+b)[1]['reports'],[])
        self.assertEqual(self.request('/api/heatmap?study='+a)[1]['total']['clicks'],1)
        self.assertEqual(self.request('/api/project/config?study=missing')[0],400)
        self.assertEqual(self.request('/api/project/studies',{'studyTitle':'   '})[0],400)
        self.request('/api/project/config?study='+b,{'enabled':True})
        start=dict(id='record-b',study=b,session='shared-session',startedAt=1000,mime='video/webm')
        self.assertEqual(self.request('/api/recordings/start',start)[0],200)
        self.assertEqual(self.request('/api/recordings?study='+a+'&session=shared-session')[1],[])
        self.assertEqual(len(self.request('/api/recordings?study='+b+'&session=shared-session')[1]),1)
        initialize(self.db)
        self.assertEqual(len(self.request('/api/project/studies')[1]['studies']),3)
        self.assertEqual(self.request('/api/project?study='+a)[1]['total']['clicks'],1)

    def test_legacy_migration(self):
        self.seed()
        self.request('/api/project/findings',{'title':'Legacy note','observation':'Keep me'})
        self.request('/api/project/reports',{})
        with connect(self.db) as db:
            db.execute('DROP TABLE live_studies')
            config=json.loads(db.execute("SELECT value FROM live_settings WHERE id='project'").fetchone()[0])
            config.update(studyTitle='Existing research',enabled=False,recordingMode='screenshots')
            db.execute("UPDATE live_settings SET value=? WHERE id='project'",(json.dumps(config),))
        initialize(self.db);initialize(self.db)
        result=self.request('/api/project')[1]
        self.assertEqual(result['project']['studyTitle'],'Existing research')
        self.assertFalse(result['project']['enabled'])
        self.assertEqual(result['total']['clicks'],4)
        self.assertEqual(len(result['findings']),1)
        self.assertEqual(len(result['reports']),1)
        self.assertEqual(len(result['studies']),1)

    def test_multi_study_browser(self):
        self.seed()
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_multi_study.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=180)


if __name__=='__main__':
    import unittest
    unittest.main(defaultTest='MultiStudyTests')
