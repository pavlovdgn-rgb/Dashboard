import {SummaryMetric} from '../components';
import {useWireRoute} from '../screens/useWireRoute';
import {pageLabels} from '../heatmap/types';
import type {LiveSummary} from './types';
import {sessionTasks,studyTasks} from './taskMetrics';
import s from './LiveWorkspace.module.css';

export function OverviewMetrics({data}:{data:LiveSummary}){
 const {navigate}=useWireRoute();
 const tasks=studyTasks(data.project),assigned=data.sessions.filter(session=>sessionTasks(session.task).length);
 const complete=assigned.filter(session=>sessionTasks(session.task).every(task=>task.status==='succeeded')).length;
 const recorded=data.sessions.filter(session=>(session.recordings||0)>0||(session.frames||0)>0).length;
 const clicking=data.sessions.filter(session=>session.clicks>0).length;
 const affected=new Set(data.signals.map(signal=>signal.session)).size;
 const top=[...data.pages].sort((a,b)=>b.sessions-a.sessions)[0];
 const scenario=data.project.mode==='scenario';
 return <div className={s.overviewMetrics} aria-label="Сводка исследования">
  <SummaryMetric State="Ready" Label="Сессии" Value={String(data.total.sessions)} Hint="Посещения в отдельных вкладках, не уникальные люди" Detail={`${clicking} с кликами\n${recorded} с видео или снимками`} ShowLink LinkLabel="Посмотреть сессии" onClick={()=>navigate({screen:'participants',item:''})}/>
  {scenario?<SummaryMetric State="Ready" Label="Задания" Value={String(tasks.length)} Hint="В текущем сценарии исследования" Detail={tasks.length?tasks.slice(0,2).map(task=>task.title).join('\n')+(tasks.length>2?`\nИ ещё ${tasks.length-2}`:''):'Добавьте первое задание в настройках'} ShowBadge={tasks.length>0} Badge={`${tasks.filter(task=>task.criterion!=='none').length} с проверкой`} ShowLink LinkLabel="Настроить задания" onClick={()=>navigate({screen:'setup'})}/>:<SummaryMetric State="Ready" Label="Экраны" Value={String(data.total.pages)} Hint="Экраны с сохранёнными посещениями или кликами" Detail={top?`Чаще посещали: ${pageLabels[top.id]||top.id}\nВ ${top.sessions} сессиях`:'Данные появятся после первого посещения'} ShowLink LinkLabel="Открыть тепловую карту" onClick={()=>navigate({screen:'heatmap',item:'',link:''})}/>}
  {scenario?<SummaryMetric State="Ready" Label="Выполнили все задания" Value={assigned.length?`${complete} из ${assigned.length}`:'—'} Hint="Сессии с подтверждённым успехом по всем полученным заданиям" Detail={assigned.length?`${assigned.length-complete} сессий пока без полного успеха\nРезультаты отдельных заданий — ниже`:'Пока нет сессий с сохранёнными заданиями'} ShowBadge={assigned.length>0} Badge={`${Math.round(complete/Math.max(1,assigned.length)*100)}%`} ShowLink LinkLabel="Результаты по сессиям" onClick={()=>navigate({screen:'participants',item:assigned.length?`ids:${assigned.map(session=>session.id).join(',')}`:''})}/>:<SummaryMetric State="Ready" Label="Клики" Value={String(data.total.clicks)} Hint="Сохранённые нажатия в текущей выборке" Detail={`В ${clicking} из ${data.total.sessions} сессий\nКоличество кликов не означает успех задания`} ShowLink LinkLabel="Посмотреть клики" onClick={()=>navigate({screen:'heatmap',item:'',link:''})}/>}
  <SummaryMetric State="Ready" Label="Сессии с сигналами" Value={`${affected} из ${data.total.sessions}`} Hint="Есть серии повторных кликов" Detail={`${data.signals.length} серий повторных кликов\nПовод изучить действия, а не доказанная проблема`} ShowLink LinkLabel="Разобрать сигналы" onClick={()=>navigate({screen:'signals',item:''})}/>
 </div>;
}
