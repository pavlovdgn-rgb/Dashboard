"""Custom criteria integration checks against disposable SQLite and HTTP server."""
import os
import subprocess
import unittest
from pathlib import Path
from uuid import uuid4
from check_heatmap_api import HeatmapApiTests
from serve_heatmap import connect
import success_criteria

class SuccessCriteriaTests(unittest.TestCase):
    setUp=HeatmapApiTests.setUp
    tearDown=HeatmapApiTests.tearDown
    request=HeatmapApiTests.request

    def task(self,check=None,**patch):
        return dict(id='custom-task',title='Запись',instruction='Запишитесь на консультацию',criterion='custom',successDescription='Запись подтверждена',verification=check or {'method':'manual'},**patch)

    def send(self,kind,session='custom-session',task='custom-task',**patch):
        return self.request('/api/project/task-events',{**dict(id=str(uuid4()),study='leed-local',session=session,kind=kind,taskId=task,timestamp=1000,page='leed-leads-table',vw=1280,vh=900),**patch})

    def configure(self,tasks,**patch):
        return self.request('/api/project/config',{'mode':'scenario','enabled':True,'tasks':tasks,**patch})

    def test_manual_review_snapshot_and_report(self):
        self.assertEqual(self.configure([self.task()])[0],200)
        run=self.send('started')[1]['run']
        self.assertEqual(run['status'],'pending')
        review={'session':'custom-session','taskId':'custom-task','status':'succeeded'}
        self.assertEqual(self.request('/api/project/task-review',review)[0],400)
        self.assertEqual(self.send('finished')[1]['run']['status'],'needs_review')
        report=self.request('/api/project/reports',{})[1]
        activity_before=report['sessions'][0]['lastAt']
        for state in ('succeeded','failed','indeterminate'):
            self.assertEqual(self.request('/api/project/task-review',{**review,'status':state})[0],200)
            result=self.request('/api/project')[1]
            current=next(s for s in result['sessions'] if s['id']=='custom-session')['task']
            self.assertEqual(current['status'],state)
            self.assertEqual(next(s for s in result['sessions'] if s['id']=='custom-session')['lastAt'],activity_before)
        self.assertEqual(report['sessions'][0]['task']['status'],'needs_review')
        changed=self.task();changed['successDescription']='Новый критерий'
        self.assertEqual(self.configure([changed])[0],200)
        self.assertEqual(self.send('started')[1]['run']['successDescription'],'Запись подтверждена')
        self.assertEqual(self.send('started',session='new')[1]['run']['successDescription'],'Новый критерий')
        other=self.request('/api/project/studies',{'studyTitle':'Other','scenario':'Other'})[1]['studyId']
        self.assertEqual(self.request('/api/project/task-review?study='+other,review)[0],400)
        self.assertEqual(self.request('/api/project/task-review',{**review,'session':[]})[0],400)

    def test_observed_events_scoping_and_sequence(self):
        check={'method':'automatic','type':'event','value':'booking_confirmed','page':''}
        task=self.task(check)
        self.assertEqual(self.configure([task])[0],400)
        self.request('/api/project/config',{'mode':'free','enabled':True})
        self.assertEqual(self.send('prototype_event',task='',value='booking_confirmed')[0],200)
        with connect(self.db) as db:self.assertEqual(success_criteria.catalog(db,'different-project'),[])
        second={**task,'id':'second'}
        self.assertEqual(self.configure([task,second])[0],200)
        self.send('started')
        self.assertEqual(self.send('screen_visited')[1]['run']['status'],'pending')
        self.assertEqual(self.send('prototype_event',value='wrong')[1]['run']['status'],'pending')
        self.assertEqual(self.send('prototype_event',task='second',value='booking_confirmed')[1]['run']['succeededTasks'],0)
        self.assertEqual(self.send('prototype_event',value='booking_confirmed')[1]['run']['succeededTasks'],1)
        self.send('finished')
        self.assertEqual(self.send('prototype_event',value='booking_confirmed')[1]['run']['succeededTasks'],1)
        self.request('/api/project/config',{'enabled':False})
        self.assertTrue(self.send('prototype_event',task='second',value='booking_confirmed')[1]['paused'])
        self.request('/api/project/config',{'enabled':True})
        self.send('finished',task='second')
        self.assertEqual(self.send('chat_message_sent',task='')[0],200)
        self.assertEqual(self.send('prototype_event',task='second',value='booking_confirmed')[1]['run']['succeededTasks'],1)

    def test_screen_element_and_legacy_update(self):
        for kind,typ,value in [('screen_visited','screen','leed-leads-table'),('element_clicked','element','book-button')]:
            self.request('/api/project/config',{'mode':'free','enabled':True})
            self.send(kind,session='catalog',task='',value=value)
            check={'method':'automatic','type':typ,'value':value,'page':'leed-leads-table'}
            self.assertEqual(self.configure([self.task(check)])[0],200)
            self.send('started',session=typ)
            self.assertEqual(self.send(kind,session=typ,value=value,page='leed-dashboard')[1]['run']['status'],'pending')
            self.assertEqual(self.send(kind,session=typ,value=value)[1]['run']['status'],'succeeded')
        self.assertEqual(self.request('/api/project/config',{'successCriterion':'none'})[0],200)
        self.assertNotIn('verification',self.request('/api/project/config')[1]['tasks'][0])
        self.assertEqual(self.request('/api/project/config',{'successCriterion':'custom'})[0],400)

    def test_browser_editor_and_review(self):
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_success_criteria.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=180)

    def test_browser_full_journey(self):
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_criteria_journey.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=240)

if __name__=='__main__':unittest.main(defaultTest='SuccessCriteriaTests')
