"""One-time study creation explicitly requested by the workspace owner.

Creates no participants or outcomes, never edits another study, and respects deletion.
The cloud schema marker prevents later cold starts from undoing researcher edits.
"""
import json
import time
import live_project
import study_task_plan
import success_criteria

STUDY_ID='biletberu-retest-2026-10-15'
STUDY_TITLE='Повторный тест · 6 заданий · 15.10.2026'
TASKS=[
    ('nearby','Найти активности рядом с событием','Открыта активность рядом с выбранным событием.','event','nearby_activity_opened'),
    ('favourite','Добавить активность в избранное','Активность появилась в избранном.','event','activity_favourited'),
    ('purchase','Купить 2 билета на спектакль','Открыт экран успешной оплаты, в любом его варианте.','screen','bb-done'),
    ('favourites','Найти раздел «Избранное»','Открыт раздел «Избранное».','screen','bb-favourites'),
    ('planning','Найти функцию «Куда пойдём?»','Открыт раздел «Куда пойдём?», в том числе без билетов.','event','planning_opened'),
    ('plan','Построить план из избранного','В план дня добавлено место из избранного.','event','favourite_added_to_plan'),
]


def create_once(db):
    if db.execute('SELECT 1 FROM deleted_studies WHERE id=?',(STUDY_ID,)).fetchone():return False
    if db.execute('SELECT 1 FROM live_studies WHERE id=?',(STUDY_ID,)).fetchone():return False
    tasks=study_task_plan.validate_tasks([
        dict(id=key,title=title,instruction=title,criterion='custom',successDescription=description,
             verification=dict(method='automatic',type=kind,value=value,page=value if kind=='screen' else ''))
        for key,title,description,kind,value in TASKS
    ])
    success_criteria.validate_connected(db,live_project.DEFAULT['id'],tasks)
    config={**live_project.DEFAULT,'studyId':STUDY_ID,'studyTitle':STUDY_TITLE,'enabled':False,
            'url':live_project.participant_url(live_project.DEFAULT['url'],STUDY_ID),'mode':'scenario',
            'scenario':tasks[0]['instruction'],'successCriterion':'custom','tasks':tasks,
            'collectClicks':True,'collectVisits':True,'allowVideo':False,'recordingMode':'screenshots'}
    db.execute('INSERT INTO live_studies VALUES (?,?,?,?)',
               (STUDY_ID,config['id'],json.dumps(config,ensure_ascii=False),int(time.time()*1000)))
    saved=live_project.settings(db,STUDY_ID)
    if saved['enabled'] or [task['instruction'] for task in saved['tasks']]!=[task[1] for task in TASKS]:
        raise ValueError('Requested study did not retain the exact task instructions')
    return True


def use_payment_success_screen(db):
    """Apply the owner's revised criterion, retaining labels and historical attempts."""
    row=db.execute('SELECT value FROM live_studies WHERE id=?',(STUDY_ID,)).fetchone()
    if not row:return False
    config=json.loads(row[0])
    task=next((task for task in config.get('tasks',[]) if task['id']=='purchase' or task['title']=='Купить 2 билета на спектакль'),None)
    if task is None:return False
    task['successDescription']='Открыт экран успешной оплаты, в любом его варианте.'
    task['criterion']='custom'
    task['verification']={'method':'automatic','type':'screen','value':'bb-done','page':'bb-done'}
    task['revision']=study_task_plan.version(task)
    success_criteria.validate_connected(db,config['id'],[task])
    db.execute('UPDATE live_studies SET value=? WHERE id=?',(json.dumps(config,ensure_ascii=False),STUDY_ID))
    return True
