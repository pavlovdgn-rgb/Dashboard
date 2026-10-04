import { WorkspaceBreadcrumbs } from '../screens/WorkspaceBreadcrumbs';
import { useState } from 'react';
import { EuiModal, EuiModalHeader, EuiModalHeaderTitle, EuiModalBody, EuiModalFooter, EuiCallOut, EuiToast } from '@elastic/eui';
import { NavMenu, ProductButton, SummaryMetric, ScenarioTable, ParticipantsTable } from '../components';
import { ProductDropdown } from '../components/_shared/ProductDropdown';
import { ProductTheme } from '../tokens/ProductTheme';
import { ResearchProvider } from '../data/ResearchProvider';
import { useResearch, type MockOptions } from '../data/researchStore';
import { deviceLabels, selectParticipants, selectScenarios, type Device } from '../data/research';
import { screenRegistry, navigationRoutes } from '../screens/registry';
import { ProductWorkspace } from '../screens/ProductWorkspace';
import { FreeResults } from '../screens/FreeResults';
import { useWireRoute } from '../screens/useWireRoute';
import { ReportContent } from '../screens/ReportContent';
import type { ParticipantFilters } from '../components/_shared/ParticipantsTableExample';
import styles from './ResultsOverview.module.css';

/** Existing trial composition, wired to a shared mock store and browser history. */
export function ResultsOverview(options:MockOptions) {
  return <ResearchProvider key={`${options.failure}-${options.empty}`} {...options}><ProductWorkspace/></ResearchProvider>;
}
export function ResultsWorkspace() {
  const store=useResearch();
  const study={...store.study,project:store.project.title,scenarioSummary:store.study.tasks.map(x=>x.title).join('\n')};
  const scenarioDefinitions=store.study.tasks;
  const {route,navigate}=useWireRoute();
  const [notice,setNotice]=useState('');
  const [toast,setToast]=useState('');
  const [error,setError]=useState('');
  const [navRevision,setNavRevision]=useState(0);
  const scenarios=selectScenarios(store.observations,route.device,scenarioDefinitions);
  const participants=selectParticipants(store.observations,route.device);
  const selected=scenarios.find(row=>row.id===route.scenario);
  const incomplete=participants.filter(row=>row.coverage!=='Complete').length;
  const complete=participants.length-incomplete;
  const hasData=participants.length>0;
  const loading=store.pending==='refresh';
  const metricState=loading?'Loading':hasData?'Ready':'NoData';
  const scopeParticipants=selectParticipants(store.observations,route.device,route.scenario);
  const scopedBySource=route.item.startsWith('ids:')?scopeParticipants.filter(row=>route.item.slice(4).split(',').includes(row.id)):scopeParticipants;
  const tableParticipants=route.coverage==='partial'?scopedBySource.filter(row=>row.coverage!=='Complete'):scopedBySource;
  const participantScope=`${study.id}-${route.device}-${route.scenario}-${route.coverage}-${route.item}`;
  const closeDialog=()=>{if(notice){setNotice('');setNavRevision(value=>value+1);}else navigate({screen:'overview',coverage:'all',reportId:''},true);};
  const go=(target:string)=>{
    navigate({screen:navigationRoutes[target]||'overview',coverage:'all',item:''});
  };
  const refresh=async()=>{
    setError('');setToast('');
    try {await store.refresh();setToast('Результаты обновлены');}
    catch(cause){setError(cause instanceof Error?cause.message:'Не удалось обновить результаты.');}
  };
  const dialogTitle=notice||(route.screen==='participants'&&route.coverage==='partial'?'Участники с неполными данными':screenRegistry[route.screen].title);
  return <ProductTheme><div className={styles.screen} data-screen="results-overview">
    <aside className={styles.sidebar}><NavMenu key={navRevision} Active={screenRegistry[route.screen].navigation} FooterText="● Готово к тестированию" onChange={value=>go(String(value))}/></aside>
    <div className={styles.workspace}>
      <header className={styles.header}><WorkspaceBreadcrumbs/><ProductButton Kind="Tertiary" onClick={()=>setNotice('Коллега')}>Коллега</ProductButton></header>
      <main className={styles.main}>
        <div className={styles.heading}><div><h1>Обзор результатов</h1><p>Сценарии исследования и результаты участников</p></div><div className={styles.headingActions}><ProductButton Kind="Secondary" State={loading?'Loading':store.pending?'Disabled':'Default'} onClick={()=>void refresh()}>Обновить результаты</ProductButton><ProductButton Kind="Primary" icon="document" onClick={()=>go('PDF')}>Отчёт PDF</ProductButton></div></div>
        {error?<div role="alert"><EuiCallOut color="danger" title={error}><ProductButton Kind="Secondary" onClick={()=>void refresh()}>Повторить обновление</ProductButton></EuiCallOut></div>:null}
        <div className={styles.context}><ProductDropdown label="Устройство" value={route.device} onChange={value=>navigate({device:value as Device,scenario:'',reportId:''})} options={Object.entries(deviceLabels).map(([value,label])=>({value,label}))}/><p>Режим: {study.mode==='free'?'свободное изучение':'задания'}</p><span role="status">{loading?'Обновляем результаты…':`${study.status==='active'?'Сбор идёт':study.status==='finished'?'Сбор завершён':'Черновик'} · обновлено ${store.updatedAt}`}</span></div>
        {study.mode==='free'?<FreeResults/>:<><div className={styles.summary}>
          <SummaryMetric Label="Сценариев" Value={String(scenarioDefinitions.length)} Hint="В исследовании · режим заданий" Detail={study.scenarioSummary} ShowBadge={false} ShowProgress={false} ShowLink={false}/>
          <SummaryMetric State={metricState} Label="Участников" Value={String(participants.length)} Hint="Уникальные участники в текущей выборке" Detail={hasData?`${complete} с полными данными\n${incomplete} с неполными данными`:'Нет наблюдений в текущей выборке.\nДоли пока не рассчитываются.'} Badge={`${hasData?Math.round(100*complete/participants.length):0}% полные`} ShowBadge={hasData} ShowProgress={hasData} ShowLink={false}/>
          <SummaryMetric State={metricState} Label="С неполными данными" Value={`${incomplete} из ${participants.length}`} Hint="Требуют проверки полноты данных" Detail={hasData?'Часть событий или записи отсутствует.\nЭто не означает неуспех задания.':'Нет наблюдений в текущей выборке.\nДоли пока не рассчитываются.'} Badge={`${hasData?Math.round(100*incomplete/participants.length):0}% выборки`} BadgeTone="warning" ShowBadge={hasData} ShowProgress={false} ShowLink={hasData&&!loading} onClick={()=>navigate({screen:'participants',coverage:'partial',scenario:''})}/>
        </div>
        <ScenarioTable overview className={styles.scenarios} State={loading?'Loading':hasData?'OverviewUnselected':route.device==='mobile'?'FilteredEmpty':'Empty'} rows={scenarios} selectedId={route.scenario} onChange={value=>navigate({scenario:String(value)},true)} onRetry={()=>navigate({device:'all',scenario:''})}/>
        <section className={styles.analysis} aria-label="Анализ сценария">{selected?<><h2>{selected.title}</h2><p>Выбранный сценарий · {selected.started} участников начали · {selected.assessed} попыток оценены</p><div className={styles.analysisActions}>{([['Heatmap','Тепловая карта'],['Funnel','Воронка'],['Participants','Участники'],['Signals','Сигналы затруднений']] as const).map(([id,title])=><ProductButton key={id} Kind="Secondary" onClick={()=>go(id)}>{title}</ProductButton>)}</div></>:<><h2>Выберите сценарий в списке выше</h2><p>Откроются тепловая карта, воронка, участники и сигналы затруднений.</p></>}</section></>}
      </main>
    </div>
    {notice||route.screen!=='overview'?<EuiModal className={styles.dialog} onClose={closeDialog} aria-labelledby="overview-dialog-title"><EuiModalHeader className={styles.noPrint}><EuiModalHeaderTitle id="overview-dialog-title">{dialogTitle}</EuiModalHeaderTitle></EuiModalHeader><EuiModalBody>
      {notice?<><p>Рабочее пространство команды · демонстрационный сеанс</p><ProductButton Kind="Secondary" onClick={()=>navigate({screen:'login'})}>Выйти</ProductButton></>:route.screen==='participants'?<div className={styles.report}>
        <p>{selected?.title||scenarioDefinitions[0]?.title||'Свободное изучение'} · {deviceLabels[route.device]}</p>
        {route.coverage==='partial'?<ProductButton Kind="Tertiary" onClick={()=>navigate({coverage:'all'})}>Все участники</ProductButton>:null}
        <ParticipantsTable key={participantScope} rows={tableParticipants} filters={store.participantFilters[participantScope]} onFiltersChange={value=>store.setParticipantFilters(previous=>({...previous,[participantScope]:value as ParticipantFilters}))} State={loading?'Loading':tableParticipants.length?'Ready':'Empty'} onOpenRecording={(value:unknown)=>{const entry=value as {participantId:string;attempt:number};navigate({screen:'replay',participant:entry.participantId,time:0});}}/>
      </div>:<ReportContent route={route} onSaved={(reportId,created)=>{navigate({reportId},true);if(created)setToast('Отчёт сформирован');}}/>}
    </EuiModalBody><EuiModalFooter className={styles.noPrint}><ProductButton Kind="Secondary" onClick={closeDialog}>Вернуться к результатам</ProductButton></EuiModalFooter></EuiModal>:null}
    {toast?<div className={`${styles.toast} ${styles.noPrint}`} role="status"><EuiToast title={toast} color="success" iconType="checkInCircleFilled" onClose={()=>setToast('')}/></div>:null}
  </div></ProductTheme>;
}
