import { useEffect,useRef,useState } from 'react';
import { EuiBreadcrumbs,EuiCallOut,EuiLink,EuiLoadingSpinner } from '@elastic/eui';
import { NavMenu,ProductButton } from '../components';
import { ProductTheme } from '../tokens/ProductTheme';
import { ProductDropdown } from '../components/_shared/ProductDropdown';
import { DesignIcon } from '../components/_shared/CatalogComponent';
import {OpenInterfaceButton} from '../components/_shared/OpenInterfaceButton';
import { useWireRoute } from '../screens/useWireRoute';
import { navigationRoutes,screenRegistry } from '../screens/registry';
import { LocalHeatmap } from '../heatmap/LocalHeatmap';
import { LiveViews } from './LiveViews';
import { SidebarRoundControl } from './SidebarRoundControl';
import { liveApi } from './api';
import type { LiveSummary } from './types';
import layout from '../pages/ResultsOverview.module.css';
import w from '../screens/Workspace.module.css';
import crumbs from '../screens/WorkspaceBreadcrumbs.module.css';
import s from './LiveWorkspace.module.css';

const titles:Record<string,string>={overview:'Обзор результатов',participants:'Сессии',participant:'История сессии',replay:'История сессии',setup:'Настройка исследования',launch:'Проверка и запуск',funnel:'Воронка переходов',report:'Отчёты',signals:'Сигналы затруднений',findings:'Находки команды',projects:'Все проекты',studies:'Исследования проекта',heatmap:'Тепловая карта кликов','heatmap-live':'Тепловая карта кликов'};
export function LiveWorkspace() {
  const {route,navigate}=useWireRoute();
  const [headerActions,setHeaderActions]=useState<HTMLDivElement|null>(null);
  const [data,setData]=useState<LiveSummary|null>(null),[error,setError]=useState(''),[revision,setRevision]=useState(0);
  const cached=useRef(new Map<string,LiveSummary>()),content=useRef<HTMLDivElement>(null),lastHeight=useRef(480);
  const map=['heatmap','heatmap-live'].includes(route.screen);
  const summaryDevice=map||['setup','launch','report'].includes(route.screen)?'all':route.device;
  useEffect(()=>{const reviewed=()=>setRevision(value=>value+1);addEventListener('ux-task-reviewed',reviewed);return()=>removeEventListener('ux-task-reviewed',reviewed);},[]);
  useEffect(()=>{
    let disposed=false,busy=false;
    async function read(){if(busy)return;busy=true;try{const next=await liveApi<LiveSummary>(`?device=${summaryDevice}`);if(!disposed){cached.current.set(`${route.study}:${summaryDevice}`,next);setData(next);setError('');}}catch(e){if(!disposed){setError(e instanceof Error?e.message:'Не удалось загрузить проект.');}}finally{busy=false;}}
    void read();const timer=setInterval(()=>void read(),2000);return()=>{disposed=true;clearInterval(timer);};
  },[summaryDevice,revision,route.study]);
  // Retire the old product workspace; keep its state as a backup rather than mixing it with live data.
  useEffect(()=>{try {const old=localStorage.getItem('ux-lab-workspace-v1');if(old){if(!localStorage.getItem('ux-lab-workspace-archive-v1'))localStorage.setItem('ux-lab-workspace-archive-v1',old);localStorage.removeItem('ux-lab-workspace-v1');}}catch{/* Storage may be unavailable; live project still comes from SQLite. */}},[]);
  const title=titles[route.screen]||'Проверка и запуск';
  const scopedData=data?.project.studyId===route.study?data:cached.current.get(`${route.study}:${summaryDevice}`)||null;
  const project=scopedData?.project;
  const studyTitle=project?.studyTitle||data?.studies?.find(study=>study.studyId===route.study)?.studyTitle||'Исследование';
  const breadcrumbs=route.screen==='projects'?[{text:'Все проекты'}]:['studies','report'].includes(route.screen)?[{text:'Все проекты',href:'#/projects'},{text:'Lead Generation',href:'#/studies'},...(route.screen==='report'?[{text:'Отчёты'}]:[])]:[{text:'Все проекты',href:'#/projects'},{text:'Lead Generation',href:'#/studies'},{text:studyTitle}];
  return <ProductTheme><div className={layout.screen} data-live-project="leed-generation">
    <aside className={`${layout.sidebar} ${s.liveSidebar}`} data-round-footer={!['projects','studies','report'].includes(route.screen)}><div className={s.sidebarNavigation}><NavMenu studies={data?.studies||[]} selectedStudy={route.study} onSelectStudy={(study:string)=>{lastHeight.current=content.current?.getBoundingClientRect().height||480;navigate({study,screen:['projects','studies','report'].includes(route.screen)?'overview':['participant','replay'].includes(route.screen)?'participants':route.screen==='finding'?'findings':route.screen,scenario:''});}} Scope={route.screen==='projects'?'workspace':'study'} Active={screenRegistry[route.screen].navigation} ProjectLabel="ПРОЕКТ: LEAD GENERATION" StudyLabel="РАЗДЕЛЫ ИССЛЕДОВАНИЯ" ParticipantsLabel="Сессии" FooterText="Локальное рабочее пространство" onChange={value=>navigate({screen:navigationRoutes[String(value)]||'projects',link:'',item:'',scenario:''})}/></div>{!['projects','studies','report'].includes(route.screen)?<SidebarRoundControl key={route.study} data={scopedData} connectionError={error} refresh={()=>setRevision(value=>value+1)} onRoundFixed={study=>{setRevision(value=>value+1);navigate({study,screen:'launch',device:'all',scenario:''});}}/>:null}</aside>
    <div className={layout.workspace}><header className={layout.header}><EuiBreadcrumbs className={crumbs.root} aria-label="Хлебные крошки" breadcrumbs={breadcrumbs} responsive={false} max={0}/><span className={w.muted}>Локально · Lead Generation</span></header>
      <main className={`${layout.main} ${s.main}`}>
        {['participant','replay'].includes(route.screen)?<EuiLink className={s.backLink} href={`#/participants?device=${route.device}&study=${encodeURIComponent(route.study)}`}><DesignIcon type="arrowLeft"/>К сессиям</EuiLink>:null}
        <div className={w.between}><div className={w.heading}><h1>{title}</h1><p className={w.muted}>{['projects','studies','report'].includes(route.screen)?'Lead Generation':studyTitle}</p></div><div className={s.actions} ref={setHeaderActions}>{project&&['setup','launch'].includes(route.screen)?<OpenInterfaceButton url={project.url}/>:null}</div></div>
        {error?<EuiCallOut color="danger" title="Нет связи со сборщиком"><p>{error}</p><ProductButton Kind="Secondary" onClick={()=>setRevision(x=>x+1)}>Повторить</ProductButton></EuiCallOut>:null}
        <div ref={content} className={s.studyContent} aria-busy={!scopedData} style={!scopedData?{minHeight:lastHeight.current}:undefined}>{!scopedData?<div className={s.studyLoading} role="status"><EuiLoadingSpinner size="l"/><p>{error?'Запустите локальные серверы проекта.':'Загружаем исследование…'}</p></div>:<>
          {!map&&!['projects','studies','setup','launch','report'].includes(route.screen)?<div className={s.toolbar}><ProductDropdown label="Размер экрана" value={route.device} options={[{value:'all',label:'Все размеры экрана'},{value:'desktop',label:'От 768 px'},{value:'mobile',label:'До 768 px'}]} onChange={value=>navigate({device:value as 'all'|'desktop'|'mobile'})}/><span className={w.muted}>{project?.enabled?'Сбор включён':'Сбор приостановлен'} · {scopedData.total.lastAt?`последнее действие ${new Date(scopedData.total.lastAt).toLocaleString('ru-RU')}`:'ожидаем первое посещение'}</span></div>:null}
          {map?<LocalHeatmap key={route.study} refreshRevision={revision}/>:<LiveViews key={route.study} data={scopedData} refresh={()=>setRevision(x=>x+1)} headerActions={headerActions}/>}
          <p className={s.footer}>Данные Lead Generation сохраняются на этом компьютере. <EuiLink href={`#/launch?study=${encodeURIComponent(route.study)}`}>Проверка и запуск</EuiLink></p>
        </>}</div>
      </main>
    </div>

  </div></ProductTheme>;
}

