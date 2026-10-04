"""Multi-task migration, isolation, sequencing and funnel drop-off evidence checks."""
import json
import os
import subprocess
from pathlib import Path
from check_live_project import LiveProjectTests
from serve_heatmap import connect,initialize

class MultiTaskTests(LiveProjectTests):
    def tasks(self):
        return [dict(id='task-a',title='Первое сообщение',instruction='Отправьте первое сообщение.',criterion='chat_message_sent'),
                dict(id='task-b',title='Второе сообщение',instruction='Отправьте ещё одно сообщение.',criterion='chat_message_sent')]

    def send(self,session,kind,task='',event_id=None,study='leed-local'):
        return self.request('/api/project/task-events',dict(id=event_id or session+'-'+kind+'-'+task,study=study,session=session,kind=kind,taskId=task,timestamp=1000,page='leed-leads-table',vw=1280,vh=900))

    def test_sequence(self):
        self.seed()
        tasks=self.tasks()
        self.assertEqual(self.request('/api/project/config',{'mode':'scenario','tasks':tasks})[0],200)
        run=self.send('multi','started')[1]['run']
        self.assertEqual([t['status'] for t in run['tasks']],['pending','not_started'])
        self.assertEqual(self.send('multi','chat_message_sent','task-b')[1]['run']['succeededTasks'],0)
        self.assertEqual(self.send('multi','chat_message_sent','task-a')[1]['run']['succeededTasks'],1)
        run=self.send('multi','finished','task-a')[1]['run']
        self.assertEqual(run['activeTaskId'],'task-b')
        self.assertEqual(run['tasks'][1]['status'],'pending')
        # A retry and a late action for A must never complete B.
        self.assertEqual(self.send('multi','finished','task-a')[1]['run']['finishedTasks'],1)
        self.assertEqual(self.send('multi','chat_message_sent','task-a',event_id='late-a')[1]['run']['succeededTasks'],1)
        self.assertEqual(self.send('multi','finished','task-b')[1]['run']['tasks'][1]['status'],'failed')
        self.assertEqual(self.send('multi','chat_message_sent','task-b',event_id='late-b')[1]['run']['succeededTasks'],1)
        self.request('/api/project/config',{'tasks':[{**tasks[1],'instruction':'Changed B'},tasks[0]]})
        self.assertEqual(self.send('multi','started',event_id='reload')[1]['run']['tasks'][1]['scenario'],tasks[1]['instruction'])
        fresh=self.send('new','started')[1]['run'];self.assertEqual(fresh['activeTaskId'],'task-b')
        self.assertNotEqual(fresh['tasks'][0]['revision'],run['tasks'][1]['revision'])
        other=self.request('/api/project/studies',{'studyTitle':'Other','scenario':'Other task'})[1]['studyId']
        self.request('/api/project/config?study='+other,{'enabled':True,'tasks':tasks})
        self.assertEqual(self.send('multi','started',event_id='other-start',study=other)[1]['run']['succeededTasks'],0)
        report=self.request('/api/project/reports',{})[1]
        self.assertEqual(next(s for s in report['sessions'] if s['id']=='multi')['task']['totalTasks'],2)
        self.request('/api/project/config',{'enabled':False})
        self.assertTrue(self.send('new','finished','task-b')[1]['paused'])

    def test_legacy_task_migration(self):
        with connect(self.db) as db:
            db.execute('INSERT INTO study_task_runs VALUES (?,?,?,?,?,?,?,?,?,?,?)',('leed-local','legacy','chat_message_sent','Old task','succeeded',10,20,20,30,1280,900))
        initialize(self.db);initialize(self.db)
        result=self.request('/api/project')[1]
        task=next(s for s in result['sessions'] if s['id']=='legacy')['task']
        self.assertEqual(task['tasks'][0]['taskId'],'legacy-task')
        self.assertEqual(task['succeededTasks'],1);self.assertEqual(task['finishedAt'],30)
        with connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM study_task_runs').fetchone()[0],1)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM study_task_attempts').fetchone()[0],1)

    def test_task_validation(self):
        tasks=self.tasks()
        for value in ([tasks[0],tasks[0]],[{**tasks[0],'criterion':'clicked_chat'}],[{**tasks[0],'instruction':''}],tasks*11):
            self.assertEqual(self.request('/api/project/config',{'mode':'scenario','tasks':value})[0],400)
        self.assertEqual(self.request('/api/project/config',{'mode':'scenario','tasks':[]})[0],400)
        self.assertEqual(self.request('/api/project/config',{'mode':'free','tasks':[{**tasks[0],'instruction':''}]})[0],200)
        self.assertEqual(self.request('/api/project/config',{'mode':'scenario'})[0],400)

    def test_funnel_last_actions(self):
        self.seed()
        self.request('/api/project/config',{'funnel':['leed-dashboard','leed-leads-table']})
        result=self.request('/api/project')[1];step=result['funnel'][1]
        lost=set(result['funnel'][0]['sessionIds'])-set(step['sessionIds'])
        self.assertEqual(len(lost),2)
        self.assertEqual(sum(item['sessions'] for item in step['lastActions']),len(lost))
        self.assertEqual({sid for item in step['lastActions'] for sid in item['sessionIds']},lost)
        self.assertTrue(all(item['kind'] in ('click','visit') for item in step['lastActions']))

    def test_browser_multi_task(self):
        self.seed()
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_multi_task.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=180)

if __name__=='__main__':
    import unittest
    unittest.main()
