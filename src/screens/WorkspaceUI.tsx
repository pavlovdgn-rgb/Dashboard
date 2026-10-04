import { useState, type MouseEvent, type ReactNode } from 'react';
import { ProductButton, ProductField } from '../components';
import { EuiCallOut } from '@elastic/eui';
import s from './Workspace.module.css';
export function Card({children}:{children:ReactNode}) {return <section className={s.card}>{children}</section>;}
export function Field({label,value,onChange,type='Text',options,error}:{label:string;value:string;onChange:(value:string)=>void;type?:'Text'|'Textarea'|'Select'|'Search'|'Password';options?:string[];error?:boolean}) {return <ProductField Label={label} Type={type} value={value} onChange={value=>onChange(String(value))} options={options} State={error?'Invalid':'Default'}/>;}
/** A row delegates to its explicit primary action; nested controls keep their own behavior. */
function activateTableRow(event:MouseEvent<HTMLTableElement>) {
  if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  const target=event.target;
  if(!(target instanceof Element)||target.closest('table')!==event.currentTarget)return;
  if(target.closest('a,button,input,select,textarea,label,[role="button"],[role="link"],[contenteditable="true"]'))return;
  if(window.getSelection()?.toString())return;
  const primary=target.closest('tbody tr')?.querySelector<HTMLElement>('[data-row-action]');
  const action=primary?.matches('a,button')?primary:primary?.querySelector<HTMLElement>('a,button');
  if(!action||action.matches(':disabled,[aria-disabled="true"]'))return;
  action.click();
}
export function Table({headers,children,label}:{headers:string[];children:ReactNode;label:string}) {return <div className={s.table}><table aria-label={label} onClick={activateTableRow}><thead><tr>{headers.map(x=><th key={x} scope="col">{x}</th>)}</tr></thead><tbody>{children}</tbody></table></div>;}
export function Empty({children='Пока нет данных'}:{children?:ReactNode}) {return <div className={s.empty} role="status">{children}</div>;}
export function AsyncButton({children,action,primary=false}:{children:ReactNode;action:()=>void|Promise<void>;primary?:boolean}) {const [pending,setPending]=useState(false),[error,setError]=useState('');return <><ProductButton Kind={primary?'Primary':'Secondary'} State={pending?'Loading':'Default'} onClick={()=>{setPending(true);setError('');void new Promise(resolve=>setTimeout(resolve,250)).then(action).catch((e:unknown)=>setError(e instanceof Error?e.message:'Не удалось выполнить действие. Повторите попытку.')).finally(()=>setPending(false));}}>{children}</ProductButton>{error?<EuiCallOut color="danger" title={error}/>:null}</>;}
