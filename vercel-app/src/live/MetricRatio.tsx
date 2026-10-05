import { EuiProgress } from '@elastic/eui';
import s from './MetricRatio.module.css';

/** A ratio uses the same 0–100 scale in every row; no denominator means no data. */
export function MetricRatio({value,total,label}:{value:number;total:number;label:string}) {
  const ratio=total>0&&Number.isFinite(total)&&Number.isFinite(value)?Math.max(0,Math.min(100,value/total*100)):null;
  const text=ratio===null?'—':`${Math.round(ratio)}%`;
  return <div className={s.ratio} title={ratio===null?'Нет данных':`${value} из ${total}`}>
    <EuiProgress className={s.track} value={ratio??0} max={100} size="m" color="primary" aria-label={label} aria-valuetext={ratio===null?'Нет данных':`${text} (${value} из ${total})`}/>
    <span className={s.value}>{text}</span>
  </div>;
}
