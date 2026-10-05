import {EuiBadge} from '@elastic/eui';
import {Card,Table} from '../screens/WorkspaceUI';
import type {LiveSession,LiveSummary,TaskAttempt,TaskStatus} from './types';
import {MetricRatio} from './MetricRatio';
import {sessionTasks,taskCounts,taskGroups} from './taskMetrics';
import s from './LiveWorkspace.module.css';
import {TaskReview} from './TaskReview';
import {useWireRoute} from '../screens/useWireRoute';

const statusLabels:Record<TaskStatus,string>={succeeded:'Выполнено',failed:'Не выполнено',pending:'Без итогового результата',not_started:'Не начато',unassessed:'Не оценивалось',needs_review:'Ожидает оценки',indeterminate:'Невозможно оценить'};
function Status({status}:{status:TaskStatus}){return <EuiBadge color={status==='succeeded'?'success':status==='failed'?'danger':'hollow'}>{statusLabels[status]}</EuiBadge>;}
function remaining(tasks:TaskAttempt[]){const c=taskCounts(tasks);return `Не выполнено: ${c.failed} · Без итога: ${c.pending} · Не начато: ${c.notStarted} · Не оценивалось: ${c.unassessed}`+(c.needsReview?` · Ожидает оценки: ${c.needsReview}`:'')+(c.indeterminate?` · Невозможно оценить: ${c.indeterminate}`:'');}

export function TaskOutcome({task,details=false}:{task?:LiveSession['task'];details?:boolean}){
 const {route}=useWireRoute();
 const tasks=sessionTasks(task),counts=taskCounts(tasks);
 if(!details)return !tasks.length?<span>Не оценивалось</span>:tasks.length===1?<Status status={tasks[0].status}/>:<div className={s.sessionTaskProgress}><span>{counts.succeeded} из {counts.total} заданий</span><MetricRatio value={counts.succeeded} total={counts.total} label="Выполненные задания сессии"/>{counts.needsReview?<small>Ожидает оценки: {counts.needsReview}</small>:null}{counts.indeterminate?<small>Невозможно оценить: {counts.indeterminate}</small>:null}{counts.pending||counts.notStarted?<small>Не завершено: {counts.pending+counts.notStarted}</small>:null}{counts.failed?<small>Не выполнено: {counts.failed}</small>:null}</div>;
 return <Card><h2>Результаты заданий</h2>{tasks.length?<>
   <p>Выполнено {counts.succeeded} из {counts.total} заданий</p><MetricRatio value={counts.succeeded} total={counts.total} label="Выполненные задания сессии"/>
   <p>{remaining(tasks)}</p><div className={s.taskResultsTable}><Table label="Задания сессии" headers={['Задание','Результат','Критерий']}>
     {tasks.map((item,index)=><tr key={item.taskId}><td>{index+1}. {item.title}<small>{item.scenario}</small></td><td><Status status={item.status}/>{item.reviewedAt?<small>Оценено: {new Date(item.reviewedAt).toLocaleString('ru-RU')}</small>:item.completedAt?<small>{new Date(item.completedAt).toLocaleString('ru-RU')}</small>:null}{item.verification?.method==='manual'&&item.finishedAt!==null?<TaskReview session={route.participant} taskId={item.taskId} status={item.status} onSaved={()=>window.dispatchEvent(new Event('ux-task-reviewed'))}/>:null}</td><td>{item.criterionLabel}{item.verification?<small>{item.verification.method==='manual'?'Ручная оценка':`Автоматически · ${item.verification.value}`}</small>:null}</td></tr>)}
   </Table></div><p>Показаны задания, полученные в этой сессии. Закрытие вкладки не означает неуспех.</p>
 </>:<p>Для этой сессии состав заданий не был сохранён. Её выполнение задним числом не оценивается.</p>}</Card>;
}
export function TaskSummary({data}:{data:Pick<LiveSummary,'project'|'sessions'>}){
 const groups=taskGroups(data),known=data.sessions.filter(session=>sessionTasks(session.task).length).length;
 if(data.project.mode!=='scenario'&&!known)return null;
 return <Card><h2>Выполнение заданий</h2><p>Всего сессий: {data.sessions.length} · С заданиями: {known} · Без сведений о заданиях: {data.sessions.length-known}</p>
   <p>Для каждого задания — доля сессий, в которых подтверждён успех, среди всех сессий, получивших это задание.</p>
   {groups.length?<div className={s.taskResultsTable}><Table label="Результаты заданий" headers={['Задание','Успех подтверждён','Доля сессий','Остальные результаты']}>
     {groups.map(group=>{const versions=[...new Set(group.attempts.map(task=>task.revision))];return <tr key={group.id}>
       <td>{group.title}{group.archived?<small>Удалено из текущего сценария</small>:null}<small>{group.instruction}</small>
       {versions.length>1?<details><summary>Версии задания: {versions.length}</summary>{versions.map(revision=>{const attempts=group.attempts.filter(task=>task.revision===revision),c=taskCounts(attempts);return <p key={revision}>{attempts[0].scenario}<br/>Критерий: {attempts[0].criterionLabel}<br/>Успех: {c.succeeded} из {c.total} · {remaining(attempts)}</p>;})}</details>:null}</td>
       <td>{group.succeeded} из {group.total} сессий</td><td><MetricRatio value={group.succeeded} total={group.total} label={`Успех: ${group.title}`}/></td><td>{remaining(group.attempts)}</td>
     </tr>;})}
   </Table></div>:<p>Добавьте задания в настройках исследования.</p>}
   <p>Неоценённые и неначатые задания не считаются неуспешными. Если условие задания менялось, сравните версии в строке задания.</p>
 </Card>;
}
