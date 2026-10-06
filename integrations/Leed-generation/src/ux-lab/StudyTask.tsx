import {useEffect,useId,useRef,useState} from 'react'
import {Button} from '../components/Button'
import {taskState,finishTask} from './task'
import {collectionEnabled,studyInstructions} from './activity'

/** Native modal keeps focus inside the task and restores it to the reopen button. */
export function StudyTask({scenario,studyTitle}:{scenario:string;studyTitle:string}){
  const dialog=useRef<HTMLDialogElement>(null),reopen=useRef<HTMLElement>(null),id=useId()
  const [state,setState]=useState(taskState)
  const run=state.run,tasks=run?.tasks;
  const current=tasks?.find(task=>task.taskId===run?.activeTaskId)||tasks?.at(-1);
  const instruction=current?.scenario||scenario,title=current?.title||studyInstructions().tasks[0]?.title;
  const taskKey=current?`${current.taskId}:${current.revision}`:scenario;
  const total=tasks?.length||studyInstructions().tasks.length||1;
  const automatic=(current?.verification||run?.verification)?.method==='automatic';
  useEffect(()=>{const update=()=>setState({...taskState()});addEventListener('ux-task-state',update);addEventListener('ux-lab-policy',update);return()=>{removeEventListener('ux-task-state',update);removeEventListener('ux-lab-policy',update)}},[])
  useEffect(()=>{if(taskKey&&!dialog.current?.open)dialog.current?.showModal()},[taskKey,run?.finishedAt])
  if(!instruction)return null
  return <><aside ref={reopen} className="ux-study-task" data-ux-private="true" data-ux-overlay="true"><Button variant="secondary" onClick={()=>dialog.current?.showModal()}>Посмотреть задание</Button>{total>1?<span className="ux-study-counter">{run?.finishedAt?'Задания завершены':`Задание ${(current?.ordinal||0)+1} из ${total}`}</span>:null}</aside>
    <dialog ref={dialog} className="ux-study-dialog" aria-labelledby={id} aria-describedby={`${id}-body`} data-ux-private="true" data-ux-overlay="true" onClose={()=>reopen.current?.querySelector('button')?.focus()}>
      <p className="ux-study-caption">{studyTitle}{total>1?` · Задание ${(current?.ordinal||0)+1} из ${total}`:''}</p><h2 id={id}>Задание исследования</h2>{title&&title!=='Задание 1'?<h3>{title}</h3>:null}<p id={`${id}-body`} className="ux-study-scenario">{instruction}</p>
      {state.error?<p role="alert">{state.error}</p>:null}
      {automatic&&!run?.finishedAt?<p className="ux-study-caption">Задание завершится автоматически, когда вы выполните нужное действие.</p>:null}
      {state.run?.finishedAt?<p role="status">Попытка завершена. Спасибо за участие!</p>:total>1?<p className="ux-study-caption">После завершения текущего задания откроется следующее. Пройдено: {run?.finishedTasks||0} из {total}.</p>:null}
      <div className="ux-study-actions">{state.run&&!state.run.finishedAt&&!automatic?<Button variant="secondary" disabled={!collectionEnabled()||state.pending} onClick={()=>finishTask()}>{state.pending?'Сохраняем результат…':'Завершить задание'}</Button>:null}<Button autoFocus onClick={()=>dialog.current?.close()}>{state.run?.finishedAt?'Закрыть':'Понятно, к заданию'}</Button></div>
    </dialog></>
}
