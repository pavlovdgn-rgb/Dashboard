import {useState} from 'react';
import {EuiButton,EuiButtonEmpty,EuiCallOut,EuiModal,EuiModalBody,EuiModalFooter,EuiModalHeader,EuiModalHeaderTitle} from '@elastic/eui';
import {ProductButton} from '../components';
import {Card} from '../screens/WorkspaceUI';
import {liveApi} from './api';
import type {LiveSummary} from './types';
import s from './LiveWorkspace.module.css';

export function StudyReset({data,refresh}:{data:LiveSummary;refresh:()=>void}){
 const [confirmation,setConfirmation]=useState<{resetId:string;version:string}|null>(null);
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[done,setDone]=useState(false);
 async function reset(){
  if(busy||!confirmation)return;
  setBusy(true);setError('');
  try{
   await liveApi('/studies/reset',{studyId:data.project.studyId,...confirmation});
   setConfirmation(null);setDone(true);refresh();
  }catch(cause){setError(cause instanceof Error?cause.message:'Не удалось обнулить статистику. Повторите попытку.');}
  finally{setBusy(false);}
 }
 return <>
  <Card><h2>Сброс результатов</h2>
   <p>Обнулите статистику перед новым тестированием. Настройки исследования и задания сохранятся.</p>
   <div className={s.actions}><EuiButtonEmpty color="danger" iconType="refresh" onClick={()=>{setError('');setDone(false);setConfirmation({resetId:crypto.randomUUID(),version:data.project.collectionVersion||''});}}>Обнулить статистику</EuiButtonEmpty></div>
   {done?<p role="status">Статистика обнулена. Сбор приостановлен — включите его в разделе «Проверка и запуск», когда будете готовы.</p>:null}
  </Card>
  {confirmation?<EuiModal aria-labelledby="reset-study-heading" onClose={()=>{if(!busy)setConfirmation(null);}}>
   <EuiModalHeader><EuiModalHeaderTitle><h2 id="reset-study-heading">Обнулить статистику исследования?</h2></EuiModalHeaderTitle></EuiModalHeader>
   <EuiModalBody>
    <p>В исследовании «{data.project.studyTitle}» будут удалены все сессии ({data.total.sessions}), посещения, клики, тепловые карты, записи прохождений, результаты заданий, находки и отчёты.</p>
    <p>Настройки, задания и ссылка участника сохранятся. Сбор данных будет приостановлен. Исследование можно будет запустить заново.</p>
    <p>Восстановить удалённые результаты нельзя. Другие исследования не изменятся.</p>
    {error?<EuiCallOut color="danger" role="alert" title={error}/>:null}
   </EuiModalBody>
   <EuiModalFooter><ProductButton Kind="Tertiary" State={busy?'Disabled':'Default'} onClick={()=>setConfirmation(null)}>Отмена</ProductButton><EuiButton color="danger" fill isLoading={busy} onClick={()=>void reset()}>Обнулить статистику</EuiButton></EuiModalFooter>
  </EuiModal>:null}
 </>;
}
