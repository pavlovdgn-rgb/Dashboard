import { useId } from 'react';
import { EuiButtonGroup } from '@elastic/eui';
import s from './SignalViewSwitch.module.css';

export function SignalViewSwitch({pages,onChange}:{pages:boolean;onChange:(pages:boolean)=>void}) {
  const id=useId();
  return <EuiButtonGroup className={s.root} legend="Представление сигналов" buttonSize="s" color="text" idSelected={`${id}-${pages?'pages':'events'}`} options={[
    {id:`${id}-events`,label:'Отдельные события'},
    {id:`${id}-pages`,label:'По страницам'}
  ]} onChange={selected=>onChange(selected===`${id}-pages`)}/>;
}
