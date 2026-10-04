import { useId, useState } from 'react';
import { EuiRadioGroup } from '@elastic/eui';
import { ProductAction } from '../components/_shared/ProductComponent';
import styles from './TaskResultControl.module.css';
import { ProductTheme } from '../tokens/ProductTheme';

export type TaskResult = 'completed' | 'unable';
export function TaskResultControl({onNext}:{onNext?:(result:TaskResult)=>void}) {
  const id=useId();
  const [result,setResult]=useState<TaskResult|''>('');
  const [submitted,setSubmitted]=useState(false);
  return <ProductTheme><section className={styles.panel}>
    <h2>Задание 1 из 3</h2>
    <p>Найдите городской рюкзак и добавьте его в корзину.</p>
    <p>Отметьте результат задания, затем нажмите «Далее».</p>
    <EuiRadioGroup name={id} legend={{children:'Результат задания',className:styles.legend}} options={[{id:id+'completed',label:'Выполнил задание'},{id:id+'unable',label:'Не удалось выполнить'}]} idSelected={result?id+result:''} onChange={value=>{setResult(value===id+'completed'?'completed':'unable');setSubmitted(false);}}/>
    <ProductAction kind="Primary" state={result?'Default':'Disabled'} onClick={()=>{if(result){onNext?.(result);setSubmitted(true);}}}>Далее</ProductAction>
    {submitted?<p role="status">Выбранный результат сохранён в демонстрации.</p>:null}
    <p className={styles.note}>Участник 014<br/>Действия и ввод записываются</p>
  </section></ProductTheme>;
}
