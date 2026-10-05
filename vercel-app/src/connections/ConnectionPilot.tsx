import {useEffect,useState} from 'react';
import {EuiCallOut,EuiLink} from '@elastic/eui';
import {ProductButton} from '../components';
import {ProductDropdown} from '../components/_shared/ProductDropdown';
import {Card,Field,Table} from '../screens/WorkspaceUI';
import {embedURL} from './figma';
import {FigmaPlayer} from './FigmaPlayer';
import {API,request} from './api';
import type {Connection,Result} from './api';
import w from '../screens/Workspace.module.css';
import s from './ConnectionPilot.module.css';
const labels:Record<string,string>={visit:'Посещение',INITIAL_LOAD:'Прототип загружен',PRESENTED_NODE_CHANGED:'Переход на экран',MOUSE_PRESS_OR_RELEASE:'Событие мыши Figma',NEW_STATE:'Изменение компонента',LOGIN_SCREEN_SHOWN:'Нужен вход в Figma',PASSWORD_SCREEN_SHOWN:'Нужен пароль'};
export function ConnectionPilot(){
  const [connections,setConnections]=useState<Connection[]>([]),[selected,setSelected]=useState(new URLSearchParams(location.search).get('connection')||'');
  const [kind,setKind]=useState('web'),[name,setName]=useState(''),[url,setURL]=useState(''),[clientId,setClientId]=useState('');
  const [error,setError]=useState(''),[busy,setBusy]=useState(false),[notice,setNotice]=useState(''),[result,setResult]=useState<Result|null>(null),[playing,setPlaying]=useState(false);
  const [readError,setReadError]=useState('');
  const connection=connections.find(row=>row.id===selected);
  function choose(value:string){setResult(null);setPlaying(false);setSelected(value);const address=new URL(location.href);address.searchParams.set('connection',value);history.replaceState({},'',address);}
  useEffect(()=>{let disposed=false;void request<{connections:Connection[]}>('/api/connections').then(data=>{if(!disposed)setConnections(data.connections);}).catch(()=>{if(!disposed)setError('Сервис проверки недоступен. Запустите execution/start_local_heatmap.py.');});return()=>{disposed=true};},[]);
  useEffect(()=>{
    if(!selected)return;
    let disposed=false,running=false;
    async function update(){if(running)return;running=true;try{const data=await request<Result>('/api/results?project='+encodeURIComponent(selected));if(!disposed){setResult(data);setReadError('');}}catch{if(!disposed)setReadError('Не удалось получить события. Повторяем подключение…');}finally{running=false;}}
    void update();const timer=setInterval(()=>void update(),2000);return()=>{disposed=true;clearInterval(timer)};
  },[selected]);
  async function create(){
    setBusy(true);setError('');try{if(kind==='figma')embedURL(url,clientId);const row=await request<Connection>('/api/connections',{name,kind,url,clientId:kind==='figma'?clientId:''});setConnections(old=>[row,...old]);choose(row.id);setNotice('Подключение создано. Теперь проверьте получение событий.');}catch(error){setError(error instanceof Error?error.message:'Не удалось создать подключение');}finally{setBusy(false);}
  }
  async function copy(text:string){try{await navigator.clipboard.writeText(text);setNotice('Скопировано');}catch{setNotice('Не удалось скопировать автоматически. Выделите текст ниже.');}}
  const snippet=connection?`<script defer src="${API}/sdk.js" data-project="${connection.id}"></script>`:'';
  const participant=connection?(()=>{const target=new URL(connection.url);target.searchParams.set('ux_study',connection.study);return target.href;})():'';
  async function policy(){if(!connection)return;setBusy(true);try{await request('/api/policy',{project:connection.id,enabled:!connection.enabled});setConnections(old=>old.map(row=>row.id===connection.id?{...row,enabled:row.enabled?0:1}:row));setPlaying(false);}catch{setError('Не удалось изменить сбор');}finally{setBusy(false);}}
  return <main className={s.page}>
    <EuiLink href="/?screen=results-overview#/setup">← К настройке исследования</EuiLink>
    <div className={w.heading}><h1>Проверка подключений</h1><p className={w.muted}>Пилот · отдельные тестовые сессии, без изменения результатов Lead Generation</p></div>
    {error||readError?<EuiCallOut color="danger" title={error||readError}/>:null}{notice?<p role="status">{notice}</p>:null}
    <Card><h2>Новое подключение</h2><div className={s.form}>
      <ProductDropdown appearance="field" label="Тип интерфейса" value={kind} options={[{value:'web',label:'Сайт или веб-приложение'},{value:'figma',label:'Прототип Figma'}]} onChange={setKind}/>
      <Field label="Название подключения" value={name} onChange={setName}/>
      <Field label={kind==='figma'?'Ссылка на Figma-прототип':'Адрес тестируемой страницы'} value={url} onChange={setURL}/>
      {kind==='figma'?<><Field label="Client ID приложения Figma" value={clientId} onChange={setClientId}/><p className={w.muted}>В приложении Figma → Embed API добавьте разрешённый адрес: <code>{location.origin}</code>. Client Secret здесь не нужен. Без Client ID доступен только предпросмотр.</p><EuiLink href="https://developers.figma.com/docs/embeds/embed-api/" target="_blank" rel="noreferrer">Как настроить Embed API</EuiLink></>:<p className={w.muted}>Для первой проверки используйте локальную HTML-страницу. Сборщик работает на этом компьютере; удалённым участникам потребуется HTTPS-сервис.</p>}
      <ProductButton Kind="Primary" State={busy?'Loading':!name.trim()||!url.trim()?'Disabled':'Default'} onClick={()=>void create()}>Создать подключение</ProductButton>
    </div></Card>
    {connections.length?<ProductDropdown appearance="field" label="Подключение для проверки" value={selected} options={connections.map(row=>({value:row.id,label:row.name}))} onChange={choose}/>:null}
    {connection?<><Card><div className={w.between}><h2>{connection.name}</h2><ProductButton Kind="Secondary" State={busy?'Disabled':'Default'} onClick={()=>void policy()}>{connection.enabled?'Приостановить сбор':'Возобновить сбор'}</ProductButton></div>
      <p>{connection.enabled?(result?.total.events?'События получены':'Ожидаем первые события'):'Сбор приостановлен'}</p>
      {connection.kind==='web'?<><p>1. Добавьте этот код на страницу перед закрывающим тегом head.</p><pre className={s.code}>{snippet}</pre><div><ProductButton Kind="Secondary" onClick={()=>void copy(snippet)}>Скопировать код</ProductButton></div>
        <p>2. Откройте ссылку участника, нажмите кнопку и перейдите на другую страницу.</p><EuiLink href={participant} target="_blank" rel="noreferrer">Открыть тестируемый сайт ↗</EuiLink><pre className={s.code}>{participant}</pre>
        <p className={w.muted}>Передаются технические ID экранов, клики и размеры окна. Текст, значения полей, HTML и видео не собираются. Для понятных ID можно добавить data-ux-page и data-ux-target; data-ux-private исключает область из сбора кликов.</p>
      </>:<><p>Откройте прототип, нажмите на интерактивный элемент и перейдите на следующий экран. События появятся в журнале ниже.</p><p className={w.muted}>Прототип должен быть доступен участнику по настройкам Figma.</p><div><ProductButton Kind="Primary" State={!connection.enabled||playing?'Disabled':'Default'} onClick={()=>setPlaying(true)}>Открыть прототип для проверки</ProductButton></div></>}
    </Card>
    {playing&&connection.kind==='figma'?<FigmaPlayer key={connection.id} connection={connection}/>:null}
    <Card><div className={w.between}><h2>Полученные события</h2><span>Событий: {result?.total.events||0} · Сессий: {result?.total.sessions||0}</span></div>
      {result?.events.length?<div className={s.events}><Table label="События подключения" headers={['Время','Событие','Экран / элемент','Сессия']}>{result.events.map(event=><tr key={event.id}><td>{new Date(event.timestamp).toLocaleTimeString('ru-RU')}</td><td>{labels[event.kind||'']||'Клик'}</td><td>{event.page}{event.target?' / '+event.target:''}</td><td>{event.session.slice(0,8)}</td></tr>)}</Table></div>:<p className={w.muted}>Пока событий нет. Открытие ссылки само по себе не подтверждает, что сбор работает.</p>}
      <p className={w.muted}>Показаны последние 100 событий. Журнал сохраняется после обновления страницы.</p>
    </Card></>:null}
  </main>;
}
