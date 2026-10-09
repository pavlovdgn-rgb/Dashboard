import {useState} from 'react';
import {createPortal} from 'react-dom';
import {EuiCallOut,EuiLink,EuiModal,EuiModalHeader,EuiModalHeaderTitle,EuiModalBody,EuiModalFooter} from '@elastic/eui';
import {ProductButton} from '../components';
import {Field,Table} from '../screens/WorkspaceUI';
import {useWireRoute} from '../screens/useWireRoute';
import {liveApi} from './api';
import type {LiveConfig,LiveSummary} from './types';
import s from './LiveWorkspace.module.css';

export function ProjectList({data,refresh,headerActions}:{data:LiveSummary;refresh:()=>void;headerActions?:HTMLElement|null}){
 const {route,navigate}=useWireRoute();
 const [creating,setCreating]=useState(false),[title,setTitle]=useState(''),[scenario,setScenario]=useState(''),[busy,setBusy]=useState(false),[error,setError]=useState('');
 const studies=data.studies||[{...data.project,sessions:data.total.sessions,createdAt:0}];
 const action=<span className={s.reportAction}><ProductButton Kind="Primary" icon="plus" onClick={()=>{setError('');setCreating(true);}}>Создать исследование</ProductButton></span>;
 async function create(){
   if(busy||!title.trim()||title.trim().length>120||scenario.length>2000)return;
   setBusy(true);setError('');
   try{const study=await liveApi<LiveConfig>('/studies',{studyTitle:title.trim(),scenario:scenario.trim()});setCreating(false);refresh();navigate({screen:'setup',study:study.studyId,device:'all'});}
   catch(e){setError(e instanceof Error?e.message:'Не удалось создать исследование.');}
   finally{setBusy(false);}
 }
 return <>
  {route.screen==='studies'?(headerActions?createPortal(action,headerActions):action):null}
  {creating?<EuiModal onClose={()=>{if(!busy)setCreating(false);}} aria-labelledby="new-study-heading"><EuiModalHeader><EuiModalHeaderTitle><h2 id="new-study-heading">Новое исследование</h2></EuiModalHeaderTitle></EuiModalHeader><EuiModalBody><div className={s.form}>
   <p>Прототип: Билет Беру. У исследования будут свои настройки, ссылка для участника и результаты.</p>
   <Field label="Название исследования" value={title} onChange={setTitle} error={title.length>120}/>
   <Field label="Сценарий для участника (необязательно)" type="Textarea" value={scenario} onChange={setScenario} error={scenario.length>2000}/>
   <p>Например: найдите мероприятие и попробуйте оформить билет.</p>
   <p>Сбор будет выключен до запуска исследования.</p>
   {error?<EuiCallOut color="danger" title={error}/>:null}
  </div></EuiModalBody><EuiModalFooter><ProductButton Kind="Tertiary" State={busy?'Disabled':'Default'} onClick={()=>setCreating(false)}>Отмена</ProductButton><ProductButton Kind="Primary" State={busy?'Loading':!title.trim()||title.length>120||scenario.length>2000?'Disabled':'Default'} onClick={()=>void create()}>Создать</ProductButton></EuiModalFooter></EuiModal>:null}
  <div className={`${s.table} ${route.screen==='studies'?s.studyTable:''}`}><Table label={route.screen==='projects'?'Проекты':'Исследования'} headers={route.screen==='projects'?['Проект','Исследований','Сбор']:['Исследование','Сценарий','Сессий','Сбор']}>
   {route.screen==='projects'?<tr><td><EuiLink data-row-action onClick={()=>navigate({screen:'studies'})}>Билет Беру</EuiLink><small>Мобильный прототип покупки билетов</small></td><td>{studies.length}</td><td>{studies.some(study=>study.enabled)?'Включён':'Приостановлен'}</td></tr>:studies.map(study=><tr key={study.studyId}><td><EuiLink data-row-action onClick={()=>navigate({screen:'overview',study:study.studyId,device:'all'})}>{study.studyTitle}</EuiLink></td><td><span className={s.scenarioPreview} title={study.scenario}>{study.mode==='scenario'?`${study.tasks?.length||1} заданий · ${study.scenario||'По сценарию'}`:'Свободное изучение'}</span></td><td>{study.sessions}</td><td>{study.enabled?'Включён':'Приостановлен'}</td></tr>)}
  </Table></div>
 </>;
}
