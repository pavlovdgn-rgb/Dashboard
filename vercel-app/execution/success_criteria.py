"""Custom success descriptions, immutable checks and explicit researcher reviews."""
import json
import time
from mobile_pages import MOBILE_SCREENS

TYPES={'screen','element','event'}

def initialize(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS task_criteria_snapshots (
        study TEXT, session TEXT, taskId TEXT, description TEXT NOT NULL,
        verification TEXT NOT NULL, reviewedAt INTEGER, PRIMARY KEY(study,session,taskId));
      CREATE TABLE IF NOT EXISTS prototype_success_signals (
        project TEXT, type TEXT, value TEXT, page TEXT, label TEXT, lastAt INTEGER,
        PRIMARY KEY(project,type,value,page));
    ''')

def validate(task,allow_incomplete=False):
    if 'successDescription' in task and (not isinstance(task['successDescription'],str) or len(task['successDescription'])>2000):raise ValueError('Invalid success description')
    if 'verification' not in task:
        if task['criterion']=='custom':raise ValueError('Custom criterion needs verification')
        return
    description=task.get('successDescription','')
    if not isinstance(description,str) or len(description)>2000 or (not allow_incomplete and not description.strip()):raise ValueError('Describe success')
    check=task['verification']
    if not isinstance(check,dict):raise ValueError('Invalid verification')
    if check.get('method')=='manual':
        if set(check)!={'method'}:raise ValueError('Invalid manual check')
    elif check.get('method')=='automatic':
        if set(check)!={'method','type','value','page'} or check['type'] not in TYPES:raise ValueError('Invalid automatic check')
        if any(not isinstance(check[k],str) or len(check[k])>200 for k in ('value','page')):raise ValueError('Invalid check target')
        if not allow_incomplete and not check['value'].strip():raise ValueError('Choose a verified event')
    else:raise ValueError('Invalid verification method')
    if task['criterion']!='custom':raise ValueError('Unexpected legacy criterion with verification')

def catalog(db,project):
    result=[dict(row) for row in db.execute('SELECT type,value,page,label,lastAt FROM prototype_success_signals WHERE project=? ORDER BY type,label',(project,))]
    if project=='biletberu-mobile':
        observed={(signal['type'],signal['value'],signal['page']) for signal in result}
        for name,(_path,label) in MOBILE_SCREENS.items():
            page='bb-'+name
            if ('screen',page,page) not in observed:
                result.append({'type':'screen','value':page,'page':page,'label':label,'lastAt':0})
        # Earlier rounds stored clicks for the heatmap before the success-signal catalog existed.
        # Reuse their stable page/target pairs without changing or reopening those rounds.
        for row in db.execute('''SELECT c.page,c.target,MAX(c.context) AS context,MAX(c.timestamp) AS lastAt
            FROM clicks AS c JOIN live_studies AS s ON s.id=c.study
            WHERE s.project_id=? AND c.version='biletberu-v1' AND c.page LIKE 'bb-%'
            GROUP BY c.page,c.target ORDER BY lastAt DESC LIMIT 500''',(project,)):
            key=('element',row['target'],row['page'])
            if key in observed:continue
            try:label=json.loads(row['context'] or '{}').get('element',{}).get('label') or 'Элемент'
            except (AttributeError,TypeError,ValueError):label='Элемент'
            result.append({'type':'element','value':row['target'],'page':row['page'],'label':label,'lastAt':row['lastAt']})
    # Old confirmed domain actions are valid connection evidence, without rewriting history.
    for row in db.execute("SELECT kind,MAX(timestamp) AS lastAt FROM study_task_events JOIN live_studies ON live_studies.id=study_task_events.study WHERE project_id=? AND kind IN ('chat_message_sent','lead_created') GROUP BY kind",(project,)):
        if not any(s['type']=='event' and s['value']==row['kind'] for s in result):result.append({'type':'event','value':row['kind'],'page':'','label':{'chat_message_sent':'Отправлено сообщение в чат','lead_created':'Создан новый лид'}[row['kind']],'lastAt':row['lastAt']})
    return result

def validate_connected(db,project,tasks):
    known={(s['type'],s['value'],s['page']) for s in catalog(db,project)}
    for task in tasks:
        check=task.get('verification',{})
        if check.get('method')=='automatic' and (check['type'],check['value'],check['page']) not in known:
            raise ValueError('Event has not been observed in this prototype')

def snapshot(db,data,task):
    if 'verification' in task:
        db.execute('INSERT INTO task_criteria_snapshots VALUES (?,?,?,?,?,NULL)',(data['study'],data['session'],task['id'],task['successDescription'],json.dumps(task['verification'],ensure_ascii=False)))

def details(db,study,session,task):
    row=db.execute('SELECT * FROM task_criteria_snapshots WHERE study=? AND session=? AND taskId=?',(study,session,task)).fetchone()
    if not row:return {}
    return {'successDescription':row['description'],'verification':json.loads(row['verification']),'reviewedAt':row['reviewedAt'],'criterionLabel':row['description']}

def signal(data):
    kind=data['kind']
    if kind=='screen_visited':return ('screen',data['page'],data['page'])
    if kind=='element_clicked':return ('element',data.get('value',''),data['page'])
    if kind in ('chat_message_sent','lead_created'):return ('event',kind,'')
    if kind=='prototype_event':return ('event',data.get('value',''),'')
    return None

def observe(db,project,data):
    event=signal(data)
    if not event:return
    kind,value,page=event
    if not value:raise ValueError('Missing event target')
    label=data.get('label') or {'chat_message_sent':'Отправлено сообщение в чат','lead_created':'Создан новый лид'}.get(value,value)
    db.execute('INSERT INTO prototype_success_signals VALUES (?,?,?,?,?,?) ON CONFLICT(project,type,value,page) DO UPDATE SET label=excluded.label,lastAt=MAX(lastAt,excluded.lastAt)',(project,kind,value,page,label,data['timestamp']))

def matches(run,data):
    check=run.get('verification',{})
    return check.get('method')=='automatic' and signal(data)==(check.get('type'),check.get('value'),check.get('page'))

def review(db,study,data):
    if set(data)!={'session','taskId','status'} or data['status'] not in ('succeeded','failed','indeterminate'):raise ValueError('Invalid review')
    if any(not isinstance(data[key],str) or not data[key] or len(data[key])>120 for key in ('session','taskId')):raise ValueError('Invalid review target')
    args=(study,data['session'],data['taskId'])
    row=db.execute('SELECT finishedAt FROM study_task_attempts WHERE study=? AND session=? AND taskId=?',args).fetchone()
    check=details(db,*args).get('verification',{})
    if not row or row['finishedAt'] is None or check.get('method')!='manual':raise ValueError('Only completed manually assessed tasks can be reviewed')
    now=int(time.time()*1000)
    db.execute('UPDATE study_task_attempts SET status=?,completedAt=?,updatedAt=? WHERE study=? AND session=? AND taskId=?',(data['status'],now if data['status']=='succeeded' else None,now,*args))
    db.execute('UPDATE task_criteria_snapshots SET reviewedAt=? WHERE study=? AND session=? AND taskId=?',(now,*args))
    return {'saved':True}
