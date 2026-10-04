"""Prepare idempotent finishing patches, navigation and verification payloads."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/complete-wireframes'
PRE="const p=await figma.getNodeByIdAsync('20:2');await figma.setCurrentPageAsync(p);\n"
PATCH=r'''
const frames=p.findAll(n=>n.type==='FRAME'&&n.parent.type==='SECTION');
const changed=[],created=[];
await figma.loadFontAsync({family:'Inter',style:'Regular'});
for(const f of frames){
 for(const tx of f.findAllWithCriteria({types:['TEXT']}))for(const s of tx.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 if(['CriteriaURL','CriteriaButton','ResultsEmpty'].includes(f.name))for(const tx of f.findAllWithCriteria({types:['TEXT']}))if(tx.characters.includes('Покупка в интернет-магазине')){tx.characters=tx.characters.replaceAll('Покупка в интернет-магазине','Навигация каталога');changed.push(tx.id);}
 for(const row of f.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Table')&&n.layoutMode==='HORIZONTAL')){row.counterAxisAlignItems='CENTER';changed.push(row.id);}
 if(f.name==='ParticipantSession')for(const tx of f.findAllWithCriteria({types:['TEXT']}))if(tx.characters.includes('Это не заменяет проверку критерия успеха.')){tx.characters=tx.characters.replace('Это не заменяет проверку критерия успеха.','Отметьте, удалось ли выполнить задание, чтобы перейти дальше.');changed.push(tx.id);}
 if(f.width===390){
  const meta=META.find(m=>m.name===f.name);
  for(const tx of f.parent.children.filter(n=>n.type==='TEXT'&&n.x===f.x)){
   for(const s of tx.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
   if(tx.name==='ScreenTitle'){tx.fontSize=18;tx.y=f.y-120;}
   if(tx.name==='ScreenAnnotation'){tx.fontSize=11;tx.characters=meta.kind+' · '+meta.trigger;tx.y=f.y-60;}
   changed.push(tx.id);
  }
 }
 if(['Replay','ReplayIncomplete'].includes(f.name)){
  const timeline=f.findAll(n=>n.type==='FRAME'&&n.name==='Timeline')[0];
  const old=timeline.children.find(n=>n.type==='TEXT'&&n.characters.startsWith('00:00'));
  if(old){
   const ticks=figma.createAutoLayout('HORIZONTAL');ticks.name='TimelineTicks';ticks.resize(old.width,old.height);ticks.primaryAxisSizingMode='FIXED';ticks.counterAxisSizingMode='FIXED';ticks.fills=[];
   timeline.insertChild(timeline.children.indexOf(old),ticks);created.push(ticks.id);
   for(const [seconds,label] of [[0,'00:00'],[48,'00:48'],[96,'01:36'],[144,'02:24'],[192,'03:12'],[272,'04:32']]){
    const tx=figma.createText();ticks.appendChild(tx);tx.fontName={family:'Inter',style:'Regular'};tx.fontSize=14;tx.characters=label;tx.resize(44,old.height);tx.textAutoResize='HEIGHT';tx.layoutPositioning='ABSOLUTE';tx.x=Math.max(0,Math.min(ticks.width-44,ticks.width*seconds/272-22));tx.y=0;created.push(tx.id);
   }
   changed.push(old.id,timeline.id);old.remove();
  }
 }
}
const oldInfo={ResultsOverview:'Страница · Результаты исследования: сводка и сценарии',Heatmaps:'Страница · Обзор результатов → Тепловая карта',Funnel:'Страница · Результаты сценария → Воронка',Replay:'Страница · Участник / сигнал → Запись сессии',SuccessCriteria:'Страница настройки · Критерий: последовательность действий',Projects:'Модалка по центру · Все проекты → Создать проект',Studies:'Страница · Все проекты → Открыть проект',StudySetup:'Страница · Настройка исследования; подключение — постоянный блок',Launch:'Страница · Проверка и запуск; приглашение — постоянный блок'};
for(const f of frames.filter(f=>oldInfo[f.name]))if(!f.parent.children.some(n=>n.name==='SurfaceNote-'+f.name)){
 const tx=figma.createText();f.parent.appendChild(tx);tx.name='SurfaceNote-'+f.name;tx.fontName={family:'Inter',style:'Regular'};tx.fontSize=14;tx.characters=oldInfo[f.name];tx.resize(f.width,22);tx.textAutoResize='HEIGHT';tx.x=f.x;tx.y=f.y-28;created.push(tx.id);
}
return {createdNodeIds:created,mutatedNodeIds:changed};
'''

# Only connect transitions whose displayed project/study context is consistent.
ROUTES=[
 ('Login','Продолжить вход','ProjectsDefault'),
 ('ProjectsDefault','Создать проект','Projects'),('ProjectsEmpty','Создать проект','Projects'),
 ('Projects','Отмена','ProjectsDefault'),('Projects','×','ProjectsDefault'),('Projects','Создать проект','StudiesEmpty',-1),
 ('ProjectsDefault','Открыть','Studies',0),('StudiesEmpty','Создать исследование','StudySetupBlank'),
 ('Studies','Продолжить настройку','StudySetup'),
 ('TaskEditor','Выбрать задание из списка','TaskPicker'),('TaskEditor','Настроить критерий','CriteriaURL'),
 ('TaskEditor','Сохранить задание','StudySetup'),('TaskEditor','Отмена','StudySetup'),
 ('TaskPicker','Добавить задание','TaskEditor'),('TaskPicker','Отмена','TaskEditor',-1),('TaskPicker','×','TaskEditor'),
 ('CriteriaURL','Целевая кнопка','CriteriaButton'),('CriteriaButton','Целевая страница','CriteriaURL'),
 ('CriteriaURL','Сохранить критерий','TaskEditor'),('CriteriaURL','Вернуться к заданию','TaskEditor'),
 ('CriteriaButton','Вернуться к заданию','StudySetup'),('CriteriaButton','Сохранить критерий','StudySetup'),
 ('Launch','Запустить и создать ссылку','LaunchActive'),('LaunchError','Повторить запуск','LaunchActive'),
 ('LaunchError','Вернуться к настройке','StudySetup'),('LaunchActive','Открыть обзор результатов','ResultsEmpty'),
 ('Report','Сформировать PDF','ReportGenerating'),('ReportReady','Изменить состав отчёта','Report'),
 ('Heatmaps','Первый клик','HeatmapsFirstClick'),('HeatmapsFirstClick','Все клики','Heatmaps'),
]
LINKS=r'''
const frames=p.findAll(n=>n.type==='FRAME'&&n.parent.type==='SECTION');const byName=Object.fromEntries(frames.map(f=>[f.name,f]));
const changed=[],links=[],missing=[];
async function bind(node,dest){await node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:dest.id,navigation:'NAVIGATE',transition:null}]}]);changed.push(node.id);links.push({nodeId:node.id,from:node.name,to:dest.name});}
const nav={'Все проекты':'ProjectsDefault','Исследования проекта':'Studies','Обзор результатов':'ResultsOverview','Тепловая карта':'Heatmaps','Воронка':'Funnel','Участники':'Participants','Сигналы затруднений':'Signals','Отчёт PDF':'Report'};
for(const f of frames){
 const study=f.findAll(n=>n.type==='FRAME'&&n.name==='StudyContext')[0];const studyText=study?study.findAll(n=>n.type==='TEXT').map(n=>n.characters).join(' '):'';
 const project=f.findAll(n=>n.type==='FRAME'&&n.name==='ProjectContext')[0];const service=project&&project.findAll(n=>n.type==='TEXT'&&n.characters==='Сервис доставки').length;
 for(const item of f.findAll(n=>n.type==='FRAME'&&n.name==='NavigationItem')){
  const text=item.findAll(n=>n.type==='TEXT')[0].characters.replace(/^•\s*/, '');let target=nav[text];
  if(text==='Исследования проекта'&&service)target='StudiesEmpty';
  if(text==='Все проекты'||text==='Исследования проекта'){}else if(studyText.includes('Навигация каталога'))target={'Настройка исследования':'StudySetup','Проверка и запуск':'Launch','Обзор результатов':'ResultsEmpty'}[text];
  else if(!studyText.includes('Покупка в интернет-магазине'))target=undefined;
  if(target&&target!==f.name)await bind(item,byName[target]);
 }
 for(const tx of f.findAll(n=>n.type==='TEXT'&&n.parent.name==='Header'&&n.characters==='Все проекты'))await bind(tx,byName.ProjectsDefault);
}
for(const [name,label,target,idx=0] of ROUTES){
 const f=byName[name],matches=f.findAll(n=>n.type==='TEXT'&&n.characters===label&&!['Header','NavigationItem','NavigationItemDisabled'].includes(n.parent.name));const tx=matches.at(idx);
 if(!tx){missing.push({name,label});continue;}await bind(tx.parent.name==='Action'?tx.parent:tx,byName[target]);
}
return {mutatedNodeIds:changed,links,missing};
'''
AUDIT=r'''
const frames=p.findAll(n=>n.type==='FRAME'&&n.parent.type==='SECTION');const overflow=[],annotations=[];
for(const f of frames)for(const parent of [f,...f.findAllWithCriteria({types:['FRAME']})])for(const c of parent.children)if(c.visible&&(c.x<-.5||c.y<-.5||c.x+c.width>parent.width+1||c.y+c.height>parent.height+1))overflow.push({frame:f.name,parent:parent.name,node:c.id,name:c.name});
for(const f of frames)for(const tx of f.parent.children.filter(n=>n.type==='TEXT'&&n.x===f.x&&n.y<f.y&&n.y>f.y-125))if(tx.y+tx.height>f.y)annotations.push({frame:f.name,id:tx.id});
return {frames:frames.map(f=>({name:f.name,id:f.id,width:f.width,height:f.height,sectionId:f.parent.id,navCount:f.findAll(n=>n.type==='FRAME'&&n.name.startsWith('NavigationItem')).length})),overflow,annotationOverflow:annotations};
'''
def main():
    meta=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    (OUT/'final-polish.js').write_text(PRE+'const META='+json.dumps(meta,ensure_ascii=False)+';\n'+PATCH,encoding='utf-8')
    (OUT/'prototype-links.js').write_text(PRE+'const ROUTES='+json.dumps(ROUTES,ensure_ascii=False)+';\n'+LINKS,encoding='utf-8')
    (OUT/'audit.js').write_text(PRE+AUDIT,encoding='utf-8')
    print('Prepared final-polish, prototype-links, audit.')
if __name__=='__main__':main()
