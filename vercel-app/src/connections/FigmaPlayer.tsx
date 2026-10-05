import {useEffect,useRef,useState} from 'react';
import {ProductButton} from '../components';
import {Card} from '../screens/WorkspaceUI';
import {embedURL,figmaEvent} from './figma';
import type {PilotEvent} from './figma';
import type {Connection} from './api';
import {API} from './api';
import w from '../screens/Workspace.module.css';
import s from './ConnectionPilot.module.css';
type Collector={record(data:PilotEvent):void;dispose():void;session:string};
declare global{interface Window{UXLabSDK?:{attach(config:Record<string,unknown>):Collector}}}
function loadSDK():Promise<void>{
  if(window.UXLabSDK)return Promise.resolve();
  return new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=API+'/sdk.js';script.onload=()=>resolve();script.onerror=()=>{script.remove();reject(Error('Не удалось загрузить сборщик'));};document.head.append(script);});
}
export function FigmaPlayer({connection}:{connection:Connection}){
  const iframe=useRef<HTMLIFrameElement>(null);
  const [ready,setReady]=useState(false),[loaded,setLoaded]=useState(false),[status,setStatus]=useState('Ожидаем события Figma…'),[delivery,setDelivery]=useState(''),[count,setCount]=useState(0);
  useEffect(()=>{
    let disposed=false,collector:Collector|undefined,observed=false,timer:ReturnType<typeof setTimeout>|undefined;
    const receive=(event:MessageEvent)=>{
      const record=figmaEvent(event,iframe.current?.contentWindow||null);if(!record)return;
      observed=true;setCount(value=>value+1);
      if(record.kind==='INITIAL_LOAD'){setLoaded(true);setStatus('Прототип загружен. Сделайте клик и перейдите на другой экран.');}
      else if(record.kind==='LOGIN_SCREEN_SHOWN')setStatus('Для этого прототипа требуется вход в Figma.');
      else if(record.kind==='PASSWORD_SCREEN_SHOWN')setStatus('Для этого прототипа требуется пароль.');
      else setStatus('События Figma поступают');
      collector?.record(record);
    };
    void loadSDK().then(()=>{
      if(disposed)return;
      collector=window.UXLabSDK!.attach({root:document.createElement('div'),study:connection.study,version:'figma-embed-v1',namespace:connection.id,endpoint:API+'/api/events?'+new URLSearchParams({project:connection.id,study:connection.study}),getContext:()=>null,onStatus:(state:{pending:number;error:string})=>{if(!disposed)setDelivery(state.error||(state.pending?`Ожидают отправки: ${state.pending}`:'Очередь отправлена'));}});
      window.addEventListener('message',receive);setReady(true);
      timer=setTimeout(()=>{if(!observed)setStatus(connection.client_id?'Событий пока нет. Проверьте Client ID, разрешённый адрес и доступ к прототипу.':'Предпросмотр доступен, но для получения событий нужен Client ID приложения Figma.');},15000);
    }).catch(error=>{if(!disposed)setStatus(error.message);});
    return()=>{disposed=true;clearTimeout(timer);window.removeEventListener('message',receive);collector?.dispose();};
  },[connection.id,connection.study,connection.client_id]);
  return <Card><div className={w.between}><h2>Проверка Figma</h2><ProductButton Kind="Secondary" State={loaded?'Default':'Disabled'} onClick={()=>iframe.current?.contentWindow?.postMessage({type:'RESTART'},'https://www.figma.com')}>Начать заново</ProductButton></div>
    <p role="status">{status}</p><p className={w.muted}>Получено событий: {count} · {delivery}</p>
    {ready?<iframe ref={iframe} className={s.frame} title="Тестируемый прототип Figma" src={embedURL(connection.url,connection.client_id)} allowFullScreen/>:null}
    <p className={w.muted}>Проверяем события и переходы. Тепловая карта, восстановление состояний и видеозапись Figma в эту проверку не входят.</p>
  </Card>;
}
