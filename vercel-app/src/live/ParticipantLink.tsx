import {useEffect,useId,useRef,useState} from 'react';
import {createPortal} from 'react-dom';
import {EuiToast} from '@elastic/eui';
import {ProductButton} from '../components';
import {Card} from '../screens/WorkspaceUI';
import field from '../components/_shared/ProductComponent.module.css';
import s from './LiveWorkspace.module.css';

export function ParticipantLink({url,enabled}:{url:string;enabled:boolean}){
  const id=useId(),input=useRef<HTMLInputElement>(null);
  const [status,setStatus]=useState<'idle'|'copying'|'copied'|'error'>('idle');
  useEffect(()=>{setStatus('idle');},[url]);
  useEffect(()=>{if(status!=='copied')return;const timer=setTimeout(()=>setStatus('idle'),5000);return()=>clearTimeout(timer);},[status]);
  async function copy(){
    setStatus('copying');
    try{await navigator.clipboard.writeText(url);setStatus('copied');}
    catch{setStatus('error');input.current?.focus();input.current?.select();}
  }
  return <Card><h2 id={id}>Ссылка для участника</h2>
    <div className={s.participantLink}><div className={field.field}><input ref={input} type="text" value={url} readOnly aria-labelledby={id} aria-describedby={`${id}-help`} onFocus={event=>event.currentTarget.select()}/></div><ProductButton Kind="Primary" icon={status==='copied'?'check':'copy'} State={status==='copying'?'Loading':'Default'} onClick={()=>void copy()}>{status==='copied'?'Скопировано':'Скопировать'}</ProductButton></div>
    <p id={`${id}-help`}>Передайте участнику ссылку и пароль рабочего пространства. В этой версии пароль даёт доступ и к дашборду.</p>
    {!enabled?<p>Сбор приостановлен. Перед тестом включите переключатель «Сбор данных» выше.</p>:null}
    {status==='copied'||status==='error'?createPortal(<div className={s.copyToast} role="status"><EuiToast title={status==='copied'?'Ссылка скопирована':'Не удалось скопировать ссылку'} color={status==='copied'?'success':'danger'} iconType={status==='copied'?'checkInCircleFilled':'alert'} onClose={()=>setStatus('idle')}><p>{status==='copied'?'Можно отправить её участнику.':'Ссылка выделена — нажмите Ctrl+C.'}</p></EuiToast></div>,document.body):null}
  </Card>;
}
