import { useState } from 'react';
import type { Meta, StoryObj } from '@storybook/react-vite';
import { Modal, ProductField, ProductButton, Badge, NavMenu, ProductTab, Breadcrumbs, Pagination, ParticipantsTable, Toast, Tooltip, DataCoverage } from '../components';
import { ProductTheme } from '../tokens/ProductTheme';
import styles from './catalog.module.css';

function StudyForm({onSave,onCancel}:{onSave:(name:string)=>void;onCancel:()=>void}) {
  const [name,setName]=useState('');
  const [mode,setMode]=useState('Задания');
  const [error,setError]=useState(false);
  const submit=()=>{if(!name.trim()){setError(true);return;}setError(false);onSave(name.trim());};
  return <div className={styles.form}>
    <ProductField Type="Text" Label="Название исследования" State={error?'Invalid':'Default'} value={name} onChange={value=>{setName(String(value));if(String(value).trim())setError(false);}}/>
    <ProductField Type="Select" Label="Режим исследования" value={mode} options={['Задания','Свободное изучение']} onChange={value=>setMode(String(value))}/>
    {error?<p role="alert">Укажите название исследования.</p>:null}
    <div className={styles.actions}><ProductButton Kind="Secondary" onClick={onCancel}>Отмена</ProductButton><ProductButton Kind="Primary" onClick={submit}>Сохранить</ProductButton></div>
  </div>;
}
function ModalSandbox() {
  const [revision,setRevision]=useState(0);
  const [saved,setSaved]=useState('');
  return <ProductTheme><div className={styles.sandbox}><h1>Новое исследование</h1><p>Откройте окно, заполните поля и сохраните. Escape и крестик закрывают диалог.</p>
    <Modal key={revision} title="Создать исследование" footer={<Badge Color="Hollow" label="Черновик"/>}><StudyForm onCancel={()=>setRevision(v=>v+1)} onSave={name=>{setSaved(name);setRevision(v=>v+1);}}/></Modal>
    {saved?<p role="status" className={styles.status}>Создано исследование «{saved}».</p>:null}
  </div></ProductTheme>;
}
function FormSandbox() {
  const [revision,setRevision]=useState(0);
  const [saved,setSaved]=useState('');
  return <ProductTheme><div className={styles.sandbox}><h1>Настройка исследования</h1><StudyForm key={revision} onCancel={()=>{setRevision(v=>v+1);setSaved('');}} onSave={setSaved}/>{saved?<p role="status" className={styles.status}>Сохранено: {saved}</p>:null}<DataCoverage Coverage="Partial" ShowAction={false}/></div></ProductTheme>;
}
function NavigationSandbox() {
  const [section,setSection]=useState('Overview');
  const [tab,setTab]=useState('signals');
  const [page,setPage]=useState(1);
  return <ProductTheme><div className={styles.navigation}><NavMenu Active={section as 'Overview'} onChange={value=>{setSection(String(value));setPage(1);}}/><main className={styles.sandbox}><Breadcrumbs/><h1>Исследование «Покупка в магазине»</h1><p role="status">Раздел: {section} · страница {page}</p><div className={styles.actions} role="tablist" aria-label="Результаты"><ProductTab Selected={tab==='signals'?'True':'False'} onClick={()=>setTab('signals')}>Сигналы</ProductTab><ProductTab Selected={tab==='findings'?'True':'False'} onClick={()=>setTab('findings')}>Находки · 2</ProductTab></div><p role="tabpanel">{tab==='signals'?'Повторные клики и возвраты по шагам сценария.':'Находки команды, подтверждённые записями участников.'}</p><Pagination key={section} Type="Few" onChange={value=>setPage(Number(value)+1)}/></main></div></ProductTheme>;
}
function DataSandbox() {
  const [selected,setSelected]=useState('');
  const [revision,setRevision]=useState(0);
  return <ProductTheme><div className={styles.sandbox}><h1>Участники исследования</h1><Tooltip Description="Неполные данные не означают неуспех задания."><button>Как считаются результаты?</button></Tooltip><ParticipantsTable State="Ready" onOpenRecording={(value:unknown)=>{const data=value as {participantId?:string;id?:string;attempt?:number};setSelected(`Запись ${data.participantId||data.id||'участника'} · попытка ${data.attempt||1}`);setRevision(v=>v+1);}}/>{selected?<Toast key={revision} Type="Success" Icon="True" title={selected}/>:null}</div></ProductTheme>;
}
/** Компоненты существующей базы в общих пользовательских сценариях UX-Lab. */
const meta={title:'Sandboxes/Blocks',id:'sandboxes',tags:['autodocs'],parameters:{layout:'padded',docs:{description:{component:'Живые композиции из компонентов базы: формы, навигация, диалог и таблица с обратной связью.'}}}} satisfies Meta;
export default meta;
type Story=StoryObj<typeof meta>;
/** Modal + Input + Select + Badge + две кнопки. */
export const Dialog:Story={name:'Модальное окно',render:()=> <ModalSandbox/>};
/** Валидация, сохранение и сброс формы. */
export const Form:Story={name:'Форма',render:()=> <FormSandbox/>};
/** Sidebar, вкладки, цепочка навигации и пагинация. */
export const Navigation:Story={name:'Навигация',render:()=> <NavigationSandbox/>};
/** Фильтры таблицы, страницы, выбор записи и уведомление. */
export const DataFeedback:Story={name:'Данные и обратная связь',render:()=> <DataSandbox/>};
