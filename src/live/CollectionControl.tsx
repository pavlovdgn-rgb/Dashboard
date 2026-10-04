import {useEffect,useRef,useState} from 'react';
import {EuiCallOut,EuiLoadingSpinner,EuiSwitch} from '@elastic/eui';
import {Card} from '../screens/WorkspaceUI';
import {liveApi} from './api';
import s from './CollectionControl.module.css';
import w from '../screens/Workspace.module.css';

export function CollectionControl({enabled,refresh}:{enabled:boolean;refresh:()=>void}) {
  const [confirmed,setConfirmed]=useState<boolean|null>(null),[busy,setBusy]=useState(false),[error,setError]=useState('');
  const lock=useRef(false);
  useEffect(()=>setConfirmed(null),[enabled]);
  const checked=confirmed??enabled;
  async function change(next:boolean) {
    if(lock.current)return;
    lock.current=true;setBusy(true);setError('');
    try {const result=await liveApi<{enabled:boolean}>('/config',{enabled:next});setConfirmed(result.enabled);refresh();}
    catch {setError('Не удалось изменить сбор данных. Состояние сохранено. Повторите попытку.');}
    finally {lock.current=false;setBusy(false);}
  }
  return <Card><div className={s.header}><div className={w.heading}><h2>Сбор данных</h2><p className={s.status} data-enabled={checked}>{checked?'Включён':'Приостановлен'}</p></div><div className={s.control} aria-busy={busy}><EuiSwitch className={s.switch} label="Сбор данных" showLabel={false} checked={checked} disabled={busy} onChange={event=>void change(event.target.checked)}/>{busy?<EuiLoadingSpinner size="m"/>:null}</div></div>
    <p>{checked?'Выбранные в настройках данные собираются, пока участник работает в подключённом интерфейсе.':'Новые действия не собираются. Ранее сохранённые данные доступны в результатах.'}</p>
    {error?<EuiCallOut color="danger" title={error}/>:null}
    <p className={w.muted}>Открытые вкладки получают изменение режима в течение нескольких секунд.</p>
  </Card>;
}
