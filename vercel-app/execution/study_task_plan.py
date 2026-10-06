"""Versioned task lists and sequential attempts. Existing session plans are immutable."""
import hashlib
import json
import math
import re
import success_criteria

CRITERIA={'none':'Без автоматической проверки','chat_message_sent':'Отправлено сообщение в чат','lead_created':'Создан новый лид','custom':'Свой критерий'}
LEGACY_ID='legacy-task'

def version(task):
    payload={key:task[key] for key in ('title','instruction','criterion')}
    payload.update({key:task[key] for key in ('successDescription','verification') if key in task})
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]

def definitions(config):
    """Normalize legacy single-task settings without rewriting original saved configuration."""
    if 'tasks' in config:
        return [{**task,'revision':version(task)} for task in config['tasks']]
    if not config.get('scenario'):return []
    task={'id':LEGACY_ID,'title':'Задание 1','instruction':config['scenario'],'criterion':config.get('successCriterion','none')}
    return [{**task,'revision':version(task)}]

def validate_tasks(value,allow_incomplete=False):
    if not isinstance(value,list) or len(value)>20:raise ValueError('Expected up to 20 tasks')
    result=[];seen=set()
    for task in value:
        if not isinstance(task,dict) or not {'id','title','instruction','criterion'}<=set(task) or set(task)-{'id','title','instruction','criterion','successDescription','verification'}:raise ValueError('Invalid task definition')
        if not isinstance(task['id'],str) or not re.fullmatch(r'[a-zA-Z0-9_.:-]{1,120}',task['id']) or task['id'] in seen:raise ValueError('Invalid or duplicate task ID')
        for key,limit in (('title',120),('instruction',2000)):
            if not isinstance(task[key],str) or (not allow_incomplete and not task[key].strip()) or len(task[key])>limit:raise ValueError('Invalid task '+key)
        if not isinstance(task['criterion'],str) or task['criterion'] not in CRITERIA:raise ValueError('Invalid task criterion')
        success_criteria.validate(task,allow_incomplete)
        clean={**task,'title':task['title'].strip(),'instruction':task['instruction'].strip()}
        result.append({**clean,'revision':version(clean)});seen.add(task['id'])
    return result

def initialize(db):
    success_criteria.initialize(db)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS study_task_sessions (
        study TEXT NOT NULL, session TEXT NOT NULL, startedAt INTEGER NOT NULL,
        vw INTEGER NOT NULL, vh INTEGER NOT NULL, PRIMARY KEY(study,session));
      CREATE TABLE IF NOT EXISTS study_task_attempts (
        study TEXT NOT NULL, session TEXT NOT NULL, taskId TEXT NOT NULL, revision TEXT NOT NULL,
        ordinal INTEGER NOT NULL, title TEXT NOT NULL, scenario TEXT NOT NULL, criterion TEXT NOT NULL,
        status TEXT NOT NULL, startedAt INTEGER, updatedAt INTEGER NOT NULL, completedAt INTEGER,
        finishedAt INTEGER, PRIMARY KEY(study,session,taskId));
      CREATE INDEX IF NOT EXISTS task_attempts_study ON study_task_attempts(study,session,ordinal);
    ''')
    if 'taskId' not in {row[1] for row in db.execute('PRAGMA table_info(study_task_events)')}:
        db.execute("ALTER TABLE study_task_events ADD COLUMN taskId TEXT NOT NULL DEFAULT ''")
    for column in ('value','label'):
        if column not in {row[1] for row in db.execute('PRAGMA table_info(study_task_events)')}:
            db.execute('ALTER TABLE study_task_events ADD COLUMN '+column+" TEXT NOT NULL DEFAULT ''")
    # Idempotent migration: old tables remain intact; later updates never get overwritten.
    for row in db.execute('SELECT * FROM study_task_runs'):
        db.execute('INSERT OR IGNORE INTO study_task_sessions VALUES (?,?,?,?,?)',(row['study'],row['session'],row['startedAt'],row['vw'],row['vh']))
        task={'title':'Задание 1','instruction':row['scenario'],'criterion':row['criterion']}
        db.execute('INSERT OR IGNORE INTO study_task_attempts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   (row['study'],row['session'],LEGACY_ID,version(task),0,task['title'],row['scenario'],row['criterion'],row['status'],row['startedAt'],row['updatedAt'],row['completedAt'],row['finishedAt']))

def outcome(row):
    return {**dict(row),'criterionLabel':CRITERIA[row['criterion']]}

def get_run(db,study,session):
    tasks=[{**outcome(row),**success_criteria.details(db,study,session,row['taskId'])} for row in db.execute('SELECT * FROM study_task_attempts WHERE study=? AND session=? ORDER BY ordinal',(study,session))]
    if not tasks:return None
    active=next((task for task in tasks if task['finishedAt'] is None),None)
    # Keep the former top-level fields for older single-task clients and saved reports.
    return {**(active or tasks[-1]),'tasks':tasks,'activeTaskId':active['taskId'] if active else None,
            'finishedAt':None if active else max(task['finishedAt'] for task in tasks),
            'totalTasks':len(tasks),'succeededTasks':sum(task['status']=='succeeded' for task in tasks),
            'finishedTasks':sum(task['finishedAt'] is not None for task in tasks)}

def start_plan(db,data,config):
    tasks=definitions(config)
    if config['mode']!='scenario' or not tasks:return False
    db.execute('INSERT INTO study_task_sessions VALUES (?,?,?,?,?)',(data['study'],data['session'],data['timestamp'],data['vw'],data['vh']))
    for ordinal,task in enumerate(tasks):
        success_criteria.snapshot(db,data,task)
        state=('unassessed' if task['criterion']=='none' else 'pending') if ordinal==0 else 'not_started'
        db.execute('INSERT INTO study_task_attempts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   (data['study'],data['session'],task['id'],task['revision'],ordinal,task['title'],task['instruction'],task['criterion'],state,data['timestamp'] if ordinal==0 else None,data['timestamp'],None,None))
    return True

def record(db,data,identifier,pages,config):
    required={'id','study','session','kind','timestamp','page','vw','vh'}
    if not required<=set(data) or set(data)-required-{'taskId','value','label'}:raise ValueError('Invalid task event')
    data={**data,'taskId':data.get('taskId','')}
    for key in ('id','study','session'):identifier(data[key])
    if not isinstance(data['taskId'],str):raise ValueError('Invalid task ID')
    if data['taskId']:identifier(data['taskId'])
    if data['kind'] not in ('started','finished','chat_message_sent','lead_created','screen_visited','element_clicked','prototype_event'):raise ValueError('Invalid task action')
    for key in ('value','label'):
        if key in data and (not isinstance(data[key],str) or len(data[key])>200):raise ValueError('Invalid event target')
    if data['page'] not in pages or not data['page'].startswith('leed-'):raise ValueError('Invalid task page')
    for key,low,high in [('timestamp',0,1e14),('vw',240,10000),('vh',200,10000)]:
        value=data[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or int(value)!=value or not low<=value<=high:raise ValueError('Invalid task measurement')
    previous=db.execute('SELECT * FROM study_task_events WHERE id=?',(data['id'],)).fetchone()
    if previous:
        if any(previous[key]!=value for key,value in data.items()):raise ValueError('Conflicting task event')
        return {'accepted':data['id'],'run':get_run(db,data['study'],data['session'])}
    if not config['enabled']:return {'paused':True}
    success_criteria.observe(db,config['id'],data)
    run=get_run(db,data['study'],data['session'])
    if not run:
        if not start_plan(db,data,config):return {'ignored':True,'run':None}
        run=get_run(db,data['study'],data['session'])
    if data['kind'] in ('screen_visited','element_clicked','prototype_event') and not data['taskId']:
        return {'accepted':data['id'],'run':run}
    if not run['activeTaskId'] and data['kind'] in ('chat_message_sent','lead_created'):
        return {'accepted':data['id'],'run':run}
    if data['kind']!='started' and not data['taskId'] and len(run['tasks'])>1:
        raise ValueError('Task ID required for multi-task sessions; reload the participant tab')
    db.execute('INSERT INTO study_task_events ('+','.join(data)+') VALUES ('+','.join('?' for _ in data)+')',tuple(data.values()))
    task_id=data['taskId'] or run['activeTaskId']
    # Events queued for a completed task cannot satisfy a later task with the same criterion.
    if data['kind']!='started' and task_id and task_id==run['activeTaskId']:
        args=(data['study'],data['session'],task_id)
        automatic=run.get('verification',{}).get('method')=='automatic'
        completed=False
        if data['kind']==run['criterion'] or success_criteria.matches(run,data):
            db.execute("UPDATE study_task_attempts SET status='succeeded',completedAt=COALESCE(completedAt,?),updatedAt=? WHERE study=? AND session=? AND taskId=?",
                       (data['timestamp'],data['timestamp'],*args))
            if automatic:
                db.execute('UPDATE study_task_attempts SET finishedAt=? WHERE study=? AND session=? AND taskId=?',(data['timestamp'],*args))
                completed=True
        elif data['kind']=='finished':
            db.execute("UPDATE study_task_attempts SET status=CASE WHEN status='pending' THEN 'failed' ELSE status END,finishedAt=?,updatedAt=? WHERE study=? AND session=? AND taskId=?",
                       (data['timestamp'],data['timestamp'],*args))
            if run.get('verification',{}).get('method')=='manual':
                db.execute("UPDATE study_task_attempts SET status='needs_review' WHERE study=? AND session=? AND taskId=?",args)
            completed=True
        if completed:
            following=next((task for task in run['tasks'] if task['ordinal']>run['ordinal']),None)
            if following:
                db.execute("UPDATE study_task_attempts SET status=CASE WHEN criterion='none' THEN 'unassessed' ELSE 'pending' END,startedAt=?,updatedAt=? WHERE study=? AND session=? AND taskId=?",
                           (data['timestamp'],data['timestamp'],data['study'],data['session'],following['taskId']))
    return {'accepted':data['id'],'run':get_run(db,data['study'],data['session'])}

def enrich(db,sessions,study,device):
    where='study=?'+(' AND vw<768' if device=='mobile' else ' AND vw>=768' if device=='desktop' else '')
    by_id={s['id']:s for s in sessions}
    for row in db.execute('SELECT * FROM study_task_sessions WHERE '+where,(study,)):
        run=get_run(db,study,row['session'])
        if not run:continue
        # Researcher reviews update an assessment, not the participant's last activity.
        last=max((task['finishedAt'] or task['startedAt'] or 0) if task.get('reviewedAt') else task['updatedAt'] for task in run['tasks'])
        item=by_id.get(row['session'])
        if item is None:
            item={'id':row['session'],'startedAt':row['startedAt'],'lastAt':last,'clicks':0,'visits':0,'pages':[],'signals':0,'snapshots':0}
            sessions.append(item)
        item['task']=run
        item['lastAt']=max(item['lastAt'],last)
