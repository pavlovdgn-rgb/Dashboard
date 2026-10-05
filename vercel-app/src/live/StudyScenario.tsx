import {useCallback,useState} from 'react';
import {EuiButtonGroup,EuiCallOut,EuiToolTip} from '@elastic/eui';
import {ProductAction} from '../components/_shared/ProductComponent';
import type {LiveConfig,StudyTaskDefinition} from './types';
import {studyTasks} from './taskMetrics';
import {SuccessCriteriaEditor} from './SuccessCriteriaEditor';
import {ProductButton} from '../components';
import {Card,Field} from '../screens/WorkspaceUI';
import {liveApi} from './api';
import s from './LiveWorkspace.module.css';
import switchStyles from '../components/_shared/SignalViewSwitch.module.css';

type Draft={mode:'free'|'scenario';tasks:StudyTaskDefinition[]};
const freshTask=(index:number):StudyTaskDefinition=>({id:crypto.randomUUID(),title:`Задание ${index+1}`,instruction:'',criterion:'custom',successDescription:'',verification:{method:'manual'}});
const payload=(draft:Draft)=>({...draft,tasks:draft.tasks.map(({id,title,instruction,criterion,successDescription,verification})=>({id,title,instruction,criterion,successDescription,verification}))});
function TaskIconAction({label,icon,disabled,onClick}:{label:string;icon:string;disabled:boolean;onClick:()=>void}){return <EuiToolTip content={label}><span><ProductAction kind="Tertiary" icon={icon} label={label} state={disabled?'Disabled':'Default'} onClick={onClick}/></span></EuiToolTip>;}
export function StudyScenario({config,refresh}:{config:LiveConfig;refresh:()=>void}){
 const [draft,setDraft]=useState<Draft|null>(null),[busy,setBusy]=useState(false),[saved,setSaved]=useState(false),[error,setError]=useState('');
 const [validity,setValidity]=useState<Record<string,boolean>>({});
 const onValidity=useCallback((id:string,valid:boolean)=>setValidity(old=>old[id]===valid?old:{...old,[id]:valid}),[]);
 const original:Draft={mode:config.mode||'free',tasks:studyTasks(config)},values=draft??original;
 const change=(patch:Partial<Draft>)=>{setDraft({...values,...patch});setSaved(false);};
 const update=(id:string,patch:Partial<StudyTaskDefinition>)=>change({tasks:values.tasks.map(task=>task.id===id?{...task,...patch}:task)});
 const reorder=(index:number,direction:number)=>{const tasks=[...values.tasks];[tasks[index],tasks[index+direction]]=[tasks[index+direction],tasks[index]];change({tasks});};
 const dirty=JSON.stringify(payload(values))!==JSON.stringify(payload(original));
 const invalid=values.tasks.some(task=>task.title.length>120||task.instruction.length>2000)||(values.mode==='scenario'&&(!values.tasks.length||values.tasks.some(task=>!task.title.trim()||!task.instruction.trim()||validity[task.id]===false)));
 async function save(){if(busy||invalid)return;setBusy(true);setSaved(false);setError('');try{await liveApi('/config',payload(values));setSaved(true);setDraft(null);refresh();}catch(e){setError(e instanceof Error?e.message:'Не удалось сохранить задания.');}finally{setBusy(false);}}
 return <Card><h2>Режим исследования</h2><div className={s.taskEditor}>
   <EuiButtonGroup className={switchStyles.root} buttonSize="s" color="text" legend="Режим исследования" idSelected={values.mode} options={[{id:'free',label:'Свободное изучение'},{id:'scenario',label:'По сценарию'}]} onChange={mode=>change({mode:mode as Draft['mode'],tasks:mode==='scenario'&&!values.tasks.length?[freshTask(0)]:values.tasks})} isDisabled={busy}/>
   {values.mode==='scenario'?<>
     <p>Участник получает задания по порядку. У каждого задания свой критерий успеха и отдельный результат.</p>
     {values.tasks.map((task,index)=><section className={s.taskEditorItem} key={task.id} aria-label={`Задание ${index+1}`}>
       <div className={s.taskEditorHeading}><h3>Задание {index+1}</h3><div className={s.taskIconActions}>
         <TaskIconAction icon="arrowUp" label={`Переместить задание ${index+1} вверх`} disabled={busy||!index} onClick={()=>reorder(index,-1)}/>
         <TaskIconAction icon="arrowDown" label={`Переместить задание ${index+1} вниз`} disabled={busy||index===values.tasks.length-1} onClick={()=>reorder(index,1)}/>
         <TaskIconAction icon="trash" label={`Удалить задание ${index+1}`} disabled={busy} onClick={()=>change({tasks:values.tasks.filter(t=>t.id!==task.id)})}/>
       </div></div>
       <Field label="Название задания" value={task.title} onChange={title=>update(task.id,{title})} error={task.title.length>120}/>
       <Field label="Задание" type="Textarea" value={task.instruction} onChange={instruction=>update(task.id,{instruction})} error={task.instruction.length>2000}/>
       <SuccessCriteriaEditor task={task} busy={busy} update={patch=>update(task.id,patch)} onValidity={onValidity}/>
     </section>)}
     {!values.tasks.length?<p role="status">Добавьте хотя бы одно задание.</p>:null}
     <div><ProductButton Kind="Secondary" icon="plus" State={busy||values.tasks.length>=20?'Disabled':'Default'} onClick={()=>change({tasks:[...values.tasks,freshTask(values.tasks.length)]})}>Добавить задание</ProductButton></div>
     <p className={s.taskEditorHint}>После завершения откроется следующее задание. При автоматической проверке фиксируется достижение условия; при ручной — результат ожидает вашей оценки. Неначатые и незавершённые задания учитываются отдельно.</p>
   </>:<p>Свободное изучение без заданий и оценки выполнения. Список заданий сохраняется и будет доступен при переключении режима.</p>}
   <div><ProductButton Kind="Secondary" State={busy?'Loading':!dirty||invalid?'Disabled':'Default'} onClick={()=>void save()}>Сохранить сценарий</ProductButton></div>
 </div><p className={s.taskEditorHint}>Изменения списка и критериев применяются к новым сессиям. Начатая сессия сохраняет свой порядок заданий и их условия.</p>{saved?<p role="status">Сценарий сохранён</p>:null}{error?<EuiCallOut color="danger" title={error}/>:null}</Card>;
}
