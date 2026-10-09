import {useRef,useState} from 'react';
import {EuiCallOut,EuiModal,EuiModalBody,EuiModalFooter,EuiModalHeader,EuiModalHeaderTitle} from '@elastic/eui';
import {ProductButton} from '../components';
import {DesignIcon} from '../components/_shared/CatalogComponent';
import {liveApi} from './api';
import type {LiveConfig,LiveSummary} from './types';
import s from './SidebarRoundControl.module.css';

type Props={data:LiveSummary|null;connectionError:string;refresh:()=>void;onRoundFixed:(studyId:string)=>void};
const stamp=(value:number)=>`${new Date(value).toLocaleDateString('ru-RU',{day:'2-digit',month:'2-digit'})} ${new Date(value).toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit'})}`;

export function SidebarRoundControl({data,connectionError,refresh,onRoundFixed}:Props){
  const [confirm,setConfirm]=useState(false),[busy,setBusy]=useState(false),[checking,setChecking]=useState(false),[checkFailed,setCheckFailed]=useState(false),[actionError,setActionError]=useState('');
  const locked=useRef(false);
  const project=data?.project;
  const respondents=data?.studies?.find(item=>item.studyId===project?.studyId)?.sessions??data?.total.sessions??0;
  const unavailable=Boolean(connectionError||checkFailed);
  const status=unavailable?'нет связи со сборщиком':!project?'проверяем подключение':project.roundClosedAt?'раунд зафиксирован':project.enabled?'сбор подключён':'сбор приостановлен';
  const round=project?.roundClosedAt?`раунд ${project.roundNumber||1} зафиксирован`:!project?.enabled&&respondents===0?'раунд не начат':`раунд ${project?.roundNumber||1}`;

  async function check(){
    if(locked.current||checking)return;
    setChecking(true);setCheckFailed(false);setActionError('');
    try{await liveApi<LiveConfig>('/config');refresh();}
    catch(error){setCheckFailed(true);setActionError(error instanceof Error?error.message:'Не удалось проверить подключение.');}
    finally{setChecking(false);}
  }
  async function fix(){
    if(locked.current||!project||project.roundClosedAt||respondents===0)return;
    locked.current=true;setBusy(true);setActionError('');
    try{
      const result=await liveApi<{fixed:LiveConfig;next:LiveConfig}>('/rounds',{});
      setConfirm(false);onRoundFixed(result.next.studyId);
    }catch(error){setActionError(error instanceof Error?error.message:'Не удалось зафиксировать раунд.');}
    finally{locked.current=false;setBusy(false);}
  }

  return <>
    <section className={s.footer} aria-label="Состояние сбора и раунда">
      <p className={s.status} data-error={unavailable} data-enabled={Boolean(project?.enabled)}><span className={s.dot}/>{status}</p>
      <p className={s.detail}>{data?.lastEventAt?`последнее событие: ${stamp(data.lastEventAt)}`:'последних событий нет'}</p>
      <p className={s.detail}>{round} · {respondents} респ.</p>
      <div className={s.action}><ProductButton Kind="Secondary" State={checking?'Loading':'Default'} onClick={()=>void check()}><DesignIcon type="refresh"/>Обновить</ProductButton></div>
      <div className={s.action}><ProductButton key={!project||project.roundClosedAt||respondents===0?'disabled':'ready'} Kind="Secondary" State={!project||project.roundClosedAt||respondents===0?'Disabled':'Default'} onClick={()=>setConfirm(true)}>Зафиксировать раунд</ProductButton></div>
      {actionError?<p className={s.error} role="alert">{actionError}</p>:null}
    </section>
    {confirm?<EuiModal onClose={()=>{if(!busy)setConfirm(false);}} aria-labelledby="fix-round-heading"><EuiModalHeader><EuiModalHeaderTitle><h2 id="fix-round-heading">Зафиксировать раунд?</h2></EuiModalHeaderTitle></EuiModalHeader><EuiModalBody>
      <p>Текущие сессии сохранятся в этом раунде, а сбор для него остановится. Создадим новый пустой раунд с отдельной ссылкой для участников.</p>
      <p>После фиксации откроется страница новой ссылки. Перед её отправкой включите сбор.</p>
      {actionError?<EuiCallOut color="danger" title={actionError}/>:null}
    </EuiModalBody><EuiModalFooter><ProductButton Kind="Tertiary" State={busy?'Disabled':'Default'} onClick={()=>setConfirm(false)}>Отмена</ProductButton><ProductButton Kind="Primary" State={busy?'Loading':'Default'} onClick={()=>void fix()}>Зафиксировать раунд</ProductButton></EuiModalFooter></EuiModal>:null}
  </>;
}
