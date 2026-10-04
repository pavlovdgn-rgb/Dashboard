import { useId, type MouseEvent } from 'react';
import { EuiLoadingSpinner } from '@elastic/eui';
import type { VariantValues } from './CatalogComponent';
import { ProductAction } from './ProductComponent';
import { useVariantState } from './useVariantState';
import styles from './ProductComponent.module.css';

function text(p:VariantValues,key:string,fallback:string) {
  return String(p[key]??Object.entries(p).find(([name])=>name.startsWith(key+'#'))?.[1]??fallback);
}
export function SuccessMetricView({values:p}:{values:VariantValues}) {
  const mode=String(p.Data||'Value');
  const suffix=mode==='NoData'?'NoData':mode==='Zero'?'Zero':'Value';
  const fraction=text(p,'Fraction'+suffix,mode==='NoData'?'—':mode==='Zero'?'0 / 18':'14 / 18');
  const percent=text(p,'Percent'+suffix,mode==='NoData'?'—':mode==='Zero'?'0%':'78%');
  const base=text(p,mode==='Value'?'BaseValue':'Base'+suffix,mode==='NoData'?'Нет оценённых попыток':'Оценены 18 из 20');
  const progress=Math.max(0,Math.min(100,Number.parseFloat(percent)||0));
  return <div className={styles.successMetric}>
    <div className={styles.successHeading}><span>{fraction}</span><span className={styles.percent}>{percent}</span></div>
    <div className={styles.successTrack} role={mode==='NoData'?undefined:'progressbar'} aria-label="Достигли цели" aria-valuemin={0} aria-valuemax={100} aria-valuenow={mode==='NoData'?undefined:progress}><span style={{inlineSize:`${progress}%`}}/></div>
    <span className={styles.muted}>{base}</span>
  </div>;
}
export type ScenarioRecord={id:string;title:string;description:string;started:number;completed:number;achieved:number;assessed:number;incomplete:number};
const examples:ScenarioRecord[]=[
  {id:'catalog',title:'Найти товар и добавить в корзину',description:'Поиск → Карточка товара → В корзину',started:20,completed:16,achieved:14,assessed:18,incomplete:2},
  {id:'quantity',title:'Изменить количество товара',description:'Количество товара в мини-корзине',started:18,completed:15,achieved:12,assessed:17,incomplete:1},
  {id:'checkout',title:'Оформить заказ',description:'Контакты, доставка и подтверждение заказа',started:16,completed:12,achieved:10,assessed:15,incomplete:1},
];
function selectFromRow(event:MouseEvent<HTMLTableRowElement>,onSelect:()=>void) {
  // Labels and radios retain their native keyboard and click behavior.
  if((event.target as HTMLElement).closest('input,label'))return;
  event.currentTarget.querySelector<HTMLInputElement>('input[type="radio"]')?.focus();
  onSelect();
}
function ScenarioCells({row,selected,group,onSelect,readOnly=false}:{row:ScenarioRecord;selected:boolean;group:string;onSelect:()=>void;readOnly?:boolean}) {
  return <>
    <td><label className={styles.scenarioLabel} data-readonly={readOnly||undefined}>{!readOnly?<input type="radio" name={group} checked={selected} onChange={onSelect}/>:null}<span><strong>{row.title}</strong><small className={styles.muted}>{row.description}</small></span></label></td>
    <td>{row.started}</td><td>{row.completed}</td>
    <td><SuccessMetricView values={{Data:row.assessed?'Value':'NoData',FractionValue:`${row.achieved} / ${row.assessed}`,PercentValue:`${Math.round(100*row.achieved/(row.assessed||1))}%`,BaseValue:`Оценены ${row.assessed} из ${row.started}`}}/></td>
    <td><span className={styles.incompleteCount}>{row.incomplete}</span></td>
  </>;
}
export function ScenarioRowPreview({values:p}:{values:VariantValues}) {
  const group=useId();
  const [selected,setSelected]=useVariantState(p.Selected==='True');
  const row={...examples[0],title:text(p,'Title',examples[0].title),description:text(p,'Description',examples[0].description),started:Number(text(p,'Started','20')),completed:Number(text(p,'Completed','16')),incomplete:Number(text(p,'Incomplete','2'))};
  const choose=()=>{setSelected(true);if(typeof p.onChange==='function')p.onChange(true);};
  return <div className={styles.tableSurface}><table className={`${styles.table} ${styles.scenarioTable}`}><tbody><tr onClick={event=>selectFromRow(event,choose)} data-state={selected?'Selected':String(p.State)}><ScenarioCells row={row} selected={selected} group={group} onSelect={choose}/></tr></tbody></table></div>;
}
export function ScenarioTablePreview({values:p}:{values:VariantValues}) {
  const group=useId();
  const [state,setState]=useVariantState(String(p.State||'Ready'));
  const rows=Array.isArray(p.rows)?p.rows as ScenarioRecord[]:examples;
  const readOnly=p.readOnly===true;
  const initial=String(p.selectedId??(state==='OverviewSelected'?'checkout':state==='Ready'?'catalog':''));
  const [selectedId,setSelectedId]=useVariantState(initial);
  const ready=['Ready','OverviewSelected','OverviewUnselected'].includes(state);
  const choose=(id:string)=>{setSelectedId(id);if(typeof p.onChange==='function')p.onChange(id);};
  const selected=rows.find(row=>row.id===selectedId);
  const overview=state.startsWith('Overview')||p.overview===true;
  return <section className={styles.tableSection}>
    <h3>{overview?'Сценарии исследования':'Результаты по сценариям'}</h3>
    {!overview?<p className={styles.muted}>Выберите сценарий, чтобы подробнее изучить результаты.</p>:null}
    <div className={styles.tableSurface}><table className={`${styles.table} ${styles.scenarioTable}`} aria-label="Сценарии исследования"><thead><tr>{['Сценарий','Начали','Завершили','Достигли цели','Неполные'].map(title=><th key={title} scope="col">{title}</th>)}</tr></thead>
      <tbody>{ready&&rows.length?rows.map(row=><tr key={row.id} onClick={readOnly?undefined:event=>selectFromRow(event,()=>choose(row.id))} data-state={!readOnly&&selectedId===row.id?'Selected':undefined}><ScenarioCells row={row} selected={selectedId===row.id} group={group} onSelect={()=>choose(row.id)} readOnly={readOnly}/></tr>):<tr><td colSpan={5}><div className={styles.empty} role={state==='Loading'?'status':undefined}>
        {state==='Loading'?<EuiLoadingSpinner/>:null}
        <strong>{state==='Loading'?'Загрузка сценариев':state==='Error'?'Не удалось загрузить сценарии':state==='FilteredEmpty'?'Сценарии не найдены':'Пока нет результатов'}</strong>
        <p className={styles.muted}>{state==='Error'?'Повторите загрузку.':state==='FilteredEmpty'?'Измените параметры фильтра.':'Результаты появятся после прохождения исследования.'}</p>
        {state==='Error'||state==='FilteredEmpty'?<ProductAction onClick={()=>{setState('Ready');if(typeof p.onRetry==='function')p.onRetry();}}>{state==='Error'?'Повторить загрузку':'Сбросить фильтры'}</ProductAction>:null}
      </div></td></tr>}</tbody></table></div>
    {ready||overview?<p className={styles.muted}>Демо-данные · Участники могут встречаться в нескольких сценариях. Неполные данные не означают неуспех.</p>:null}
    {state==='Ready'&&selected?<div className={styles.scenarioContext}><p>Выбран сценарий: {selected.title}</p><div className={styles.row}>{['Тепловая карта','Воронка','Участники и записи','Сигналы'].map(destination=><ProductAction key={destination} onClick={()=>{if(typeof p.onNavigate==='function')p.onNavigate({scenarioId:selected.id,destination});}}>{destination}</ProductAction>)}</div></div>:null}
  </section>;
}
