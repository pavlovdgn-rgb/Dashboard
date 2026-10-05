import {useEffect,useState} from 'react';
import {createPortal} from 'react-dom';
import {EuiCallOut,EuiLink,EuiToolTip} from '@elastic/eui';
import {ProductButton,ProductCheckbox} from '../components';
import {ProductDropdown} from '../components/_shared/ProductDropdown';
import {ProductAction} from '../components/_shared/ProductComponent';
import {Card,Empty,Field,Table} from '../screens/WorkspaceUI';
import {useWireRoute} from '../screens/useWireRoute';
import {CLICK_API,pageLabels} from '../heatmap/types';
import {liveApi} from './api';
import {TaskOutcome,TaskSummary} from './TaskOutcome';
import type {LiveReport,LiveSummary,ReportEntry,ReportSection} from './types';
import s from './LiveWorkspace.module.css';
import w from '../screens/Workspace.module.css';

const sections:{value:ReportSection;label:string}[]=[{value:'tasks',label:'Выполнение заданий'},{value:'pages',label:'Активность по экранам'},{value:'sessions',label:'Сессии и результаты'},{value:'funnel',label:'Воронка переходов'},{value:'signals',label:'Сигналы затруднений'},{value:'findings',label:'Находки'}];
const devices=[{value:'all',label:'Все размеры экрана'},{value:'desktop',label:'От 768 px'},{value:'mobile',label:'До 768 px'}];
const date=(value:number)=>new Date(value).toLocaleString('ru-RU');
const page=(value:string)=>pageLabels[value]||value;
export function ReportSnapshot({report}:{report:LiveReport}){
 const included=(key:ReportSection)=>!report.sections||report.sections.includes(key);
 return <div className={s.report}>
  <h2>{report.title||`Отчёт · ${report.project.studyTitle}`}</h2><p>{report.project.studyTitle} · {date(report.createdAt)} · {devices.find(d=>d.value===report.device)?.label}</p>
  <p>Сессий: {report.total.sessions} · Кликов: {report.total.clicks} · Экранов: {report.total.pages}</p>
  {included('tasks')?<TaskSummary data={report}/>:null}
  {included('pages')?<><h2>Экраны</h2><Table label="Экраны отчёта" headers={['Экран','Сессии','Клики']}>{report.pages.map(r=><tr key={r.id}><td>{page(r.id)}</td><td>{r.sessions}</td><td>{r.clicks}</td></tr>)}</Table>{!report.pages.length?<p>Нет данных по экранам.</p>:null}</>:null}
  {included('sessions')?<><h2>Сессии</h2><Table label="Сессии отчёта" headers={['Сессия','Последнее действие','Клики','Задания']}>{report.sessions.map(r=><tr key={r.id}><td>{r.id}</td><td>{date(r.lastAt)}</td><td>{r.clicks}</td><td><TaskOutcome task={r.task}/></td></tr>)}</Table></>:null}
  {included('funnel')?<><h2>Воронка переходов</h2>{report.funnel.length?<Table label="Воронка отчёта" headers={['Шаг','Дошли, сессий']}>{report.funnel.map((r,i)=><tr key={i}><td>{i+1}. {page(r.page)}</td><td>{r.sessions}</td></tr>)}</Table>:<p>Последовательность экранов не настроена.</p>}</>:null}
  {included('signals')?<><h2>Сигналы затруднений</h2><p className={w.muted}>Повторные клики — повод изучить контекст, а не доказательство проблемы.</p>{report.signals.length?report.signals.map(r=><p key={r.id}>{page(r.page)} · {r.label} · {date(r.timestamp)} · {r.session}</p>):<p>Сигналов в этой выборке нет.</p>}</>:null}
  {included('findings')?<><h2>Находки</h2>{report.findings.length?report.findings.map(r=><div key={r.id}><h3>{r.title}</h3><p>{r.observation}</p></div>):<p>Находок пока нет.</p>}</>:null}
  <p className={w.muted}>Данные зафиксированы на момент формирования. Сессия соответствует вкладке браузера, а не уникальному человеку.</p>
 </div>;
}
export function ProjectReports({data,headerActions}:{data:LiveSummary;headerActions?:HTMLElement|null}){
 const {route,navigate}=useWireRoute();
 const [entries,setEntries]=useState<ReportEntry[]>([]),[loaded,setLoaded]=useState(false),[revision,setRevision]=useState(0),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 const [filter,setFilter]=useState('all'),[selected,setSelected]=useState<LiveReport|null>(null);
 const [study,setStudy]=useState(route.study),[title,setTitle]=useState(''),[device,setDevice]=useState(route.device),[chosen,setChosen]=useState<ReportSection[]>(sections.map(s=>s.value));
 const creating=route.item==='create',studies=data.studies||[data.project];
 useEffect(()=>{let disposed=false;liveApi<{reports:ReportEntry[]}>('/reports').then(result=>{if(!disposed){setEntries(result.reports);setLoaded(true)}}).catch(()=>{if(!disposed)setError('Не удалось загрузить отчёты.')});return()=>{disposed=true}},[revision]);
 useEffect(()=>{let disposed=false;setSelected(null);if(route.reportId)liveApi<LiveReport>('/report?id='+encodeURIComponent(route.reportId)).then(result=>{if(!disposed)setSelected(result)}).catch(()=>{if(!disposed)setError('Не удалось открыть отчёт.')});return()=>{disposed=true}},[route.reportId]);
 async function download(entry:ReportEntry){setBusy(true);setError('');try{const response=await fetch(`${CLICK_API}/api/project/report-pdf?id=${encodeURIComponent(entry.id)}`);if(!response.ok)throw Error();const blob=await response.blob(),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=`${(entry.title||'Отчёт').replace(/[<>:"/\\|?*]/g,'_')}.pdf`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}catch{setError('Не удалось скачать PDF. Повторите попытку.')}finally{setBusy(false)}}
 async function generate(){setBusy(true);setError('');try{const result=await liveApi<LiveReport>('/reports?study='+encodeURIComponent(study),{title:title.trim()||`Отчёт · ${studies.find(s=>s.studyId===study)?.studyTitle||''}`,device,sections:chosen});setRevision(v=>v+1);navigate({item:'',reportId:result.id});setSelected(result)}catch{setError('Не удалось сформировать отчёт. Проверьте настройки и подключение.')}finally{setBusy(false)}}
 const action=<span className={s.reportAction}><ProductButton Kind="Primary" icon="plus" onClick={()=>{setError('');navigate({item:'create',reportId:''})}}>Создать отчёт</ProductButton></span>;
 const filtered=entries.filter(r=>filter==='all'||r.project.studyId===filter);
 return <>
  {!creating&&!route.reportId?(headerActions?createPortal(action,headerActions):action):null}
  {error?<EuiCallOut color="danger" title={error}/>:null}
  {creating?<Card><h2>Новый отчёт</h2><p className={w.muted}>Выберите исследование и разделы. Отчёт сохранит результаты на момент формирования.</p><div className={s.reportForm}>
   <Field label="Название отчёта" value={title} onChange={setTitle}/>
   <ProductDropdown appearance="field" label="Исследование для отчёта" value={study} options={studies.map(r=>({value:r.studyId,label:r.studyTitle}))} disabled={busy} onChange={setStudy}/>
   <ProductDropdown appearance="field" label="Размер экрана в отчёте" value={device} options={devices} disabled={busy} onChange={value=>setDevice(value as typeof device)}/>
   <fieldset className={s.reportSections}><legend>Разделы отчёта</legend>{sections.map(section=><ProductCheckbox key={section.value} Label={section.label} Value={chosen.includes(section.value)?'On':'Off'} State={busy?'Disabled':'Default'} onChange={value=>setChosen(old=>value?[...old,section.value]:old.filter(s=>s!==section.value))}/>)}</fieldset>
   {!chosen.length?<p role="alert">Выберите хотя бы один раздел.</p>:null}
   {!(data.studies?.find(s=>s.studyId===study)?.sessions)?<p className={w.muted}>В исследовании пока нет сессий. В отчёте будут показаны пустые разделы.</p>:null}
   <div className={s.actions}><ProductButton Kind="Primary" State={busy?'Loading':!chosen.length||title.length>160?'Disabled':'Default'} onClick={()=>void generate()}>Сформировать PDF</ProductButton><ProductButton Kind="Tertiary" State={busy?'Disabled':'Default'} onClick={()=>navigate({item:'',reportId:''})}>Отмена</ProductButton></div>
  </div></Card>:route.reportId?<><div className={s.actions}><ProductButton Kind="Tertiary" icon="arrowLeft" onClick={()=>navigate({reportId:'',item:''})}>К списку отчётов</ProductButton>{selected?<ProductButton Kind="Primary" icon="download" State={busy?'Loading':'Default'} onClick={()=>void download(selected)}>Скачать PDF</ProductButton>:null}</div>{selected?<Card><ReportSnapshot report={selected}/></Card>:<p role="status">Загружаем отчёт…</p>}</>:<>
   <div className={s.toolbar}><ProductDropdown label="Фильтр по исследованию" value={filter} options={[{value:'all',label:'Все исследования'},...studies.map(r=>({value:r.studyId,label:r.studyTitle}))]} onChange={setFilter}/><span className={w.muted}>Отчётов: {filtered.length}</span></div>
   {!loaded?<p role="status">Загружаем отчёты…</p>:filtered.length?<div className={`${s.table} ${s.reportsTable}`}><Table label="Отчёты проекта" headers={['Название','Исследование','Создан','']}>{filtered.map(r=>{const name=r.title||`Отчёт · ${r.project.studyTitle}`;return <tr key={r.id}><td><EuiLink className={s.reportTitle} data-row-action onClick={()=>navigate({reportId:r.id,item:''})}>{name}</EuiLink><small>{devices.find(d=>d.value===r.device)?.label}</small></td><td>{r.project.studyTitle}</td><td>{date(r.createdAt)}</td><td><EuiToolTip content="Скачать PDF"><span><ProductAction kind="Tertiary" icon="download" label={`Скачать PDF: ${name}`} state={busy?'Disabled':'Default'} onClick={()=>void download(r)}/></span></EuiToolTip></td></tr>})}</Table></div>:<Empty>{entries.length?'В выбранном исследовании пока нет отчётов.':'Создайте первый отчёт по одному из исследований проекта.'}</Empty>}
  </>}
 </>;
}
