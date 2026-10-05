import {useEffect,useState} from 'react';
import {EuiButtonGroup} from '@elastic/eui';
import {Field} from '../screens/WorkspaceUI';
import {ProductDropdown} from '../components/_shared/ProductDropdown';
import {pageLabels} from '../heatmap/types';
import {liveApi} from './api';
import type {StudyTaskDefinition,Verification} from './types';
import s from './LiveWorkspace.module.css';
import switchStyles from '../components/_shared/SignalViewSwitch.module.css';
export type SuccessSignal={type:'screen'|'element'|'event';value:string;page:string;label:string;lastAt:number};
const legacyLabels:Record<string,string>={chat_message_sent:'Отправлено сообщение в чат',lead_created:'Создан новый лид'};
export const taskVerification=(task:StudyTaskDefinition):Verification|undefined=>task.verification??(legacyLabels[task.criterion]?{method:'automatic',type:'event',value:task.criterion,page:''}:undefined);
export function SuccessCriteriaEditor({task,busy,update,onValidity}:{task:StudyTaskDefinition;busy:boolean;update:(patch:Partial<StudyTaskDefinition>)=>void;onValidity:(id:string,valid:boolean)=>void}){
 const [signals,setSignals]=useState<SuccessSignal[]>([]),[loaded,setLoaded]=useState(false),[error,setError]=useState('');
 const check=taskVerification(task),description=task.successDescription??legacyLabels[task.criterion]??'';
 useEffect(()=>{let disposed=false;async function read(){try{const result=await liveApi<{signals:SuccessSignal[]}>('/criteria-catalog');if(!disposed){setSignals(result.signals);setLoaded(true);setError('')}}catch{if(!disposed)setError('Не удалось проверить подключение события.')}}void read();const timer=setInterval(()=>void read(),3000);return()=>{disposed=true;clearInterval(timer)}},[]);
 const connected=check?.method==='automatic'&&signals.some(signal=>signal.type===check.type&&signal.value===check.value&&signal.page===check.page);
 const valid=task.criterion!=='custom'||Boolean(description.trim()&&description.length<=2000&&(check?.method==='manual'||connected));
 useEffect(()=>onValidity(task.id,valid),[task.id,valid,onValidity]);
 function setCheck(verification:Verification|undefined,successDescription=description){update(verification?{criterion:'custom',successDescription,verification}:{criterion:'none',successDescription:undefined,verification:undefined})}
 const available=check?.method==='automatic'?signals.filter(signal=>signal.type===check.type):[];
 return <div className={s.criteriaEditor}>
   <Field label="Что считать успехом" type="Textarea" value={description} error={description.length>2000} onChange={value=>setCheck(check??{method:'manual'},value)}/>
   <p className={s.taskEditorHint}>Опишите результат своими словами. Участник видит задание, а это описание предназначено для оценки.</p>
   <ProductDropdown appearance="field" label="Как проверять результат" disabled={busy} value={check?.method||'none'} options={[{value:'manual',label:'Вручную по записи сессии'},{value:'automatic',label:'Автоматически'},{value:'none',label:'Не оценивать'}]} onChange={method=>setCheck(method==='none'?undefined:method==='manual'?{method:'manual'}:{method:'automatic',type:'event',value:'',page:''})}/>
   {check?.method==='manual'?<p className={s.taskEditorHint}>После завершения задания результат будет ожидать оценки. В истории сессии можно выбрать «Выполнено», «Не выполнено» или «Невозможно оценить».</p>:null}
   {check?.method==='automatic'?<div className={s.criteriaCheck}>
     <p>Какое событие означает успех</p>
     <EuiButtonGroup className={`${switchStyles.root} ${s.criteriaPills}`} legend="Тип проверки успеха" color="text" buttonSize="s" isDisabled={busy} idSelected={check.type} options={[{id:'screen',label:'Посещение экрана'},{id:'element',label:'Нажатие элемента'},{id:'event',label:'Действие в прототипе'}]} onChange={type=>setCheck({method:'automatic',type:type as SuccessSignal['type'],value:'',page:''})}/>
     <ProductDropdown appearance="field" label={check.type==='screen'?'Экран':check.type==='element'?'Элемент на экране':'Записанное событие'} disabled={busy||!available.length} value={JSON.stringify([check.value,check.page])} placeholder={loaded?'Выберите из событий прототипа':'Загружаем события…'} options={available.map(signal=>({value:JSON.stringify([signal.value,signal.page]),label:check.type==='screen'?pageLabels[signal.value]||signal.label:signal.label+(signal.page?` · ${pageLabels[signal.page]||signal.page}`:'')}))} onChange={value=>{const [target,page]=JSON.parse(value) as [string,string];setCheck({...check,value:target,page})}}/>
     {check.type==='event'?<Field label="Или укажите имя своего события" value={check.value} onChange={value=>setCheck({...check,value:value.trim(),page:''})}/>:null}
     <p className={s.taskEditorHint}>{connected?'Событие получено от этого прототипа. Условие можно сохранить.':'Пока событие не получено, автоматическое условие сохранить нельзя. Включите сбор и выполните действие по ссылке участника.'}</p>
     {check.type==='event'&&!connected?<details><summary>Как подключить своё событие</summary><p className={s.taskEditorHint}>В подключённом прототипе отправьте событие после подтверждения результата приложением. Имя должно совпадать с условием.</p><code className={s.eventExample}>{`window.dispatchEvent(new CustomEvent('ux-success-signal', { detail: { kind: 'prototype_event', value: ${JSON.stringify(check.value||'booking_confirmed')} } }));`}</code><p className={s.taskEditorHint}>Само название не подключает событие. Прототипу нужен адаптер UX-Lab; сейчас он установлен в Lead Generation.</p></details>:null}
     {error?<p role="alert">{error}</p>:null}
   </div>:null}
 </div>;
}
