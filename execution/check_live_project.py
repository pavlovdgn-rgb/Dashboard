"""Isolated live-workspace checks, including browser flows against a temporary database."""
import os
import subprocess
from pathlib import Path
from check_heatmap_api import HeatmapApiTests


class LiveProjectTests(HeatmapApiTests):
    def click(self,seq=1,**changes):
        return {**self.event(seq),'study':'leed-local','page':'leed-leads-table',
                'context':{'signature':'1234567890abcdef','scrolls':[]},**changes}

    def visit(self,**changes):
        return {**dict(id='visit-1',study='leed-local',session='visit-only',page='leed-dashboard',
                    timestamp=2000,vw=1280,vh=900,context={'signature':'1234567890abcdef','scrolls':[]}),**changes}

    def seed(self):
        self.assertEqual(self.request('/api/heatmap/events',{'events':[
            self.click(1,timestamp=1000),self.click(2,timestamp=1200),self.click(3,timestamp=1400),
            self.click(4,page='leed-dashboard',timestamp=2000),
            self.click(5,study='leed-verify-hidden',session='hidden'),
        ]})[0],200)
        self.assertEqual(self.request('/api/project/visit',self.visit())[0],200)

    def test_project_isolation_visits_and_signals(self):
        self.seed()
        data=self.request('/api/project')[1]
        self.assertEqual(data['total']['clicks'],4)
        self.assertEqual(data['total']['sessions'],2)
        self.assertEqual(len(data['signals']),1)
        self.assertEqual(self.request('/api/project/session?id=hidden')[1]['events'],[])
        self.assertEqual(self.request('/api/project?device=mobile')[1]['total']['clicks'],0)
        self.assertEqual(self.request('/api/project?device=wrong')[0],400)
        self.assertEqual(self.request('/api/project/visit',self.visit())[0],200)
        self.assertEqual(self.request('/api/project')[1]['total']['visits'],1)
        for context in ({'signature':'x','scrolls':[]},{'signature':'1234567890abcdef','scrolls':[['private']]}):
            self.assertEqual(self.request('/api/project/visit',self.visit(context=context))[0],400)

    def test_ordered_funnel_findings_and_report_snapshot(self):
        self.seed()
        self.assertEqual(self.request('/api/project/config',{'funnel':['leed-leads-table','leed-dashboard']})[0],200)
        self.assertEqual([step['sessions'] for step in self.request('/api/project')[1]['funnel']],[1,1])
        self.request('/api/project/config',{'funnel':['leed-dashboard','leed-leads-table']})
        self.assertEqual([step['sessions'] for step in self.request('/api/project')[1]['funnel']],[2,0])
        status,finding=self.request('/api/project/findings',{'title':'Observation','observation':'Actual event','session':'session-1','timestamp':1000})
        self.assertEqual(status,200)
        self.assertTrue(self.request('/api/project/findings',{'id':finding['id'],'resolved':True})[1]['resolved'])
        report=self.request('/api/project/reports',{})[1]
        self.assertEqual(report['total']['clicks'],4)
        self.request('/api/heatmap/events',{'events':[self.click(6,timestamp=3000)]})
        self.assertEqual(self.request('/api/project')[1]['reports'][0]['total']['clicks'],4)
        self.assertEqual(self.request('/api/project')[1]['total']['clicks'],5)
        self.request('/api/project/config',{'enabled':False})
        self.assertFalse(self.request('/api/project/config')[1]['enabled'])

    def test_browser_live_workspace(self):
        self.seed()
        env={**os.environ,'LIVE_TEST_API':self.url}
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_live_project.mjs'],
                       cwd=Path(__file__).resolve().parents[1],env=env,check=True,timeout=180)

    def test_collection_parameters_persist_and_validate(self):
        self.seed()
        keys=('collectClicks','collectVisits','allowVideo')
        self.assertTrue(all(self.request('/api/project/config')[1][key] for key in keys))
        for key in keys:
            for invalid in ('false',0,None):
                self.assertEqual(self.request('/api/project/config',{key:invalid})[0],400)
        self.assertEqual(self.request('/api/project/config',dict.fromkeys(keys,False))[0],200)
        self.assertTrue(all(not self.request('/api/project/config')[1][key] for key in keys))
        self.assertEqual(self.request('/api/project')[1]['total']['clicks'],4)
        self.assertEqual(self.request('/api/project')[1]['total']['visits'],1)
        self.request('/api/project/config',{'studyTitle':'Updated'})
        self.assertFalse(self.request('/api/project/config')[1]['collectClicks'])


if __name__=='__main__':
    import unittest
    unittest.main(defaultTest='LiveProjectTests')
