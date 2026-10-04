import {useState} from 'react';
import {ProductDropdown} from '../components/_shared/ProductDropdown';
import {liveApi} from './api';
export function TaskReview({session,taskId,status,onSaved}:{session:string;taskId:string;status:string;onSaved:()=>void}){
 const [busy,setBusy]=useState(false),[error,setError]=useState('');
 async function save(value:string){setBusy(true);setError('');try{await liveApi('/task-review',{session,taskId,status:value});onSaved()}catch{setError('Оценка не сохранена. Повторите попытку.')}finally{setBusy(false)}}
 return <div><ProductDropdown label="Оценка исследователя" placeholder="Оценить результат" value={status} disabled={busy} options={[{value:'succeeded',label:'Выполнено'},{value:'failed',label:'Не выполнено'},{value:'indeterminate',label:'Невозможно оценить'}]} onChange={value=>void save(value)}/>{error?<p role="alert">{error}</p>:null}</div>;
}
