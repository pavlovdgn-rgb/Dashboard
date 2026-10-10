"""Exercise the actual HTTP handler, clean persistence, atomic retries and bounded media."""
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

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
        config = self.data('GET', '/api/index.py?__path=/api/project/config&study=biletberu-mobile')
        self.assertTrue(config['url'].startswith('https://biletberu-mobile.vercel.app/app/main?ux_study=biletberu-mobile'))
        self.assertIn('ux_token=', config['url'])
        self.assertEqual(self.request('GET', '/api/index.py?__path=/sdk.js')[0], 200)

    def test_clicks_retry_conflict_and_reconnect(self):
        self.data('POST', '/api/project/config', {'enabled':True})
        event = dict(id='cloud-event-1',study='biletberu-mobile',session='cloud-session-1',seq=1,
                     page='bb-main',version='biletberu-v1',target='test-button',x=.3,y=.4,
                     vw=1280,vh=720,rw=1280,rh=720,scroll_x=0,scroll_y=0,timestamp=1000,
                     context={'signature':'1234567890abcdef','scrolls':[]})
        self.data('POST', '/api/heatmap/events', {'events':[event]})
        self.data('POST', '/api/heatmap/events', {'events':[event]})
        self.data('POST', '/api/heatmap/events', {'events':[{**event,'x':.9}]}, status=400)
        result = self.data('GET', '/api/heatmap?study=biletberu-mobile&aggregation=page')
        self.assertEqual(result['total']['clicks'], 1)
        api._migrated = False  # Simulate a cold function initialization, preserve the same database.
        self.assertEqual(self.data('GET', '/api/heatmap?study=biletberu-mobile')['total']['clicks'], 1)
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
        self.assertIn('biletberu-mobile.vercel.app/app/main', study['url'])
        self.assertEqual(self.data('GET', '/api/project?study='+study['studyId'])['total']['clicks'], 0)
        snapshot = {'id':'cloud-snapshot','html':'<!doctype html><html><body>Тест</body></html>','width':1280,'height':720}
        self.data('POST', '/api/heatmap/snapshots', snapshot)
        self.assertEqual(self.data('GET', '/api/heatmap/snapshots?id=cloud-snapshot')['html'], snapshot['html'])

    def test_delete_study_removes_only_its_data(self):
        first=self.data('POST','/api/project/studies',{'studyTitle':'Удаляемое исследование'})['studyId']
        second=self.data('POST','/api/project/studies',{'studyTitle':'Соседнее исследование'})['studyId']
        self.assertEqual(self.request('POST','/api/project/studies/delete',{'studyId':first},authenticated=False)[0],401)
        with api.cloud_db.connect() as db:
            for key in ('shared-snapshot','only-first-snapshot'):
                db.execute('INSERT INTO snapshots VALUES (?,?,?,?)',(key,'<!doctype html><html></html>',390,844))
            for key,study,snapshot in (('first-click',first,'shared-snapshot'),('first-only-click',first,'only-first-snapshot'),('second-click',second,'shared-snapshot')):
                db.execute('''INSERT INTO clicks (id,study,session,seq,page,version,layout,target,x,y,vw,vh,rw,rh,scroll_x,scroll_y,timestamp,context)
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (key,study,'session-'+key,1,'bb-main','v1','layout','button',.5,.5,390,844,390,844,0,0,1000,json.dumps({'snapshot':snapshot})))
            db.execute('INSERT INTO visits VALUES (?,?,?,?,?,?,?,?)',('first-visit',first,'session-first','bb-main',1000,390,844,'{}'))
            db.execute('INSERT INTO replay_frames (id,study,session,seq,timestamp,page,snapshot,vw,vh,kind,label) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                       ('first-frame',first,'session-first',1,1000,'bb-main','<html></html>',390,844,'screen','Главная'))
            db.execute('INSERT INTO recordings (id,study,session,startedAt,mime) VALUES (?,?,?,?,?)',('first-recording',first,'session-first',1000,'video/webm'))
            db.execute('INSERT INTO recording_chunks VALUES (?,?,?,?)',('first-recording',0,b'video','digest'))
            db.execute('INSERT INTO study_task_sessions VALUES (?,?,?,?,?)',(first,'session-first',1000,390,844))
            db.execute('INSERT INTO live_findings (id,value,study) VALUES (?,?,?)',('first-finding','{}',first))
            db.execute('INSERT INTO live_reports (id,value,study) VALUES (?,?,?)',('first-report','{}',first))
        result=self.data('POST','/api/project/studies/delete',{'studyId':first})
        self.assertEqual(result['deleted'],first)
        self.assertNotIn(first,[item['studyId'] for item in self.data('GET','/api/project/studies')['studies']])
        self.assertEqual(self.request('GET','/api/project/config?study='+first)[0],400)
        self.assertNotEqual(self.data('GET','/api/project?study='+first)['project']['studyId'],first)
        self.assertEqual(self.request('POST','/api/project/studies/delete',{'studyId':first})[0],400)
        self.assertEqual(self.request('POST','/api/project/studies/delete',{'studyId':'leed-local'})[0],400)
        with api.cloud_db.connect() as db:
            for table in ('clicks','visits','replay_frames','recordings','study_task_sessions','live_findings','live_reports'):
                self.assertEqual(db.execute(f'SELECT COUNT(*) FROM {table} WHERE study=?',(first,)).fetchone()[0],0,table)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM recording_chunks WHERE recording=?',('first-recording',)).fetchone()[0],0)
            self.assertIsNone(db.execute('SELECT id FROM snapshots WHERE id=?',('only-first-snapshot',)).fetchone())
            self.assertIsNotNone(db.execute('SELECT id FROM snapshots WHERE id=?',('shared-snapshot',)).fetchone())
            self.assertIsNotNone(db.execute('SELECT id FROM clicks WHERE study=?',(second,)).fetchone())
        late={'id':'late-deleted-snapshot','study':first,'html':'<!doctype html><html></html>','width':390,'height':844}
        self.assertTrue(self.data('POST','/api/heatmap/snapshots',late)['closed'])
        late_click=dict(id='late-deleted-click',study=first,session='late-session',seq=1,page='bb-main',
                        version='biletberu-v1',target='button',x=.5,y=.5,vw=390,vh=844,rw=390,rh=844,
                        scroll_x=0,scroll_y=0,timestamp=2000,context={'signature':'1234567890abcdef','scrolls':[]})
        self.assertEqual(self.data('POST','/api/heatmap/events',{'events':[late_click]})['accepted'],[late_click['id']])
        with api.cloud_db.connect() as db:
            self.assertIsNone(db.execute('SELECT id FROM snapshots WHERE id=?',(late['id'],)).fetchone())
            self.assertIsNone(db.execute('SELECT id FROM clicks WHERE id=?',(late_click['id'],)).fetchone())

    def test_last_study_can_be_deleted_and_created_again(self):
        import live_project
        with tempfile.TemporaryDirectory() as folder:
            db=sqlite3.connect(str(Path(folder)/'isolated.sqlite3'))
            db.row_factory=sqlite3.Row
            try:
                db.executescript((ROOT/'execution/schema.sql').read_text(encoding='utf-8'))
                live_project.initialize(db)
                deleted=live_project.delete_study(db,'biletberu-mobile')
                self.assertIsNone(deleted['nextStudyId'])
                live_project.initialize(db)
                self.assertEqual(live_project.get(db,'/api/project',{},lambda value:value)['studies'],[])
                created=live_project.post(db,'/api/project/studies',{'studyTitle':'Новое первое'},lambda value:value,[])
                self.assertEqual(live_project.get(db,'/api/project',{},lambda value:value)['project']['studyId'],created['studyId'])
            finally:
                db.close()

    def test_existing_cloud_database_migrates_to_deletion_schema(self):
        import live_project
        with tempfile.TemporaryDirectory() as folder:
            previous=os.environ['UXLAB_TEST_DB']
            os.environ['UXLAB_TEST_DB']=str(Path(folder)/'version-two.sqlite3')
            try:
                with api.cloud_db.connect() as db:
                    db.executescript((ROOT/'execution/schema.sql').read_text(encoding='utf-8'))
                    live_project.initialize(db)
                    db.execute('DROP TABLE deleted_studies')
                    db.execute('INSERT INTO cloud_schema VALUES (2)')
                api.cloud_db.migrate()
                with api.cloud_db.connect() as db:
                    self.assertIsNotNone(db.execute('SELECT version FROM cloud_schema WHERE version=3').fetchone())
                    self.assertIsNotNone(db.execute('SELECT id FROM live_studies WHERE id=?',('biletberu-mobile',)).fetchone())
                    self.assertIsNotNone(db.execute("SELECT name FROM sqlite_master WHERE name='deleted_studies'").fetchone())
            finally:
                os.environ['UXLAB_TEST_DB']=previous

    def test_mobile_link_collects_only_its_study(self):
        origin='https://biletberu-mobile.vercel.app'
        self.data('POST','/api/project/config',{'enabled':False})

        config=self.data('GET','/api/project/config')
        token=parse_qs(urlsplit(config['url']).fragment)['ux_token'][0]
        headers={'Origin':origin,'X-UXLab-Participant':token}
        path='/api/project/config?study=biletberu-mobile'
        code,cors,payload=self.request('GET',path,extra=headers,authenticated=False)
        self.assertEqual(code,200,payload)
        self.assertEqual(cors['Access-Control-Allow-Origin'],origin)
        self.assertEqual(self.request('GET',path,extra={'Origin':origin,'X-UXLab-Participant':'wrong'},authenticated=False)[0],403)
        self.assertEqual(self.request('GET','/api/project?study=biletberu-mobile',extra=headers,authenticated=False)[0],401)
        self.assertEqual(self.request('OPTIONS','/api/project/visit',extra={'Origin':origin},authenticated=False)[0],204)
        visit=dict(id='mobile-link-visit',study='biletberu-mobile',session='mobile-link-session',page='bb-main',
                   timestamp=3000,vw=390,vh=844,context={'signature':'1234567890abcdef','scrolls':[]})
        endpoint='/api/project/visit?study=biletberu-mobile'
        code,_,payload=self.request('POST',endpoint,visit,extra=headers,authenticated=False)
        self.assertEqual(code,200,payload)
        self.assertTrue(json.loads(payload)['paused'])
        self.data('POST','/api/project/config',{'enabled':True})
        self.assertEqual(self.request('POST',endpoint,{**visit,'study':'leed-local'},extra=headers,authenticated=False)[0],403)
        code,_,payload=self.request('POST',endpoint,visit,extra=headers,authenticated=False)
        self.assertEqual(code,200,payload)
        self.assertEqual(self.data('GET','/api/project')['total']['sessions']>=1,True)
        task=dict(id='mobile-link-task',study='biletberu-mobile',session='mobile-link-session',kind='screen_visited',
                  taskId='',timestamp=3001,page='bb-main',vw=390,vh=844)
        task_endpoint='/api/project/task-events?study=biletberu-mobile'
        self.assertEqual(self.request('POST',task_endpoint,{**task,'study':'legacy-video'},extra=headers,authenticated=False)[0],403)
        code,_,payload=self.request('POST',task_endpoint,task,extra=headers,authenticated=False)
        self.assertEqual(code,200,payload)
        self.assertTrue(json.loads(payload)['ignored'])
        snapshot=dict(id='s3-mobile-link-test',study='biletberu-mobile',
                      html='<!doctype html><html><body>Снимок</body></html>',width=390,height=844)
        snap_endpoint='/api/heatmap/snapshots?study=biletberu-mobile'
        self.assertEqual(self.request('POST',snap_endpoint,{**snapshot,'study':'leed-local'},extra=headers,authenticated=False)[0],403)
        self.assertEqual(self.request('POST',snap_endpoint,snapshot,extra=headers,authenticated=False)[0],200)
        self.assertEqual(self.data('GET','/api/heatmap/snapshots?id='+snapshot['id'])['html'],snapshot['html'])
        self.data('POST','/api/project/config',{'enabled':False})

    def test_existing_lead_data_is_archived_without_mixing_mobile_results(self):
        original=os.environ['UXLAB_TEST_DB']
        with tempfile.TemporaryDirectory() as folder:
            database=str(Path(folder)/'legacy.sqlite3')
            raw=sqlite3.connect(database)
            raw.executescript((ROOT/'execution/schema.sql').read_text())
            raw.execute('INSERT INTO visits VALUES (?,?,?,?,?,?,?,?)',
                        ('legacy-visit','leed-local','legacy-session','leed-dashboard',1000,390,844,'{}'))
            raw.commit();raw.close()
            try:
                os.environ['UXLAB_TEST_DB']=database
                api.cloud_db.migrate()
                with api.cloud_db.connect() as db:
                    legacy=json.loads(db.execute("SELECT value FROM live_studies WHERE id='leed-local'").fetchone()[0])
                    mobile=json.loads(db.execute("SELECT value FROM live_studies WHERE id='biletberu-mobile'").fetchone()[0])
                    self.assertFalse(legacy['enabled'])
                    self.assertTrue(legacy['roundClosedAt'])
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM visits WHERE study='leed-local'").fetchone()[0],1)
                    self.assertFalse(mobile['enabled'])
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM visits WHERE study='biletberu-mobile'").fetchone()[0],0)
                    self.assertIsNotNone(db.execute('SELECT version FROM cloud_schema WHERE version=2').fetchone())
                api.cloud_db.migrate()
            finally:
                os.environ['UXLAB_TEST_DB']=original

    def test_round_creates_new_cloud_participant_link(self):
        study=self.data('POST','/api/project/studies',{'studyTitle':'Проверка раундов'})['studyId']
        config='/api/project/config?study='+study
        self.data('POST',config,{'enabled':True})
        visit=dict(id='cloud-round-visit',study=study,session='tester',page='bb-main',
                   timestamp=2000,vw=1280,vh=720,context={'signature':'1234567890abcdef','scrolls':[]})
        self.data('POST','/api/project/visit',visit)
        fixed=self.data('POST','/api/project/rounds?study='+study,{})
        new=fixed['next']
        self.assertTrue(fixed['fixed']['roundClosedAt'])
        self.assertFalse(fixed['fixed']['enabled'])
        self.assertIn('ux_study='+new['studyId'],new['url'])
        self.assertEqual(new['recordingMode'],'video')
        self.assertEqual(self.data('GET','/api/project?study='+new['studyId'])['total']['sessions'],0)
        self.assertEqual(self.data('GET','/api/project?study='+study)['total']['sessions'],1)
        late={**visit,'id':'cloud-round-late','session':'late'}
        self.assertTrue(self.data('POST','/api/project/visit',late)['closed'])
        click=dict(id='cloud-round-click',study=study,session='late',seq=1,page='bb-main',
                   version='leed-local-v2',target='button',x=.3,y=.4,vw=1280,vh=720,rw=1280,rh=720,
                   scroll_x=0,scroll_y=0,timestamp=3000,context={'signature':'1234567890abcdef','scrolls':[]})
        self.assertEqual(self.data('POST','/api/heatmap/events',{'events':[click]})['accepted'],[click['id']])
        self.assertEqual(self.data('GET','/api/project?study='+study)['total']['sessions'],1)
        self.assertEqual(self.data('GET','/api/project?study='+study)['total']['clicks'],0)
        self.assertEqual(self.request('POST',config,{'enabled':True})[0],400)

    def test_automatic_tasks_finish_and_advance(self):
        for kind, typ, value in [('screen_visited','screen','bb-main'),
                                 ('element_clicked','element','confirm-button'),
                                 ('prototype_event','event','order_confirmed')]:
            with self.subTest(type=typ):
                study = self.data('POST','/api/project/studies',{'studyTitle':'Auto '+typ})['studyId']
                config = '/api/project/config?study='+study
                self.data('POST',config,{'enabled':True,'mode':'free'})
                def send(event_id, action, task='', **extra):
                    return self.data('POST','/api/project/task-events',dict(
                        id=study+'-'+event_id,study=study,session='auto-session',kind=action,
                        taskId=task,timestamp=1000,page='bb-main',vw=1280,vh=900,**extra))['run']
                send('catalog',kind,value=value)
                check = dict(method='automatic',type=typ,value=value,page='' if typ=='event' else 'bb-main')
                task = dict(id='first',title='Первое',instruction='Выполните действие',criterion='custom',
                            successDescription='Действие выполнено',verification=check)
                self.data('POST',config,{'mode':'scenario','tasks':[task,{**task,'id':'second'},
                    {**task,'id':'manual','verification':{'method':'manual'}}]})
                self.assertEqual(send('start','started')['activeTaskId'],'first')
                self.assertEqual(send('wrong','prototype_event','first',value='wrong')['succeededTasks'],0)
                self.data('POST',config,{'enabled':False})
                paused = dict(id=study+'-pause',study=study,session='auto-session',kind=kind,taskId='first',
                              timestamp=1000,page='bb-main',vw=1280,vh=900,value=value)
                self.assertTrue(self.data('POST','/api/project/task-events',paused)['paused'])
                self.data('POST',config,{'enabled':True})
                run=send('success',kind,'first',value=value)
                self.assertEqual(run['activeTaskId'],'second')
                self.assertEqual(run['finishedTasks'],1)
                self.assertEqual(run['tasks'][0]['status'],'succeeded')
                self.assertEqual(run['tasks'][0]['finishedAt'],1000)
                self.assertEqual(run['tasks'][0]['completedAt'],1000)
                self.assertEqual(send('success',kind,'first',value=value)['finishedTasks'],1)
                self.assertEqual(send('late',kind,'first',value=value)['finishedTasks'],1)
                # An in-progress session keeps its original automatic criterion after edits.
                self.data('POST',config,{'tasks':[{**task,'verification':{'method':'manual'}}]})
                run=send('second-success',kind,'second',value=value)
                self.assertEqual(run['activeTaskId'],'manual')
                self.assertEqual(run['finishedTasks'],2)
                self.assertEqual(send('manual-action',kind,'manual',value=value)['finishedTasks'],2)
                run=send('manual-finish','finished','manual')
                self.assertIsNone(run['activeTaskId'])
                self.assertEqual(run['finishedTasks'],3)
                self.assertEqual(run['tasks'][2]['status'],'needs_review')
                api._migrated=False
                saved=next(s for s in self.data('GET','/api/project?study='+study)['sessions'] if s['id']=='auto-session')['task']
                self.assertEqual(saved['succeededTasks'],2)
                self.assertEqual(saved['finishedTasks'],3)
                # Manual exit is available even without the success signal.
                self.data('POST',config,{'tasks':[task,{**task,'id':'second'}]})
                exit_event=dict(id=study+'-exit-start',study=study,session='exit-session',kind='started',
                                taskId='',timestamp=2000,page='bb-main',vw=1280,vh=900)
                self.data('POST','/api/project/task-events',exit_event)
                finish={**exit_event,'id':study+'-exit','kind':'finished','taskId':'first'}
                run=self.data('POST','/api/project/task-events',finish)['run']
                self.assertEqual(run['activeTaskId'],'second')
                self.assertEqual(run['tasks'][0]['status'],'failed')
                self.assertIsNone(run['tasks'][0]['completedAt'])
                self.assertEqual(run['finishedTasks'],1)
                self.assertEqual(self.data('POST','/api/project/task-events',finish)['run']['finishedTasks'],1)
                late={**finish,'id':study+'-late-after-exit','kind':kind,'value':value}
                run=self.data('POST','/api/project/task-events',late)['run']
                self.assertEqual(run['succeededTasks'],0)
                self.assertEqual(run['tasks'][0]['status'],'failed')
                run=self.data('POST','/api/project/task-events',{**finish,'id':study+'-exit-last','taskId':'second'})['run']
                self.assertIsNone(run['activeTaskId'])
                self.assertEqual(run['finishedTasks'],2)
                self.assertEqual(run['succeededTasks'],0)

    def test_mobile_screens_can_be_selected_before_first_visit(self):
        study=self.data('POST','/api/project/studies',{'studyTitle':'Выбор экрана без событий'})['studyId']
        signals=self.data('GET','/api/project/criteria-catalog?study='+study)['signals']
        screens={signal['value']:signal for signal in signals if signal['type']=='screen'}
        self.assertEqual(len(screens),len(api.serve_heatmap.MOBILE_ROUTES))
        self.assertEqual(screens['bb-done']['label'],'Оплата прошла')
        self.assertEqual(screens['bb-done']['lastAt'],0)
        check={'method':'automatic','type':'screen','value':'bb-done','page':'bb-done'}
        task={'id':'purchase','title':'Совершить покупку','instruction':'Совершить покупку',
              'criterion':'custom','successDescription':'Открыт экран успешной оплаты','verification':check}
        saved=self.data('POST','/api/project/config?study='+study,{'mode':'scenario','tasks':[task]})
        self.assertEqual(saved['tasks'][0]['verification'],check)

    def test_mobile_heatmap_separates_saved_scroll_states(self):
        study=self.data('POST','/api/project/studies',{'studyTitle':'Снимки при кликах'})['studyId']
        self.data('POST','/api/project/config?study='+study,{'enabled':True})
        for index in (1,2):
            snapshot=dict(id=f's3-scroll-{index}',study=study,
                          html=f'<!doctype html><html><body>Состояние {index}</body></html>',width=390,height=844)
            self.data('POST','/api/heatmap/snapshots',snapshot)
            click=dict(id=f'click-scroll-{index}',study=study,session='scroll-tester',seq=index,
                       page='bb-main',version='biletberu-v1',target=f'el-{index}',x=.5,y=.5,
                       vw=390,vh=844,rw=390,rh=844,scroll_x=0,scroll_y=0,timestamp=1000+index,
                       context={'signature':'1234567890abcdef','scrolls':[[0,0,index*200]],'snapshot':snapshot['id'],
                                'element':{'label':'Кнопка','rect':[.4,.4,.2,.2]}})
            self.data('POST','/api/heatmap/events',{'events':[click]})
        groups=self.data('GET','/api/heatmap?study='+study+'&aggregation=page')['groups']
        mobile=[group for group in groups if group['page']=='bb-main']
        self.assertEqual({group['context']['snapshot'] for group in mobile},{'s3-scroll-1','s3-scroll-2'})
        for group in mobile:
            result=self.data('GET','/api/heatmap?study='+study+'&aggregation=page&group='+group['layout'])
            self.assertEqual(sum(point['count'] for point in result['points']),1)

    def test_previous_round_clicks_are_available_as_element_checks(self):
        study=self.data('POST','/api/project/studies',{'studyTitle':'Клики прошлых раундов'})['studyId']
        self.data('POST','/api/project/config?study='+study,{'enabled':True})
        click=dict(id='historical-element-click',study=study,session='earlier-tester',seq=1,
                   page='bb-payment',version='biletberu-v1',target='el-fedcba9876543210',x=.4,y=.7,
                   vw=390,vh=844,rw=390,rh=844,scroll_x=0,scroll_y=0,timestamp=5000,
                   context={'signature':'1234567890abcdef','scrolls':[],
                            'element':{'label':'Кнопка','rect':[.2,.6,.4,.1]}})
        self.data('POST','/api/heatmap/events',{'events':[click]})
        next_study=self.data('POST','/api/project/rounds?study='+study,{})['next']['studyId']
        signals=self.data('GET','/api/project/criteria-catalog?study='+next_study)['signals']
        element=next(signal for signal in signals if signal['type']=='element' and signal['value']==click['target'])
        self.assertEqual((element['page'],element['label'],element['lastAt']),('bb-payment','Кнопка',5000))
        check={'method':'automatic','type':'element','value':click['target'],'page':'bb-payment'}
        task={'id':'payment-click','title':'Нажать кнопку','instruction':'Нажмите кнопку',
              'criterion':'custom','successDescription':'Кнопка нажата','verification':check}
        saved=self.data('POST','/api/project/config?study='+next_study,{'mode':'scenario','tasks':[task]})
        self.assertEqual(saved['tasks'][0]['verification'],check)

    def test_read_requests_do_not_wait_for_a_writer(self):
        self.data('GET', '/api/project/config')
        writer = sqlite3.connect(self.database)
        try:
            writer.execute('BEGIN IMMEDIATE')
            writer.execute('INSERT INTO cloud_schema VALUES (99)')
            api._migrated = False  # A cold instance also checks the schema without a write lock.
            started = time.monotonic()
            self.data('GET', '/api/project')
            self.data('GET', '/api/heatmap?study=biletberu-mobile&aggregation=page')
            self.assertLess(time.monotonic() - started, 2)
            with api.cloud_db.read_only():
                with api.cloud_db.connect() as db:
                    self.assertIsNone(db.execute('SELECT version FROM cloud_schema WHERE version=99').fetchone())
                with self.assertRaises(sqlite3.OperationalError):
                    with api.cloud_db.connect() as db:
                        db.execute('INSERT INTO cloud_schema VALUES (100)')
        finally:
            writer.rollback()
            writer.close()
        # Leaving the read scope must not turn later POST requests into read-only operations.
        self.data('POST', '/api/project/config', {'enabled':True})

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
            db.execute('BEGIN TRANSACTION READONLY')
            self.assertEqual(db.execute('SELECT id FROM sdk_check').fetchone()[0], 7)
            # Embedded libSQL accepts READONLY as a routing hint but does not
            # enforce it locally. This test checks SDK syntax and result handling;
            # the HTTP concurrency test separately checks GET isolation.
            raw.rollback()
        finally:
            raw.close()

    def test_uploads_with_rewrite_queries(self):
        # Production rewrites can preserve the public path and append __path.
        # Other query parameters must not turn a valid upload into a 404 either.
        for index, prefix in enumerate(('/api/heatmap/', '/api/index.py?__path=/api/heatmap/')):
            snapshot_path = prefix + 'snapshots'
            event_path = prefix + 'events'
            if index == 0:
                snapshot_path += '?__path=/api/heatmap/snapshots'
                event_path += '?__path=/api/heatmap/events'
            snapshot = {'id':f'rewrite-snapshot-{index}', 'html':'<!doctype html><html><body>Rewrite</body></html>', 'width':1280, 'height':720}
            self.data('POST', snapshot_path, snapshot)
            event = dict(id=f'rewrite-event-{index}', study='routing-check', session='rewrite-session',
                         seq=index+1, page='leed-leads-table', version='leed-local-v2', target='button',
                         x=.3, y=.4, vw=1280, vh=720, rw=1280, rh=720, scroll_x=0, scroll_y=0,
                         timestamp=1000, context={'signature':'1234567890abcdef', 'scrolls':[], 'snapshot':snapshot['id']})
            self.data('POST', event_path, {'events':[event]})
            self.data('POST', '/api/heatmap/events?retry=1', {'events':[event]})
        result = self.data('GET', '/api/heatmap?study=routing-check&aggregation=page')
        self.assertEqual(result['total']['clicks'], 2)
        self.assertEqual(len(result['groups']), 1)

    def test_video_chunks_ranges_and_download(self):
        self.data('GET', '/api/project/config')
        with api.cloud_db.connect() as db:
            old_study={'id':'leed-generation','title':'Lead Generation','studyId':'legacy-video',
                       'studyTitle':'Legacy video','url':'/participant/leads-table?ux_study=legacy-video',
                       'enabled':True,'allowVideo':True,'recordingMode':'video','collectClicks':True,'collectVisits':True,
                       'funnel':[],'scenario':'','mode':'free','successCriterion':'none'}
            db.execute('INSERT OR REPLACE INTO live_studies VALUES (?,?,?,?)',
                       ('legacy-video','leed-generation',json.dumps(old_study),0))
        record = dict(id='cloud-video',study='legacy-video',session='cloud-session-1',startedAt=1000,mime='video/webm')
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
            status, headers, body = self.request('GET', '/api/recordings/media?id=cloud-video&study=legacy-video', extra={'Range':f'bytes={len(assembled)}-'})
            self.assertEqual(status, 206)
            self.assertLessEqual(len(body), api.cloud_video.MAX_RESPONSE)
            assembled += body
            if len(assembled) == int(headers['Content-Range'].split('/')[1]):
                break
        expected = api.session_video.webm_duration(source, 5.0)
        self.assertEqual(assembled, expected)
        self.assertEqual(self.request('GET','/api/recordings/media?id=cloud-video&study=legacy-video',extra={'Range':'bytes=99999999-'})[0],416)
        self.assertEqual(self.request('GET','/api/recordings/media?id=cloud-video&study=missing')[0],400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
