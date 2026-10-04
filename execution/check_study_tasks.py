"""Task outcomes use confirmed actions, immutable session criteria and isolated data."""
import os
import subprocess
from pathlib import Path
from check_live_project import LiveProjectTests

class StudyTaskTests(LiveProjectTests):
    def task_event(self,session,kind,**patch):
        return dict(id=session+'-'+kind,study='leed-local',session=session,kind=kind,timestamp=1000,page='leed-leads-table',vw=1280,vh=900,**patch)

    def test_outcomes(self):
        self.seed()
        self.request('/api/project/config',{'mode':'scenario','scenario':'Send a message','successCriterion':'chat_message_sent'})
        post=lambda event:self.request('/api/project/task-events',event)
        self.assertEqual(post(self.task_event('success','started'))[1]['run']['status'],'pending')
        self.assertEqual(post(self.task_event('success','lead_created'))[1]['run']['status'],'pending')
        # A later edit must not change an existing attempt's criterion or instruction.
        self.request('/api/project/config',{'successCriterion':'lead_created','scenario':'Create a lead'})
        event=self.task_event('success','chat_message_sent')
        self.assertEqual(post(event)[1]['run']['status'],'succeeded')
        self.assertEqual(post(event)[1]['run']['scenario'],'Send a message')
        self.assertEqual(post(self.task_event('success','finished'))[1]['run']['status'],'succeeded')
        self.assertEqual(post(self.task_event('failed','started'))[1]['run']['criterion'],'lead_created')
        self.assertEqual(post(self.task_event('failed','finished'))[1]['run']['status'],'failed')
        self.assertEqual(post(self.task_event('failed','lead_created'))[1]['run']['status'],'failed')
        self.request('/api/project/config',{'enabled':False})
        self.assertTrue(post(self.task_event('paused','started'))[1]['paused'])
        self.request('/api/project/config',{'enabled':True,'mode':'free'})
        self.assertTrue(post(self.task_event('free','started'))[1]['ignored'])
        result=self.request('/api/project')[1]
        self.assertEqual(len([s for s in result['sessions'] if s.get('task')]),2)
        self.assertTrue(all('task' not in s for s in result['sessions'] if s['id'].startswith('session-')))
        self.assertEqual(post({**event,'kind':'chat_opened'})[0],400)
        self.assertEqual(post({**event,'message':'private content'})[0],400)
        other=self.request('/api/project/studies',{'studyTitle':'Other'})[1]['studyId']
        self.assertEqual(self.request('/api/project?study='+other)[1]['sessions'],[])
        report=self.request('/api/project/reports',{})[1]
        self.assertEqual(next(s['task']['status'] for s in report['sessions'] if s['id']=='success'),'succeeded')

    def test_browser_tasks(self):
        self.seed()
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_study_tasks.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=150)

if __name__=='__main__':
    import unittest
    unittest.main()
