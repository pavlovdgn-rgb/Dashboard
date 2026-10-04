import { useState } from 'react';
import { ProductAction, ProductComponent } from './ProductComponent';
import { useVariantState } from './useVariantState';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import styles from './ProductComponent.module.css';
import { ProductDropdown } from './ProductDropdown';

export type ParticipantRecord = {
  id:string;
  attempts:number;
  outcome:'Achieved'|'NotAchieved'|'NotAssessed';
  duration:string;
  signals:number;
  coverage:'Complete'|'Partial'|'Unavailable';
};
export type ParticipantFilters={query:string;outcome:string;coverage:string;page:number};
const sampleIds=['014','018','009','012','001','002','003','004','005','006','007','008','010','011','013','015'];
const participantFixture:ParticipantRecord[]=sampleIds.map((id,index)=>({
  id,attempts:index===2?2:1,
  outcome:index%4===0?'NotAchieved':index%4===1?'NotAssessed':'Achieved',
  duration:['04:32','03:10','02:48','03:24'][index%4],
  signals:[4,2,3,2][index%4],coverage:index%4===1?'Partial':'Complete',
}));
const pageSize=4;

export function ParticipantsTableExample({values:p}:{values:VariantValues}) {
  const [state,setState]=useVariantState(String(p.State||'Ready'));
  const [localFilters,setLocalFilters]=useState<ParticipantFilters>({query:'',outcome:'',coverage:'',page:1});
  const filters=(p.filters as ParticipantFilters|undefined)??localFilters;
  const {query,outcome,coverage,page}=filters;
  const updateFilters=(patch:Partial<ParticipantFilters>)=>{const next={...filters,...patch};setLocalFilters(next);if(typeof p.onFiltersChange==='function')p.onFiltersChange(next);};
  const [attempts,setAttempts]=useState<Record<string,string>>({});
  const rows=Array.isArray(p.rows)?p.rows as ParticipantRecord[]:participantFixture;
  const filtered=rows.filter(row=>row.id.includes(query.trim())&&(!outcome||row.outcome===outcome)&&(!coverage||row.coverage===coverage));
  const pageCount=Math.max(1,Math.ceil(filtered.length/pageSize));
  const currentPage=Math.min(page,pageCount);
  const visible=filtered.slice((currentPage-1)*pageSize,currentPage*pageSize);
  const hasResults=state==='Ready'&&visible.length>0;
  const reset=()=>{updateFilters({query:'',outcome:'',coverage:'',page:1});setState('Ready');};
  const open=(row:ParticipantRecord,attempt=1)=>{
    if(typeof p.onOpenRecording==='function')p.onOpenRecording({participantId:row.id,attempt});
    else if(typeof p.onClick==='function')p.onClick();
  };
  const choose=(row:ParticipantRecord,attempt:string)=>{setAttempts(previous=>({...previous,[row.id]:attempt}));if(attempt)open(row,Number(attempt));};
  return <section className={`${styles.card} ${styles.participantsCard}`}>
    <div className={styles.toolbar}>
      <strong aria-live="polite">{rows.length} участников начали · показаны {state==='Ready'?visible.length:0}</strong>
      <div className={styles.filters}>
        <span className={styles.filterSearch}><DesignIcon type="search" size="s"/><input aria-label="Поиск по ID" placeholder="Поиск по ID" value={query} onChange={e=>updateFilters({query:e.target.value,page:1})}/></span>
        <ProductDropdown label="Исход задания" value={outcome} onChange={value=>updateFilters({outcome:value,page:1})} options={[{value:'',label:'Все исходы'},{value:'Achieved',label:'Цель достигнута'},{value:'NotAchieved',label:'Цель не достигнута'},{value:'NotAssessed',label:'Нет оценки'}]}/>
        <ProductDropdown label="Полнота данных" value={coverage} onChange={value=>updateFilters({coverage:value,page:1})} options={[{value:'',label:'Все данные'},{value:'Complete',label:'Полные'},{value:'Partial',label:'Неполные'},{value:'Unavailable',label:'Недоступна'}]}/>
      </div>
    </div>
      <div className={`${styles.tableSurface} ${styles.participantsSurface}`}><table className={`${styles.table} ${styles.participantsTable}`} aria-label="Участники исследования"><colgroup>{['participant','attempt','outcome','duration','signals','coverage','action'].map(column=><col key={column} data-column={column}/>)}</colgroup><thead><tr>{['Участник','Попытка','Исход задания','Время','Сигналы','Данные','Действие'].map(title=><th scope="col" key={title}>{title}</th>)}</tr></thead>
        <tbody>{hasResults?visible.map(row=><tr key={row.id}>
          <td>{row.id}</td><td>{row.attempts>1?`${attempts[row.id]||1} из ${row.attempts}`:'1'}</td>
          <td><ProductComponent name="TaskOutcome" values={{Status:row.outcome}}/></td><td>{row.duration}</td><td>{row.signals}</td>
          <td><ProductComponent name="RecordingCoverage" values={{Status:row.coverage}}/></td>
          <td>{row.attempts>1?<ProductDropdown label={`Выбрать попытку участника ${row.id}`} placeholder="Выбрать попытку" icon="layers" value={attempts[row.id]||''} onChange={value=>choose(row,value)} options={Array.from({length:row.attempts},(_,index)=>({value:String(index+1),label:`Попытка ${index+1}`}))}/>:<ProductAction kind={row.coverage==='Unavailable'?'Secondary':'Primary'} onClick={()=>open(row)}>{row.coverage==='Unavailable'?'К участнику':'Открыть запись'}</ProductAction>}</td>
        </tr>):null}</tbody></table>
    {!hasResults?<div className={`${styles.empty} ${styles.participantsMessage}`} role={state==='Loading'?'status':undefined}>
      <h3>{state==='Loading'?'Загрузка данных':state==='Error'?'Не удалось загрузить данные':state==='Empty'||rows.length===0?'Пока нет данных':'Ничего не найдено'}</h3>
      <p>{state==='Loading'?'Подождите, данные загружаются.':state==='Error'?'Повторите попытку.':state==='Empty'||rows.length===0?'Данные появятся после начала исследования.':'Измените параметры фильтра.'}</p>
      {state==='Error'?<ProductAction onClick={()=>{if(typeof p.onRetry==='function')p.onRetry();setState('Ready');}}>Повторить загрузку</ProductAction>:state!=='Empty'&&state!=='Loading'&&rows.length>0?<ProductAction onClick={reset}>Сбросить фильтры</ProductAction>:null}
    </div>:null}</div>
      <div className={`${styles.tableFooter} ${styles.participantsFooter}`}><span aria-live="polite">{hasResults?`Участники ${(currentPage-1)*pageSize+1}–${Math.min(currentPage*pageSize,filtered.length)} из ${filtered.length}`:state==='Ready'||state==='FilteredEmpty'?'Найдено 0 участников':'Нет отображаемых участников'}</span><span className={styles.muted}>Время и показатели относятся к выбранной попытке.</span><nav className={styles.pager} aria-label="Страницы таблицы"><button disabled={!hasResults||currentPage===1} aria-label="Предыдущая страница" onClick={()=>updateFilters({page:currentPage-1})}><DesignIcon type="arrowLeft"/></button><span aria-live="polite">{hasResults?currentPage:1} из {hasResults?pageCount:1}</span><button disabled={!hasResults||currentPage===pageCount} aria-label="Следующая страница" onClick={()=>updateFilters({page:currentPage+1})}><DesignIcon type="arrowRight"/></button></nav></div>
    <p className={styles.muted}>Неполная запись и недостижение цели — разные признаки.</p>
  </section>;
}
