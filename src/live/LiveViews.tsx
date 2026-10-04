import {ProjectReports} from './ProjectReports';
import {FunnelLastActions} from './FunnelLastActions';
import {OverviewMetrics} from './OverviewMetrics';
import { useEffect,useState } from 'react';
import { createPortal } from 'react-dom';
import { EuiCallOut,EuiLink,EuiTab,EuiTabs,EuiToolTip } from '@elastic/eui';
import {ProductAction} from '../components/_shared/ProductComponent';
import { ProductButton,ProductCheckbox } from '../components';
import { DesignIcon } from '../components/_shared/CatalogComponent';
import { SignalViewSwitch } from '../components/_shared/SignalViewSwitch';
import { ProductDropdown } from '../components/_shared/ProductDropdown';
import { Card,Empty,Field,Table } from '../screens/WorkspaceUI';
import { useWireRoute } from '../screens/useWireRoute';
import { CapturedHeatmap } from '../heatmap/CapturedHeatmap';
import { pageLabels,pagePaths,type ClickGroup } from '../heatmap/types';
import { liveApi } from './api';
import { SessionVideo } from './SessionVideo';
import { ScreenshotReplay } from './ScreenshotReplay';
import { ParticipantLink } from './ParticipantLink';
import { MetricRatio } from './MetricRatio';

import {ProjectList} from './ProjectList';
import {studyTasks} from './taskMetrics';
import {TaskOutcome,TaskSummary} from './TaskOutcome';
import {StudyScenario} from './StudyScenario';
import { CollectionControl } from './CollectionControl';
import { pageSignalMetrics } from './metrics';
import type { LiveSummary,LiveEvent,LiveFinding } from './types';
import w from '../screens/Workspace.module.css';
import s from './LiveWorkspace.module.css';

const pageName=(page:string)=>pageLabels[page]||page.replace(/^leed-/,'').replaceAll('-',' ');
const date=(time:number)=>new Date(time).toLocaleString('ru-RU');
const short=(id:string)=>id.slice(0,8);
type Props={data:LiveSummary;refresh:()=>void;headerActions?:HTMLElement|null};
function useMutation(refresh:()=>void){const [busy,setBusy]=useState(false),[error,setError]=useState('');return {busy,error,run:async(action:()=>Promise<unknown>)=>{if(busy)return;setBusy(true);setError('');try{await action();refresh();}catch(e){setError(e instanceof Error?e.message:'Не удалось сохранить.');}finally{setBusy(false);}}};}
function ErrorMessage({message}:{message:string}){return message?<EuiCallOut color="danger" title={message}/>:null;}
export function LiveViews(props:Props){const {route}=useWireRoute();switch(route.screen){
  case 'projects':case 'studies':return <ProjectList {...props}/>;
  case 'overview':return <Overview {...props}/>;
  case 'participants':return <Sessions {...props}/>;
  case 'participant':case 'replay':return <Timeline key={route.participant} {...props}/>;
  case 'funnel':return <Funnel {...props}/>;
  case 'signals':case 'findings':case 'finding':return <SignalsFindings {...props}/>;
  case 'report':return <ProjectReports {...props}/>;
  case 'setup':return <StudySetup {...props}/>;
  case 'launch':return <StudyLaunch {...props}/>;
  default:return <Empty>Этот раздел недоступен. Выберите раздел в боковом меню.</Empty>;
}}
function Overview({data,headerActions}:Props){const {navigate}=useWireRoute();return <>
  {headerActions?createPortal(<div className={s.reportAction}><ProductButton Kind="Primary" icon="document" onClick={()=>navigate({screen:'report',item:'create'})}>Отчёт PDF</ProductButton></div>,headerActions):null}
  <OverviewMetrics data={data}/>
  <p className={w.muted}>Сессия — посещение в одной вкладке, а не уникальный человек. {data.project.mode==='scenario'?'Исследование по сценарию: результат оценивается по заданному критерию.':'Режим свободного изучения: достижение целей не оценивается.'}</p>
  <TaskSummary data={data}/>
  {data.pages.length?<section className={s.analysisCard}><div className={s.analysisHeading}><h2>Активность по экранам</h2><p className={w.muted}>Выберите экран, чтобы посмотреть тепловую карту.</p></div><div className={`${s.table} ${s.metricTable} ${s.activityTable}`}><Table label="Экраны проекта" headers={['Экран','Сессии','Посещения','Клики','']}>{data.pages.map(page=><tr key={page.id}><td><EuiLink data-row-action onClick={()=>navigate({screen:'heatmap',item:`page:${page.id}`,link:''})}>{pageName(page.id)}</EuiLink></td><td>{page.sessions}</td><td>{page.visits}</td><td>{page.clicks}</td><td><span className={s.rowDestination}><DesignIcon type="arrowRight"/></span></td></tr>)}</Table></div></section>:<Empty>Откройте Lead Generation. Первое посещение появится здесь автоматически.</Empty>}

  <p className={w.muted}>Учёт посещений включён с момента полного подключения. Ранее собранные клики сохранены, но число старых посещений восстановить нельзя.</p>
</>;}
function Sessions({data}:Props){const {navigate,route}=useWireRoute();const [search,setSearch]=useState(''),[page,setPage]=useState(0);const ids=route.item.startsWith('ids:')?route.item.slice(4).split(','):null;const filtered=data.sessions.filter(row=>(!ids||ids.includes(row.id))&&row.id.includes(search.trim()));const size=8,max=Math.max(1,Math.ceil(filtered.length/size)),index=Math.min(page,max-1),rows=filtered.slice(index*size,(index+1)*size);return <>
  <div className={w.between}><div className={s.search}><Field label="Поиск сессии" type="Search" value={search} onChange={value=>{setSearch(value);setPage(0);}}/></div><span>{filtered.length} сессий</span></div>
  {ids?<ProductButton Kind="Tertiary" onClick={()=>navigate({item:''})}>Все сессии</ProductButton>:null}
  <div className={`${s.table} ${s.tableViewport}`}>{rows.length?<Table label="Сессии Lead Generation" headers={['Сессия','Последнее действие','Экранов','Кликов','Запись','Задания']}>{rows.map(row=><tr key={row.id}><td><EuiLink data-row-action onClick={()=>navigate({screen:'participant',participant:row.id,item:''})}>{short(row.id)}</EuiLink></td><td>{date(row.lastAt)}</td><td>{row.pages.length}</td><td>{row.clicks}</td><td>{[row.recordings?`Видео · ${row.recordings}`:'',row.frames?`Снимки · ${row.frames}`:''].filter(Boolean).join(' · ')||'Нет записи'}</td><td><TaskOutcome task={row.task}/></td></tr>)}</Table>:<Empty>Сессии не найдены.</Empty>}</div>
  <div className={w.between}><p className={w.muted}>Откройте сессию, чтобы посмотреть видео теста и моменты кликов.</p><nav className={s.pagination} aria-label="Страницы сессий"><ProductAction kind="Secondary" label="Предыдущая страница" icon="arrowLeft" state={index===0?'Disabled':'Default'} onClick={()=>setPage(index-1)}/><span aria-live="polite">{index+1} из {max}</span><ProductAction kind="Secondary" label="Следующая страница" icon="arrowRight" state={index+1>=max?'Disabled':'Default'} onClick={()=>setPage(index+1)}/></nav></div>
</>;}
function Timeline({data,refresh}:Props){const {route}=useWireRoute();const [events,setEvents]=useState<LiveEvent[]>([]),[error,setError]=useState(''),[selected,setSelected]=useState(''),[loading,setLoading]=useState(true),[editor,setEditor]=useState(false);useEffect(()=>{let cancelled=false;liveApi<{events:LiveEvent[]}>(`/session?id=${encodeURIComponent(route.participant)}`).then(result=>{if(!cancelled){setEvents(result.events);setError('');}}).catch(e=>{if(!cancelled)setError(String(e));}).finally(()=>{if(!cancelled)setLoading(false);});return()=>{cancelled=true;};},[route.participant,data.total.lastAt]);
  const found=events.findIndex(event=>event.id===selected),requested=route.time?events.findIndex(event=>event.timestamp>=route.time):-1,index=found>=0?found:Math.max(0,requested),event=events[index];
  const group:ClickGroup|undefined=event?{layout:event.id,page:event.page,path:pagePaths[event.page],version:event.version||'leed-local-v2',vw:event.vw,vh:event.vh,rw:event.vw,rh:event.vh,clicks:event.kind==='click'?1:0,sessions:1,context:event.context}:undefined;
  return <><ErrorMessage message={error}/><TaskOutcome details task={data.sessions.find(item=>item.id===route.participant)?.task}/><div className={w.between}><p>Сессия {route.participant}</p><EuiLink href={`#/heatmap?session=${encodeURIComponent(route.participant)}&study=${encodeURIComponent(route.study)}`}>Тепловая карта этой сессии</EuiLink></div><SessionVideo session={route.participant} events={events} requestedTime={route.time} hideIfEmpty={data.project.recordingMode==='screenshots'||Boolean(data.sessions.find(item=>item.id===route.participant)?.frames)}/>{data.project.recordingMode==='screenshots'||data.sessions.find(item=>item.id===route.participant)?.frames?<ScreenshotReplay key={route.participant} session={route.participant} requestedTime={route.time}/>:null}<details className={s.history}><summary>Снимки и события · {events.length}</summary>
    {!event?<Empty>{loading?'Загружаем события…':'В этой сессии нет сохранённых событий.'}</Empty>:<><div className={w.between}><h2>{pageName(event.page)} · {date(event.timestamp)}</h2><ProductButton Kind="Secondary" onClick={()=>setEditor(true)}>Сохранить наблюдение</ProductButton></div><div className={w.columns}><div className={w.stack}>
      {!event.context?.snapshot?<EuiCallOut color="warning" title="Исходный снимок не сохранился"><p>Показан текущий интерфейс; положение старых элементов могло отличаться.</p></EuiCallOut>:null}
      <CapturedHeatmap key={event.id} group={group!} points={event.kind==='click'?[{x:event.x!,y:event.y!,target:event.target||'',count:1,sessions:[event.session],element:event.context?.element}]:[]}/>
      <div className={s.actions}><ProductButton Kind="Secondary" State={index===0?'Disabled':'Default'} icon="arrowLeft" onClick={()=>setSelected(events[index-1].id)}>Предыдущее</ProductButton><span>{index+1} из {events.length}</span><ProductButton Kind="Secondary" State={index===events.length-1?'Disabled':'Default'} iconRight="arrowRight" onClick={()=>setSelected(events[index+1].id)}>Следующее</ProductButton></div>
    </div><div className={s.events} aria-label="Действия сессии">{events.map(item=><button className={s.event} key={item.id} aria-pressed={item.id===event.id} onClick={()=>setSelected(item.id)}>{item.kind==='visit'?'Открыт экран':item.context?.element?.label||'Клик по области'}<small>{pageName(item.page)} · {new Date(item.timestamp).toLocaleTimeString('ru-RU')}</small></button>)}</div></div></>}
    </details>
    {editor&&event?<FindingForm data={data} refresh={refresh} context={{session:event.session,page:event.page,timestamp:event.timestamp}} onClose={()=>setEditor(false)}/>:null}
  </>;
}
function StudySetup({data,refresh}:Props){
  const [title,setTitle]=useState(data.project.studyTitle),[saved,setSaved]=useState(false);
  const mutation=useMutation(refresh);
  return <>
    <Card><div className={w.between}><div className={w.heading}><h2>Тестируемый интерфейс</h2><p>Lead Generation · подключённая локальная версия</p></div></div><p className={w.muted}>{data.project.url}</p><EuiLink href="/?screen=connections">Проверить подключение другого интерфейса</EuiLink></Card>
    <Card><h2>Название исследования</h2><div className={s.form}><Field label="Название исследования" value={title} onChange={value=>{setTitle(value);setSaved(false);}}/><ProductButton Kind="Secondary" State={mutation.busy?'Loading':!title.trim()||title.trim()===data.project.studyTitle?'Disabled':'Default'} onClick={()=>{setSaved(false);void mutation.run(async()=>{await liveApi('/config',{studyTitle:title.trim()});setSaved(true);});}}>Сохранить название</ProductButton></div>{saved?<p role="status">Название сохранено</p>:null}<ErrorMessage message={mutation.error}/></Card>
    <StudyScenario config={data.project} refresh={refresh}/><StudyParameters data={data} refresh={refresh}/>
    <EuiLink href={`#/launch?study=${encodeURIComponent(data.project.studyId)}`}>К проверке и запуску</EuiLink>
  </>;
}
const parameterLabels={collectVisits:'Собирать посещения экранов',collectClicks:'Собирать клики',allowVideo:'Разрешить видеозапись теста'};
type Parameters=Pick<LiveSummary['project'],keyof typeof parameterLabels|'recordingMode'>;
function StudyParameters({data,refresh}:Props){
  const [draft,setDraft]=useState<Parameters|null>(null),[saved,setSaved]=useState(false);
  const mutation=useMutation(refresh),values=draft??data.project;
  const keys=Object.keys(parameterLabels) as (keyof typeof parameterLabels)[];
  const dirty=values.recordingMode!==data.project.recordingMode||keys.some(key=>values[key]!==data.project[key]);
  return <Card><h2>Параметры исследования</h2><p>Выберите данные, которые будут сохраняться при прохождении исследования.</p>
    <div className={s.form}><ProductDropdown appearance="field" label="Формат записи" value={values.recordingMode} disabled={mutation.busy} options={[{value:'video',label:'Видео'},{value:'screenshots',label:'Скриншоты действий'}]} onChange={value=>{setSaved(false);setDraft({...values,recordingMode:value as Parameters['recordingMode']});}}/>{keys.filter(key=>key!=='allowVideo'||values.recordingMode==='video').map(key=><ProductCheckbox key={key} Label={parameterLabels[key]} Value={values[key]?'On':'Off'} State={mutation.busy?'Disabled':'Default'} onChange={value=>{setSaved(false);setDraft({...values,[key]:Boolean(value)});}}/>)}</div>
    <p className={w.muted}>Клики нужны для тепловой карты и сигналов затруднений, посещения — для маршрутов и воронки. Формат записи выбирается отдельно.</p>
    {values.recordingMode==='video'&&!values.collectVisits&&!values.collectClicks&&!values.allowVideo?<p role="status">Все виды сбора отключены: новые данные теста не будут записываться.</p>:null}
    <div className={s.actions}><ProductButton Kind="Secondary" State={mutation.busy?'Loading':dirty?'Default':'Disabled'} onClick={()=>{setSaved(false);void mutation.run(async()=>{const result=await liveApi<Parameters>('/config',{collectVisits:values.collectVisits,collectClicks:values.collectClicks,allowVideo:values.allowVideo,recordingMode:values.recordingMode});setDraft(result);setSaved(true);});}}>Сохранить параметры</ProductButton></div>
    {saved?<p role="status">Параметры сохранены</p>:null}<ErrorMessage message={mutation.error}/>
    <p>{values.recordingMode==='screenshots'?'Снимки сохраняются автоматически при переходах, нажатиях и изменениях интерфейса, даже если сбор кликов и посещений отключён. Значения полей скрыты. Разрешение на захват экрана не требуется.':'Видео участник запускает вручную и выбирает вкладку в окне браузера. Запись без звука.'}</p><p className={w.muted}>Открытые вкладки применят изменения в течение нескольких секунд. Отключение видео или переход к снимкам завершит текущую видеозапись и сохранит её. Ранее собранные данные и очередь отправки сохраняются.</p>
  </Card>;
}
function StudyLaunch({data,refresh}:Props){
  const [checked,setChecked]=useState('');const mutation=useMutation(refresh);
  return <>
    <Card><div className={w.between}><div className={w.heading}><h2>Проверка подключения</h2><p>Lead Generation · локальный сборщик</p></div></div><div className={s.actions}><ProductButton Kind="Secondary" State={mutation.busy?'Disabled':'Default'} onClick={()=>{setChecked('');void mutation.run(async()=>{await liveApi('/config');setChecked(new Date().toLocaleTimeString('ru-RU'));});}}>Проверить подключение</ProductButton></div>{checked?<EuiCallOut color="success" title="Сервер сбора доступен"><p>Проверено в {checked}. Чтобы проверить поступление данных, включите сбор, откройте интерфейс и нажмите на любой элемент. Ниже обновятся счётчики и время последнего действия.</p></EuiCallOut>:null}<ErrorMessage message={mutation.error}/></Card>
    <CollectionControl enabled={data.project.enabled} refresh={refresh}/>
    <ParticipantLink url={data.project.url} enabled={data.project.enabled}/>
    <Card><h2>Поступление данных</h2><p>Сохранено: {data.total.visits} посещений · {data.total.clicks} кликов · {data.total.sessions} сессий</p><p>{data.total.lastAt?`Последнее действие: ${date(data.total.lastAt)}`:'Действий пока нет. После включения сбора откройте интерфейс и выполните первое действие.'}</p><p className={w.muted}>Показатели обновляются автоматически. Время последнего действия относится к сохранённым событиям и не подтверждает, что участник сейчас онлайн.</p></Card>
    <Card><h2>Инструкция для участника</h2>{data.project.mode==='scenario'?<ol className={s.instructions}>{studyTasks(data.project).map(task=><li key={task.id}><strong>{task.title}</strong> — {task.instruction}</li>)}</ol>:null}<ol className={s.instructions}><li>Откройте Lead Generation и изучайте интерфейс. При включённом сборе выбранные в настройках данные сохраняются автоматически.</li>{data.project.recordingMode==='screenshots'?<li>Снимки экрана и действий сохраняются автоматически. Нажатый элемент будет выделен в записи. Значения полей скрыты.</li>:data.project.allowVideo?<><li>Для видеозаписи нажмите «Начать запись теста» в Lead Generation и выберите вкладку в окне браузера.</li><li>В конце нажмите «Завершить запись» и дождитесь подтверждения сохранения.</li></>:<li>Видеозапись отключена организатором. Тест можно пройти без видео.</li>}</ol>{data.project.recordingMode==='video'&&data.project.allowVideo?<p className={w.muted}>Видео записывается без звука и содержит всё видимое, включая текст полей. Маскирование применяется только к отдельным снимкам тепловой карты.</p>:null}<p className={w.muted}>Сейчас тест доступен локально на этом компьютере.</p></Card>
  </>;
}
function Funnel({data,refresh}:Props){const [steps,setSteps]=useState(data.project.funnel.length?data.project.funnel:['','']);const mutation=useMutation(refresh);const {navigate}=useWireRoute();const options=Object.keys(pageLabels).filter(id=>id.startsWith('leed-')).map(value=>({value,label:pageName(value)}));return <>
  <Card><div className={s.funnelEditor}><div className={s.funnelExplanation}><h2>Последовательность экранов</h2><p className={w.muted}>Задайте порядок посещений. Сессия должна пройти экраны последовательно; промежуточные переходы допустимы.</p><p className={s.funnelStepCount}>{steps.length} {steps.length<5?'шага':'шагов'}</p></div><div className={s.funnelFields}>
    {steps.map((value,index)=><div className={s.funnelStep} key={index}>
      <ProductDropdown appearance="field" label={`Шаг ${index+1}`} value={value} disabled={mutation.busy} placeholder="Выберите экран" options={options} onChange={next=>setSteps(old=>old.map((item,i)=>i===index?next:item))}/>
      <div className={`${s.taskIconActions} ${s.funnelStepDelete}`}><EuiToolTip content={steps.length<=2?'В воронке должно быть минимум два шага':`Удалить шаг ${index+1}`}><span><ProductAction kind="Tertiary" icon="trash" label={`Удалить шаг ${index+1}`} state={mutation.busy||steps.length<=2?'Disabled':'Default'} onClick={()=>setSteps(old=>old.filter((_,i)=>i!==index))}/></span></EuiToolTip></div>
    </div>)}
    <div className={s.funnelActions}><ProductButton Kind="Tertiary" State={mutation.busy||steps.length>=8?'Disabled':'Default'} onClick={()=>setSteps(old=>[...old,''])}>Добавить шаг</ProductButton><ProductButton Kind="Primary" State={mutation.busy?'Loading':steps.some(value=>!value)?'Disabled':'Default'} onClick={()=>void mutation.run(()=>liveApi('/config',{funnel:steps}))}>Применить</ProductButton></div>
    <ErrorMessage message={mutation.error}/></div></div></Card>
  {data.funnel.length?<><section className={s.analysisCard}><div className={s.analysisHeading}><h2>Прохождение шагов</h2><p className={w.muted}>{data.funnel[0].sessions?`База расчёта: ${data.funnel[0].sessions} сессий на первом шаге.`:'Нет данных: первый шаг пока не посетила ни одна сессия.'}</p></div><div className={`${s.table} ${s.metricTable} ${s.funnelTable}`}><Table label="Воронка переходов" headers={['Шаг','Дошли','От первого шага','Потеря на шаге','Сессии']}>{data.funnel.map((step,index)=><tr key={index}><td>{index+1}. {pageName(step.page)}</td><td>{step.sessions}</td><td><MetricRatio value={step.sessions} total={data.funnel[0].sessions} label={`От первого шага: шаг ${index+1}`}/></td><td>{index&&data.funnel[0].sessions?`−${data.funnel[index-1].sessions-step.sessions}`:'—'}</td><td data-row-action={step.sessions?true:undefined}><ProductButton Kind="Tertiary" State={step.sessions?'Default':'Disabled'} onClick={()=>navigate({screen:'participants',item:`ids:${step.sessionIds.join(',')}`})}>Посмотреть</ProductButton></td></tr>)}</Table></div></section><p className={s.metricNote}>Все шкалы рассчитаны от первого шага: сессии на шаге / сессии на первом шаге × 100. Потеря — число сессий, не перешедших с предыдущего шага.</p></>:<Empty>Выберите минимум два экрана и примените порядок.</Empty>}
  <FunnelLastActions steps={data.funnel}/>
  <p className={w.muted}>Для старых данных присутствие на экране подтверждается кликом. Воронка показывает последовательность экранов, а не успешность бизнес-задачи.</p>
</>;}
function FindingForm({refresh,context,onClose}:{data:LiveSummary;refresh:()=>void;context?:Partial<LiveFinding>;onClose:()=>void}){const [title,setTitle]=useState(''),[observation,setObservation]=useState('');const mutation=useMutation(refresh);return <Card><h2>Новое наблюдение</h2><div className={s.form}><Field label="Название" value={title} onChange={setTitle}/><Field label="Что наблюдали" type="Textarea" value={observation} onChange={setObservation}/><ErrorMessage message={mutation.error}/><div className={s.actions}><ProductButton Kind="Primary" State={mutation.busy?'Loading':!title.trim()||!observation.trim()?'Disabled':'Default'} onClick={()=>void mutation.run(async()=>{await liveApi('/findings',{title,observation,...context});onClose();})}>Сохранить</ProductButton><ProductButton Kind="Tertiary" onClick={onClose}>Отмена</ProductButton></div></div></Card>;}
function SignalsFindings({data,refresh}:Props){const {route,navigate}=useWireRoute();const findings=route.screen!=='signals';const [editor,setEditor]=useState(false),[pages,setPages]=useState(false);const mutation=useMutation(refresh);return <>
  <EuiTabs aria-label="Сигналы и находки"><EuiTab isSelected={!findings} onClick={()=>navigate({screen:'signals'})}>Сигналы</EuiTab><EuiTab isSelected={findings} onClick={()=>navigate({screen:'findings'})}>Находки · {data.findings.length}</EuiTab></EuiTabs>
  {findings?<><div className={w.between}><p>Наблюдения команды по реальным данным проекта.</p><ProductButton Kind="Primary" onClick={()=>setEditor(true)}>Добавить находку</ProductButton></div>{editor?<FindingForm data={data} refresh={refresh} onClose={()=>setEditor(false)}/>:null}{data.findings.length?data.findings.map(item=><Card key={item.id}><h2>{item.title}</h2><p>{item.observation}</p><div className={s.actions}>{item.session?<EuiLink onClick={()=>navigate({screen:'replay',participant:item.session!,time:item.timestamp||0})}>Посмотреть действие</EuiLink>:null}<ProductCheckbox Label="Проверено" Value={item.resolved?'On':'Off'} onChange={value=>void mutation.run(()=>liveApi('/findings',{id:item.id,resolved:Boolean(value)}))}/></div></Card>):<Empty>Пока нет находок. Добавьте наблюдение или сохраните его из истории сессии.</Empty>}</>:<>
    <Card><h2>Повторные клики</h2><p>Три и более нажатия за секунду в радиусе 24 px на одном экране. Это повод изучить контекст, а не доказательство проблемы.</p></Card><SignalViewSwitch pages={pages} onChange={setPages}/>
    {pages?<><section className={s.analysisCard}><div className={s.analysisHeading}><h2>Сессии с повторными кликами</h2><p className={w.muted}>Доля сессий с сигналом среди сессий, посетивших экран.</p></div>{data.pages.length?<div className={`${s.table} ${s.metricTable} ${s.pageSignalsTable}`}><Table label="Сигналы по страницам" headers={['Экран','Сессии с сигналом','Доля сессий']}>{pageSignalMetrics(data).map(page=><tr key={page.id}><td>{page.affectedSessions.length?<EuiLink data-row-action onClick={()=>navigate({screen:'participants',item:`ids:${page.affectedSessions.join(',')}`})}>{pageName(page.id)}</EuiLink>:pageName(page.id)}</td><td>{page.affectedSessions.length} из {page.sessions}</td><td><MetricRatio value={page.affectedSessions.length} total={page.sessions} label={`Доля сессий с сигналом: ${pageName(page.id)}`}/></td></tr>)}</Table></div>:<Empty>Нет данных по экранам в этой выборке.</Empty>}</section><p className={s.metricNote}>Сессии с сигналом / сессии, посетившие экран × 100. Несколько серий повторных кликов в одной сессии учитываются один раз на экран.</p><p className={w.muted}>При малой выборке сравнивайте также числа, а не только проценты.</p></>:!data.signals.length?<Empty>Повторных кликов в этой выборке пока нет.</Empty>:<div className={`${s.table} ${s.signalTable}`}><Table label="Сигналы" headers={['Сигнал','Экран','Сессия','Время']}>{data.signals.map(item=><tr key={item.id}><td>{item.label}<small>{item.target}</small></td><td>{pageName(item.page)}</td><td><EuiLink data-row-action onClick={()=>navigate({screen:'replay',participant:item.session,time:item.timestamp})}>{short(item.session)}</EuiLink></td><td>{date(item.timestamp)}</td></tr>)}</Table></div>}
  </>}<ErrorMessage message={mutation.error}/>
</>;}
