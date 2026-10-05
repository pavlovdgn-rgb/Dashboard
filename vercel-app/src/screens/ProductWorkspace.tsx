import { WorkspaceBreadcrumbs } from './WorkspaceBreadcrumbs';
import { NavMenu, ProductButton } from '../components';
import { ProductTheme } from '../tokens/ProductTheme';
import { useResearch } from '../data/researchStore';
import { ResultsWorkspace } from '../pages/ResultsOverview';
import { navigationRoutes, screenRegistry } from './registry';
import { useWireRoute } from './useWireRoute';
import { SetupScreens } from './SetupScreens';
import { AnalysisScreens } from './AnalysisScreens';
import { ParticipantSession } from './ParticipantSession';
import { Card, AsyncButton } from './WorkspaceUI';
import layout from '../pages/ResultsOverview.module.css';
import s from './Workspace.module.css';
import { LiveWorkspace } from '../live/LiveWorkspace';
export function ProductWorkspace() {
  const {route,navigate}=useWireRoute();const store=useResearch();
  if(store.live)return <LiveWorkspace/>;
  if(['overview','participants','report'].includes(route.screen))return <ResultsWorkspace/>;
  if(route.screen==='session')return <ProductTheme><ParticipantSession/></ProductTheme>;
  if(route.screen==='login')return <ProductTheme><header className={s.card}>UX-Lab</header><main className={s.login}><Card><p>UX-Lab</p><h1>Вход в рабочее пространство</h1><p>Доступ для коллег вашей команды. Участники теста входят по приглашению без регистрации.</p><AsyncButton primary action={()=>navigate({screen:'projects'})}>Продолжить вход</AsyncButton><p className={s.muted}>Нет доступа? Обратитесь к коллеге, который настраивает сервис.</p></Card></main></ProductTheme>;
  return <ProductTheme><div className={layout.screen}><aside className={layout.sidebar}><NavMenu Scope={route.screen==='projects'?'workspace':route.screen==='studies'?'project':'study'} Active={screenRegistry[route.screen].navigation} ProjectLabel={`ПРОЕКТ: ${store.project.title.toUpperCase()}`} StudyLabel={`ИССЛЕДОВАНИЕ: ${store.study.title.toUpperCase()}`} onChange={value=>navigate({screen:navigationRoutes[String(value)]||'projects',item:''})}/></aside><div className={layout.workspace}><header className={layout.header}><WorkspaceBreadcrumbs/><ProductButton Kind="Tertiary" onClick={()=>navigate({screen:'login'})}>Выйти</ProductButton></header><main className={layout.main}><div className={s.heading}><h1>{screenRegistry[route.screen].title}</h1><p className={s.muted}>{route.screen==='projects'?'Рабочее пространство команды':store.study.title}</p></div>{['projects','studies','setup','task','criteria','launch','control'].includes(route.screen)?<SetupScreens key={store.study.id}/>:<AnalysisScreens/>}</main></div></div></ProductTheme>;
}
