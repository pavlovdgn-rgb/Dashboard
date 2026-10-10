import {useState} from 'react';
import {createPortal} from 'react-dom';
import {EuiButton,EuiCallOut,EuiContextMenuItem,EuiContextMenuPanel,EuiLink,EuiModal,EuiModalHeader,EuiModalHeaderTitle,EuiModalBody,EuiModalFooter,EuiPopover} from '@elastic/eui';
import {ProductButton} from '../components';
import menuStyles from '../components/_shared/ProductComponent.module.css';
import {Empty,Field,Table} from '../screens/WorkspaceUI';
import {useWireRoute} from '../screens/useWireRoute';
import {liveApi} from './api';
import type {LiveConfig,LiveSummary} from './types';
import s from './LiveWorkspace.module.css';

type Study=NonNullable<LiveSummary['studies']>[number];

export function ProjectList({data,refresh,headerActions}:{data:LiveSummary;refresh:()=>void;headerActions?:HTMLElement|null}){
 const {route,navigate}=useWireRoute();
 const [creating,setCreating]=useState(false),[title,setTitle]=useState(''),[scenario,setScenario]=useState(''),[busy,setBusy]=useState(false),[error,setError]=useState('');
 const [deleting,setDeleting]=useState<Study|null>(null),[deleteBusy,setDeleteBusy]=useState(false),[deleteError,setDeleteError]=useState('');
 const [openMenuStudyId,setOpenMenuStudyId]=useState<string|null>(null);
 const studies=data.studies||[{...data.project,sessions:data.total.sessions,createdAt:0}];
 const action=<span className={s.reportAction}><ProductButton Kind="Primary" icon="plus" onClick={()=>{setError('');setCreating(true);}}>Создать исследование</ProductButton></span>;
 async function create(){
   if(busy||!title.trim()||title.trim().length>120||scenario.length>2000)return;
   setBusy(true);setError('');
   try{const study=await liveApi<LiveConfig>('/studies',{studyTitle:title.trim(),scenario:scenario.trim()});setCreating(false);refresh();navigate({screen:'setup',study:study.studyId,device:'all'});}
   catch(e){setError(e instanceof Error?e.message:'Не удалось создать исследование.');}
   finally{setBusy(false);}
 }
 async function removeStudy(){
   if(deleteBusy||!deleting)return;
   setDeleteBusy(true);setDeleteError('');
   try{
     const result=await liveApi<{deleted:string;nextStudyId:string|null}>('/studies/delete',{studyId:deleting.studyId});
     setDeleting(null);refresh();
     if(route.study===result.deleted)navigate({screen:'studies',study:result.nextStudyId||'biletberu-mobile',device:'all'},true);
   }catch(e){setDeleteError(e instanceof Error?e.message:'Не удалось удалить исследование.');}
   finally{setDeleteBusy(false);}
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
  {deleting?<EuiModal onClose={()=>{if(!deleteBusy)setDeleting(null);}} aria-labelledby="delete-study-heading"><EuiModalHeader><EuiModalHeaderTitle id="delete-study-heading">Удалить исследование?</EuiModalHeaderTitle></EuiModalHeader><EuiModalBody>
    <p>Исследование «{deleting.studyTitle}» будет удалено вместе со всеми сессиями ({deleting.sessions}), результатами, записями и отчётами. Ссылка участника перестанет работать. Восстановить данные после удаления нельзя.</p>
    {deleteError?<EuiCallOut color="danger" title={deleteError}/>:null}
  </EuiModalBody><EuiModalFooter><ProductButton Kind="Tertiary" State={deleteBusy?'Disabled':'Default'} onClick={()=>setDeleting(null)}>Отмена</ProductButton><EuiButton color="danger" fill isLoading={deleteBusy} onClick={()=>void removeStudy()}>Удалить исследование</EuiButton></EuiModalFooter></EuiModal>:null}
  {route.screen==='studies'&&!studies.length?<Empty>В проекте пока нет исследований. Создайте первое исследование.</Empty>:<div className={`${s.table} ${route.screen==='studies'?s.studyTable:''}`}><Table label={route.screen==='projects'?'Проекты':'Исследования'} headers={route.screen==='projects'?['Проект','Исследований','Сбор']:['Исследование','Сценарий','Сессий','Сбор','Действия']}>
   {route.screen==='projects'?<tr><td><EuiLink data-row-action onClick={()=>navigate({screen:'studies'})}>Билет Беру</EuiLink><small>Мобильный прототип покупки билетов</small></td><td>{studies.length}</td><td>{studies.some(study=>study.enabled)?'Включён':'Приостановлен'}</td></tr>:studies.map(study=><tr key={study.studyId}><td><EuiLink data-row-action onClick={()=>navigate({screen:'overview',study:study.studyId,device:'all'})}>{study.studyTitle}</EuiLink>{study.roundNumber?<small>Раунд {study.roundNumber}</small>:null}</td><td><span className={s.scenarioPreview} title={study.scenario}>{study.mode==='scenario'?`${study.tasks?.length||1} заданий · ${study.scenario||'По сценарию'}`:'Свободное изучение'}</span></td><td>{study.sessions}</td><td>{study.roundClosedAt?'Зафиксирован':study.enabled?'Включён':'Приостановлен'}</td><td><EuiPopover isOpen={openMenuStudyId===study.studyId} closePopover={()=>setOpenMenuStudyId(null)} anchorPosition="downRight" hasArrow={false} offset={4} panelPaddingSize="none" panelClassName={menuStyles.dropdownPanel} button={<button type="button" className={s.studyMoreAction} aria-label={`Действия с исследованием «${study.studyTitle}»`} aria-haspopup="menu" aria-expanded={openMenuStudyId===study.studyId} onClick={()=>setOpenMenuStudyId(openMenuStudyId===study.studyId?null:study.studyId)}><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg></button>}><EuiContextMenuPanel role="menu" aria-label={`Действия с исследованием «${study.studyTitle}»`} initialFocusedItemIndex={0} items={[<EuiContextMenuItem key="delete" role="menuitem" icon="trash" className={`${menuStyles.dropdownItem} ${s.studyMenuDelete}`} onClick={()=>{setOpenMenuStudyId(null);setDeleteError('');setDeleting(study);}}>Удалить</EuiContextMenuItem>]}/></EuiPopover></td></tr>)}
  </Table></div>}
 </>;
}
