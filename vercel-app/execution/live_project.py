"""Real Lead Generation workspace: configuration, sessions, visits and derived results.

No sample events or outcomes are generated. Existing heatmap clicks remain the source of truth.
"""
import json
import math
import re
import time
import uuid
import study_tasks
import success_criteria
import project_reports
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from collections import defaultdict

STUDY = 'leed-local'
DEFAULT = {'id':'leed-generation','title':'Lead Generation','studyId':STUDY,
           'studyTitle':'Исследование Lead Generation','url':'/participant/leads-table?ux_study=leed-local',
           'enabled':True,'funnel':[],'collectClicks':True,'collectVisits':True,'allowVideo':True,'recordingMode':'video','scenario':'','mode':'free','successCriterion':'none'}


def initialize(db):
    study_tasks.initialize(db)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS live_settings (id TEXT PRIMARY KEY, value TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS live_studies (id TEXT PRIMARY KEY, project_id TEXT NOT NULL, value TEXT NOT NULL, created_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS visits (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        page TEXT NOT NULL, timestamp INTEGER NOT NULL, vw INTEGER NOT NULL, vh INTEGER NOT NULL, context TEXT NOT NULL);
      CREATE INDEX IF NOT EXISTS visits_study_session ON visits(study,session,timestamp);
      CREATE TABLE IF NOT EXISTS live_findings (id TEXT PRIMARY KEY, value TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS live_reports (id TEXT PRIMARY KEY, value TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS replay_frames (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        seq INTEGER NOT NULL, timestamp INTEGER NOT NULL, page TEXT NOT NULL, snapshot TEXT NOT NULL,
        vw INTEGER NOT NULL, vh INTEGER NOT NULL, kind TEXT NOT NULL, label TEXT NOT NULL, target TEXT NOT NULL DEFAULT '{}');
      CREATE UNIQUE INDEX IF NOT EXISTS replay_frames_sequence ON replay_frames(study,session,seq);
    ''')
    if 'target' not in {row[1] for row in db.execute('PRAGMA table_info(replay_frames)')}:
        db.execute("ALTER TABLE replay_frames ADD COLUMN target TEXT NOT NULL DEFAULT '{}'")
    db.execute('INSERT OR IGNORE INTO live_settings VALUES (?,?)',('project',json.dumps(DEFAULT)))
    legacy={**DEFAULT,**json.loads(db.execute("SELECT value FROM live_settings WHERE id='project'").fetchone()[0])}
    db.execute('INSERT OR IGNORE INTO live_studies VALUES (?,?,?,?)',(STUDY,DEFAULT['id'],json.dumps(legacy,ensure_ascii=False),0))
    for table in ('live_findings','live_reports'):
        if 'study' not in {row[1] for row in db.execute('PRAGMA table_info('+table+')')}:
            db.execute("ALTER TABLE "+table+" ADD COLUMN study TEXT NOT NULL DEFAULT 'leed-local'")
        db.execute('CREATE INDEX IF NOT EXISTS '+table+'_study ON '+table+'(study)')


def settings(db,study=STUDY):
    row=db.execute('SELECT value FROM live_studies WHERE id=?',(study,)).fetchone()
    if not row:raise ValueError('Unknown study')
    saved=json.loads(row[0])
    config={**DEFAULT,**saved,'mode':saved.get('mode','scenario' if saved.get('scenario') else 'free')}
    return {**config,'tasks':study_tasks.definitions(config)}


def round_closed(db,study):
    """Collector paths also serve non-project test studies, so unknown IDs stay open."""
    row=db.execute('SELECT value FROM live_studies WHERE id=?',(study,)).fetchone()
    return bool(row and json.loads(row[0]).get('roundClosedAt'))


def participant_url(base,study):
    url=urlsplit(base)
    return urlunsplit((url.scheme,url.netloc,url.path,urlencode([(k,v) for k,v in parse_qsl(url.query) if k!='ux_study']+[('ux_study',study)]),url.fragment))


def studies(db):
    result=[]
    for row in db.execute('SELECT id,created_at FROM live_studies WHERE project_id=? ORDER BY created_at DESC,id',(DEFAULT['id'],)):
        config=settings(db,row['id'])
        count=db.execute('SELECT COUNT(DISTINCT session) FROM (SELECT session FROM clicks WHERE study=? UNION ALL SELECT session FROM visits WHERE study=? UNION ALL SELECT session FROM replay_frames WHERE study=? UNION ALL SELECT session FROM recordings WHERE study=? UNION ALL SELECT session FROM study_task_sessions WHERE study=?)',(row['id'],)*5).fetchone()[0]
        result.append({**config,'createdAt':row['created_at'],'sessions':count})
    return result


def rows(db,session=None,study=STUDY):
    args=(study,session) if session else (study,)
    where='study=?'+(' AND session=?' if session else '')
    clicks=[{**dict(row),'kind':'click'} for row in db.execute('SELECT * FROM clicks WHERE '+where,args)]
    visits=[{**dict(row),'kind':'visit'} for row in db.execute('SELECT * FROM visits WHERE '+where,args)]
    for row in clicks+visits:
        row['context']=json.loads(row['context']) if row['context'] else {}
    return sorted(clicks+visits,key=lambda row:(row['timestamp'],row.get('seq',0),row['id']))


def signals_for(events):
    """One burst signal per cluster: >=3 clicks within 1s, 24 CSS px, same viewport/page."""
    result=[];recent=[];emitted=False;previous=None
    for event in events:
        if event['kind']!='click':continue
        related=previous and event['page']==previous['page'] and event['vw']==previous['vw'] and event['vh']==previous['vh']
        anchor=recent[0] if recent else previous
        related=related and math.hypot((event['x']-anchor['x'])*event['vw'],(event['y']-anchor['y'])*event['vh'])<=24
        if not related or event['timestamp']-previous['timestamp']>1000:recent=[];emitted=False
        recent=[item for item in recent if event['timestamp']-item['timestamp']<=1000]
        recent.append(event)
        if len(recent)>=3 and not emitted:
            result.append({'id':event['id'],'session':event['session'],'page':event['page'],
                           'timestamp':event['timestamp'],'label':'Повторные клики','count':len(recent),
                           'target':event['context'].get('element',{}).get('label','Область кликов')})
            emitted=True
        previous=event
    return result


def summary(db,device='all',study=STUDY):
    if device not in ('all','desktop','mobile'):raise ValueError('Invalid device')
    config=settings(db,study)
    events=rows(db,study=study)
    last_event_at=max((row['timestamp'] for row in events),default=None)
    if device!='all':events=[row for row in events if ('mobile' if row['vw']<768 else 'desktop')==device]
    by_session=defaultdict(list);by_page=defaultdict(list)
    for row in events:by_session[row['session']].append(row);by_page[row['page']].append(row)
    signals=[];sessions=[]
    for key,items in by_session.items():
        found=signals_for(items);signals.extend(found)
        sessions.append({'id':key,'startedAt':items[0]['timestamp'],'lastAt':items[-1]['timestamp'],
            'clicks':sum(item['kind']=='click' for item in items),'visits':sum(item['kind']=='visit' for item in items),
            'pages':list(dict.fromkeys(item['page'] for item in items)),
            'signals':len(found),'snapshots':sum(bool(item['context'].get('snapshot')) for item in items)})
    sessions.sort(key=lambda row:row['lastAt'],reverse=True)
    recordings=[dict(row) for row in db.execute("SELECT session,status,startedAt,duration FROM recordings WHERE study=?",(study,))]
    frame_where='study=?'+(' AND vw<768' if device=='mobile' else ' AND vw>=768' if device=='desktop' else '')
    frames=list(db.execute('SELECT session,COUNT(*) AS count,MIN(timestamp) AS startedAt,MAX(timestamp) AS lastAt,GROUP_CONCAT(DISTINCT page) AS pages FROM replay_frames WHERE '+frame_where+' GROUP BY session',(study,)))
    for frame in frames:
        session=next((item for item in sessions if item['id']==frame['session']),None)
        if session is None:
            session={'id':frame['session'],'startedAt':frame['startedAt'],'lastAt':frame['lastAt'],'clicks':0,'visits':0,'pages':[],'signals':0,'snapshots':0}
            sessions.append(session)
        session['frames']=frame['count']
        session['pages']=list(dict.fromkeys(session['pages']+frame['pages'].split(',')))
        session['startedAt']=min(session['startedAt'],frame['startedAt'])
        session['lastAt']=max(session['lastAt'],frame['lastAt'])
    for session in sessions:
        session['recordings']=sum(row['session']==session['id'] and row['status']=='ready' for row in recordings)
    if device=='all':
        for row in recordings:
            if any(session['id']==row['session'] for session in sessions):continue
            sessions.append({'id':row['session'],'startedAt':row['startedAt'],'lastAt':row['startedAt']+row['duration']*1000,'clicks':0,'visits':0,'pages':[],'signals':0,'snapshots':0,'recordings':sum(item['session']==row['session'] and item['status']=='ready' for item in recordings)})
    study_tasks.enrich(db,sessions,study,device)
    sessions.sort(key=lambda row:row['lastAt'],reverse=True)
    pages=[{'id':key,'clicks':sum(item['kind']=='click' for item in items),
            'visits':sum(item['kind']=='visit' for item in items),'sessions':len({item['session'] for item in items})}
           for key,items in by_page.items()]
    pages.sort(key=lambda row:(-row['clicks'],row['id']))
    funnel=[]
    for index,page in enumerate(config['funnel']):
        matched=[]
        for key,items in by_session.items():
            next_step=0
            # Visits are explicit after the migration; historical clicks also prove presence on a page.
            for item in items:
                if item['page']==config['funnel'][next_step]:next_step+=1
                if next_step>index:matched.append(key);break
        funnel.append({'page':page,'sessions':len(matched),'sessionIds':matched})
        last_actions={}
        if index:
            for session in set(funnel[index-1]['sessionIds'])-set(matched):
                last=by_session[session][-1]
                label=last['context'].get('element',{}).get('label') or 'Область без названия'
                key=(last['kind'],last['page'],label)
                last_actions.setdefault(key,[]).append(session)
        funnel[-1]['lastActions']=[{'kind':kind,'page':last_page,'label':label,'sessions':len(ids),'sessionIds':sorted(ids)}
                                  for (kind,last_page,label),ids in sorted(last_actions.items(),key=lambda item:(-len(item[1]),item[0]))]
    return {'project':config,'lastEventAt':last_event_at,'total':{'clicks':sum(row['kind']=='click' for row in events),
        'visits':sum(row['kind']=='visit' for row in events),'sessions':len(sessions),'pages':len(pages),
        'lastAt':max([row['timestamp'] for row in events]+[row['lastAt'] for row in sessions],default=None)},
        'pages':pages,'sessions':sessions,'signals':signals,'funnel':funnel,
        'studies':studies(db),
        'findings':[json.loads(row[0]) for row in db.execute('SELECT value FROM live_findings WHERE study=? ORDER BY rowid DESC',(study,))],
        'reports':[json.loads(row[0]) for row in db.execute('SELECT value FROM live_reports WHERE study=? ORDER BY rowid DESC',(study,))]}


def text(value,limit=2000):
    if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError('Invalid text')
    return value.strip()


def get(db,path,query,identifier):
    study=identifier(query.get('study',[STUDY])[0])
    if path=='/api/project/studies':return {'studies':studies(db)}
    settings(db,study)
    if path=='/api/project':return summary(db,query.get('device',['all'])[0],study)
    if path=='/api/project/config':return settings(db,study)
    if path=='/api/project/reports':return {'reports':project_reports.catalog(db,settings(db,study)['id'])}
    if path=='/api/project/report':return project_reports.read(db,settings(db,study)['id'],identifier(query.get('id',[''])[0]))
    if path=='/api/project/criteria-catalog':return {'signals':success_criteria.catalog(db,settings(db,study)['id'])}
    if path=='/api/project/session':
        session=identifier(query.get('id',[''])[0])
        return {'id':session,'events':rows(db,session,study)}
    if path=='/api/project/frames':
        session=identifier(query.get('session',[''])[0])
        return {'frames':[{**dict(row),'target':json.loads(row['target'])} for row in db.execute('SELECT * FROM replay_frames WHERE study=? AND session=? ORDER BY seq',(study,session))]}
    return None


def post(db,path,data,identifier,pages,study=STUDY):
    if not isinstance(data,dict):raise ValueError('Expected object')
    if path=='/api/project/rounds':
        if data:raise ValueError('Invalid round request')
        current=settings(db,study)
        if current.get('roundClosedAt'):raise ValueError('Round already fixed')
        now=int(time.time()*1000)
        group=current.get('roundGroupId') or study
        number=current.get('roundNumber',1)
        base=current.get('roundBaseTitle') or current['studyTitle']
        next_id='study-'+str(uuid.uuid4())
        archived={**current,'roundGroupId':group,'roundNumber':number,'roundBaseTitle':base,
                  'roundClosedAt':now,'enabled':False}
        next_round={**current,'studyId':next_id,'studyTitle':f'{base[:100]} · раунд {number+1}',
                    'url':participant_url(current['url'],next_id),'enabled':False,
                    'roundGroupId':group,'roundNumber':number+1,'roundBaseTitle':base,'roundClosedAt':None}
        db.execute('UPDATE live_studies SET value=? WHERE id=?',(json.dumps(archived,ensure_ascii=False),study))
        db.execute("UPDATE recordings SET status='stopped' WHERE study=? AND status='uploading'",(study,))
        db.execute('INSERT INTO live_studies VALUES (?,?,?,?)',
                   (next_id,current['id'],json.dumps(next_round,ensure_ascii=False),now))
        return {'fixed':settings(db,study),'next':settings(db,next_id)}
    if path=='/api/project/studies':
        if set(data)-{'studyTitle','scenario'}:raise ValueError('Invalid study')
        key='study-'+str(uuid.uuid4())
        scenario=data.get('scenario','')
        if not isinstance(scenario,str) or len(scenario)>2000:raise ValueError('Invalid scenario')
        config={**DEFAULT,'studyId':key,'studyTitle':text(data.get('studyTitle'),120),'scenario':scenario.strip(),
                'mode':'scenario' if scenario.strip() else 'free','enabled':False,'funnel':[],'url':participant_url(DEFAULT['url'],key)}
        db.execute('INSERT INTO live_studies VALUES (?,?,?,?)',(key,DEFAULT['id'],json.dumps(config,ensure_ascii=False),int(time.time()*1000)))
        return settings(db,key)
    if path=='/api/project/task-events':
        config=settings(db,identifier(data.get('study','')))
        if config.get('roundClosedAt'):
            return {'accepted':identifier(data.get('id','')),'closed':True}
        return study_tasks.record(db,data,identifier,pages,config)
    if path=='/api/project/task-review':
        settings(db,study)
        return success_criteria.review(db,study,data)
    if path=='/api/project/config':
        if set(data)-{'studyTitle','scenario','tasks','mode','successCriterion','enabled','funnel','collectClicks','collectVisits','allowVideo','recordingMode'}:raise ValueError('Unknown configuration field')
        config=settings(db,study)
        if 'mode' in data:
            if data['mode'] not in ('free','scenario'):raise ValueError('Invalid study mode')
            config['mode']=data['mode']
        if 'successCriterion' in data:
            if not isinstance(data['successCriterion'],str) or data['successCriterion'] not in ('none','chat_message_sent','lead_created'):raise ValueError('Invalid success criterion')
            config['successCriterion']=data['successCriterion']
        if 'scenario' in data:
            if not isinstance(data['scenario'],str) or len(data['scenario'])>2000:raise ValueError('Invalid scenario')
            config['scenario']=data['scenario'].strip()
        if 'tasks' in data:
            if 'scenario' in data or 'successCriterion' in data:raise ValueError('Use tasks or legacy scenario fields, not both')
            config['tasks']=study_tasks.validate_tasks(data['tasks'],allow_incomplete=config['mode']=='free')
        elif 'scenario' in data or 'successCriterion' in data:
            tasks=config['tasks']
            if not tasks and config['scenario']:
                tasks=study_tasks.definitions({key:value for key,value in config.items() if key!='tasks'})
            elif tasks:
                tasks[0]={**tasks[0],'instruction':config['scenario'],'criterion':config['successCriterion']}
                if 'successCriterion' in data:
                    tasks[0].pop('verification',None)
                    tasks[0].pop('successDescription',None)
            config['tasks']=study_tasks.definitions({'tasks':tasks})
        if ('tasks' in data or 'mode' in data) and config['mode']=='scenario':
            if not config['tasks']:raise ValueError('Scenario needs at least one task')
            study_tasks.validate_tasks([{key:value for key,value in task.items() if key!='revision'} for task in config['tasks']])
            success_criteria.validate_connected(db,config['id'],config['tasks'])
        if config['tasks']:
            config['scenario']=config['tasks'][0]['instruction']
            config['successCriterion']=config['tasks'][0]['criterion']
        else:
            config['scenario']='';config['successCriterion']='none'
        if 'recordingMode' in data:
            if data['recordingMode'] not in ('video','screenshots'):raise ValueError('Invalid recording mode')
            config['recordingMode']=data['recordingMode']
        if 'studyTitle' in data:config['studyTitle']=text(data['studyTitle'],120)
        for key in ('enabled','collectClicks','collectVisits','allowVideo'):
            if key in data:
                if not isinstance(data[key],bool):raise ValueError('Invalid collection state')
                if key=='enabled' and data[key] and config.get('roundClosedAt'):raise ValueError('Fixed round cannot be restarted')
                config[key]=data[key]
        if 'funnel' in data:
            value=data['funnel']
            if not isinstance(value,list) or len(value)>8 or any(item not in pages or not item.startswith('leed-') for item in value):raise ValueError('Invalid funnel')
            config['funnel']=value
        db.execute('UPDATE live_studies SET value=? WHERE id=?',(json.dumps(config,ensure_ascii=False),study))
        return config
    if path=='/api/project/frames':
        fields={'id','study','session','seq','timestamp','page','snapshot','vw','vh','kind','label','target'}
        if set(data)!=fields:raise ValueError('Invalid frame')
        for key in ('id','study','session','snapshot'):identifier(data[key])
        settings(db,data['study'])
        if data['page'] not in pages or not data['page'].startswith('leed-'):raise ValueError('Invalid frame scope')
        if data['kind'] not in ('screen','click','change','scroll'):raise ValueError('Invalid frame kind')
        if not isinstance(data['label'],str) or len(data['label'])>160:raise ValueError('Invalid frame label')
        for key,low,high in [('seq',1,1e12),('timestamp',0,1e14),('vw',240,10000),('vh',200,10000)]:
            value=data[key]
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or int(value)!=value or not low<=value<=high:raise ValueError('Invalid frame measurement')
        target=data['target']
        if not isinstance(target,dict) or set(target) not in (set(),{'x','y'},{'x','y','rect'}):raise ValueError('Invalid frame target')
        if 'rect' in target and (not isinstance(target['rect'],list) or len(target['rect'])!=4):raise ValueError('Invalid frame rectangle')
        for value in ([target['x'],target['y']]+target.get('rect',[]) if target else []):
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=1:raise ValueError('Invalid target position')
        if round_closed(db,data['study']):return {'accepted':data['id'],'closed':True}
        data={**data,'target':json.dumps(target,sort_keys=True)}
        previous=db.execute('SELECT * FROM replay_frames WHERE id=? OR (study=? AND session=? AND seq=?)',(data['id'],data['study'],data['session'],data['seq'])).fetchone()
        if previous and any(previous[key]!=value for key,value in data.items()):raise ValueError('Conflicting frame')
        db.execute('INSERT OR IGNORE INTO replay_frames ('+','.join(data)+') VALUES ('+','.join('?' for _ in data)+')',tuple(data.values()))
        return {'accepted':data['id']}
    if path=='/api/project/visit':
        if set(data)!={'id','study','session','page','timestamp','vw','vh','context'}:raise ValueError('Invalid visit')
        for key in ('id','study','session'):identifier(data[key])
        settings(db,data['study'])
        if data['page'] not in pages or not data['page'].startswith('leed-'):raise ValueError('Invalid page')
        for key,low,high in [('timestamp',0,1e14),('vw',240,10000),('vh',200,10000)]:
            value=data[key]
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low<=value<=high or int(value)!=value:raise ValueError('Invalid visit measurement')
        context=data['context']
        if not isinstance(context,dict) or not {'signature','scrolls'}<=set(context) or set(context)-{'signature','scrolls','snapshot'}:raise ValueError('Invalid visit context')
        if not isinstance(context['signature'],str) or not re.fullmatch('[a-f0-9]{16}',context['signature']):raise ValueError('Invalid signature')
        if not isinstance(context['scrolls'],list) or len(context['scrolls'])>100:raise ValueError('Invalid scrolls')
        for scroll in context['scrolls']:
            if not isinstance(scroll,list) or len(scroll)!=3:raise ValueError('Invalid scroll')
            for index,value in enumerate(scroll):
                if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or int(value)!=value or not (-1 if index==0 else -10000)<=value<=100000:raise ValueError('Invalid scroll')
        if 'snapshot' in context:identifier(context['snapshot'])
        if round_closed(db,data['study']):return {'accepted':data['id'],'closed':True}
        encoded={**data,'context':json.dumps(context,sort_keys=True)}
        previous=db.execute('SELECT * FROM visits WHERE id=?',(data['id'],)).fetchone()
        if previous and any(previous[key]!=value for key,value in encoded.items()):raise ValueError('Conflicting visit')
        db.execute('INSERT OR IGNORE INTO visits ('+','.join(encoded)+') VALUES ('+','.join('?' for _ in encoded)+')',tuple(encoded.values()))
        return {'accepted':data['id']}
    if path=='/api/project/findings':
        settings(db,study)
        if set(data)-{'id','title','observation','session','page','timestamp','resolved'}:raise ValueError('Invalid finding')
        key=identifier(data['id']) if data.get('id') else str(uuid.uuid4())
        previous=db.execute('SELECT value FROM live_findings WHERE id=?',(key,)).fetchone()
        owner=db.execute('SELECT study FROM live_findings WHERE id=?',(key,)).fetchone()
        if owner and owner[0]!=study:raise ValueError('Finding belongs to another study')
        result={**(json.loads(previous[0]) if previous else {}),**data,'id':key}
        result['title']=text(result.get('title'),160);result['observation']=text(result.get('observation'))
        if result.get('session'):identifier(result['session'])
        if result.get('page') and result['page'] not in pages:raise ValueError('Invalid page')
        if 'resolved' in result and not isinstance(result['resolved'],bool):raise ValueError('Invalid finding status')
        if 'timestamp' in result:
            value=result['timestamp']
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=1e14:raise ValueError('Invalid finding timestamp')
        result.setdefault('createdAt',int(time.time()*1000))
        db.execute('INSERT OR REPLACE INTO live_findings (id,value,study) VALUES (?,?,?)',(key,json.dumps(result,ensure_ascii=False),study))
        return result
    if path=='/api/project/reports':
        options=project_reports.options(data)
        device=data.get('device','all')
        if device not in ('all','desktop','mobile'):raise ValueError('Invalid device')
        result=summary(db,device,study);result.pop('reports');result.pop('studies')
        result.update(id=str(uuid.uuid4()),createdAt=int(time.time()*1000),device=device,sections=options['sections'],title=options['title'] or 'Отчёт · '+result['project']['studyTitle'])
        db.execute('INSERT INTO live_reports (id,value,study) VALUES (?,?,?)',(result['id'],json.dumps(result,ensure_ascii=False),study))
        return result
    return None
