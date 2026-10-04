import { useState } from 'react';
import { createPortal } from 'react-dom';
import { EuiCallOut } from '@elastic/eui';
import { ProductButton, ProductCheckbox, ScenarioTable, HeatmapLegend } from '../components';
import { Storefront } from './ParticipantSession';
import { useResearch } from '../data/researchStore';
import { deviceLabels, scenarioDefinitions, selectParticipants, type ReportSection, type SavedReport } from '../data/research';
import type { WireRoute } from './useWireRoute';
import styles from '../pages/ResultsOverview.module.css';
import workspaceStyles from './Workspace.module.css';

function ReportSnapshot({report}:{report:SavedReport}) {
  return <>
    <p role="status">Отчёт сформирован · {new Date(report.createdAt).toLocaleString('ru-RU')}</p>
    {report.sections.includes('summary')?<section><h3>Сводные показатели</h3><p>Участников: {report.participants.length} · Сценариев с результатами: {report.scenarios.length}</p><p>Полные данные: {report.participants.filter(x=>x.coverage==='Complete').length}. Неполные данные: {report.participants.filter(x=>x.coverage==='Partial').length}.</p><p>Полнота данных и достижение цели — разные показатели.</p></section>:null}
    {report.sections.includes('heatmap')?<section><h3>Карта выбранной страницы · /products/backpack</h3><div className={workspaceStyles.heatmap}><Storefront readOnly/>{[[65,72],[15,32],[80,55]].map(([left,top],i)=><span key={i} aria-hidden="true" className={workspaceStyles.hotspot} style={{left:`${left}%`,top:`${top}%`}}/>)}</div><HeatmapLegend SampleBase={`${report.participants.length} участников · демонстрационная выборка`}/><p>Снимок страницы 1. Области кликов относятся к демонстрационному интерфейсу.</p></section>:null}
    {report.sections.includes('signals')?<section><h3>Сигналы и полнота данных</h3><p>Сигнал — повод посмотреть запись; он не доказывает причину затруднения.</p><div className={styles.reportTable}><table><thead><tr><th>Участник</th><th>Сигналов</th><th>Данные</th></tr></thead><tbody>{report.participants.map(row=><tr key={row.id}><td>{row.id}</td><td>{row.signals}</td><td>{row.coverage==='Complete'?'Полные':row.coverage==='Partial'?'Неполные':'Недоступны'}</td></tr>)}</tbody></table></div></section>:null}
    {report.sections.includes('findings')?<section><h3>Находки и выводы команды · {report.findings.length}</h3>{report.findings.map(f=><section key={f.id}><h3>{f.title}</h3><p>Наблюдение: {f.observation}</p><p>Приоритет: {f.priority} · {f.status}</p><p>Предположение: {f.hypothesis||'Не указано'}</p><p>Как проверим: {f.verification||'Не задано'}</p><p>Доказательства: {f.evidence.map(e=>`${e.participantId} / попытка ${e.attempt} / ${Math.floor(e.time/60)}:${String(e.time%60).padStart(2,'0')}`).join(', ')}</p></section>)}</section>:null}
    {report.sections.includes('scenarios')?<ScenarioTable readOnly State="OverviewUnselected" rows={report.scenarios}/>:null}
    {report.sections.includes('participants')?<p>Оценки и время участников — по сценарию «{scenarioDefinitions.find(row=>row.id===(report.scenarioId||'catalog'))?.title}».</p>:null}
    {report.sections.includes('participants')?<div className={styles.reportTable}><h3>Участники · {report.participants.length}</h3><table><thead><tr><th>Участник</th><th>Исход задания</th><th>Полнота данных</th><th>Время</th></tr></thead><tbody>{report.participants.map(row=><tr key={row.id}><td>{row.id}</td><td>{row.outcome==='Achieved'?'Цель достигнута':row.outcome==='NotAchieved'?'Цель не достигнута':'Нет оценки'}</td><td>{row.coverage==='Complete'?'Полные':'Неполные'}</td><td>{row.duration}</td></tr>)}</tbody></table></div>:null}
  </>;
}

export function ReportContent({route,onSaved}:{route:WireRoute;onSaved:(id:string,created?:boolean)=>void}) {
  const store=useResearch();
  const study=store.study;
  const reports=store.reports.filter(report=>report.studyId===study.id);
  const [sections,setSections]=useState<ReportSection[]>(['scenarios','participants']);
  const [error,setError]=useState('');
  const saved=store.reports.find(report=>report.id===route.reportId&&report.studyId===study.id);
  const hasData=selectParticipants(store.observations,route.device,route.scenario).length>0;
  const generate=async()=>{
    setError('');
    try {const report=await store.createReport(route.device,route.scenario,sections);onSaved(report.id,true);}
    catch(cause){setError(cause instanceof Error?cause.message:'Не удалось сформировать отчёт.');}
  };
  return <div className={styles.report}>
    <h2>{saved?.studyTitle||study.title}</h2><p>Демонстрационные данные · {deviceLabels[route.device]}</p>
    {saved?<>
      <ReportSnapshot report={saved}/>
      {createPortal(<div data-print-report className={`${styles.report} ${styles.printReport}`}><h2>{saved?.studyTitle||study.title}</h2><p>Демонстрационные данные · {deviceLabels[saved.device]}</p><ReportSnapshot report={saved}/></div>,document.body)}
      <div className={styles.noPrint}><ProductButton Kind="Primary" onClick={()=>window.print()}>Печать / сохранить PDF</ProductButton><ProductButton Kind="Tertiary" onClick={()=>onSaved('')}>Изменить состав отчёта</ProductButton></div>
    </>:<>
      {route.reportId?<EuiCallOut color="warning" title="Отчёт не найден в текущем сеансе"><p>Сформируйте его повторно из текущих данных.</p></EuiCallOut>:null}
      <form onSubmit={event=>{event.preventDefault();void generate();}} className={styles.reportForm}>
        <fieldset disabled={store.pending!==null} aria-invalid={Boolean(error&&!sections.length)} aria-describedby={error?'report-section-error':undefined}><legend>Включить в отчёт</legend>
          {([['summary','Сводные показатели'],['scenarios','Сводка по сценариям'],['participants','Участники'],['heatmap','Тепловые карты выбранных страниц'],['signals','Сигналы и полнота данных'],['findings','Находки и выводы команды']] as const).map(([id,label])=><ProductCheckbox key={id} Label={label} Value={sections.includes(id)?'On':'Off'} State={store.pending?'Disabled':'Default'} onChange={checked=>{setSections(previous=>checked?[...previous,id]:previous.filter(section=>section!==id));setError('');}}/>)}
        </fieldset>
        {error?<div role="alert" id="report-section-error"><EuiCallOut color="danger" title={error}/></div>:null}
        {!hasData?<EuiCallOut color="warning" title="В текущей выборке нет данных для отчёта"><p>Измените фильтр устройства в обзоре результатов.</p></EuiCallOut>:null}
        <ProductButton Kind="Primary" State={!hasData?'Disabled':store.pending==='report'?'Loading':store.pending?'Disabled':'Default'} onClick={()=>void generate()}>{store.pending==='report'?'Формируем отчёт':'Сформировать отчёт'}</ProductButton>
      </form>
    </>}
    {reports.length&&!saved?<section className={styles.noPrint}><h3>Сформированные отчёты · {reports.length}</h3>{reports.map((report,index)=><ProductButton key={report.id} Kind="Tertiary" onClick={()=>onSaved(report.id)}>Отчёт {reports.length-index} · {deviceLabels[report.device]} · {new Date(report.createdAt).toLocaleTimeString('ru-RU')}</ProductButton>)}</section>:null}
  </div>;
}
