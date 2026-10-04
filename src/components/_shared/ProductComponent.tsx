import { useId, type ReactNode } from 'react';
import { EuiButton, EuiCheckbox, EuiLoadingSpinner, EuiProgress } from '@elastic/eui';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import styles from './ProductComponent.module.css';
import { useVariantState } from './useVariantState';
import { ReplayPreview } from './ReplayPreview';
import { AttemptActionPreview } from './AttemptActionPreview';
import { ParticipantsTableExample } from './ParticipantsTableExample';
import { ScenarioRowPreview, ScenarioTablePreview, SuccessMetricView } from './ScenarioResults';
import {StudyNavigation,type StudyNavigationProps} from './StudyNavigation';
import logoUrl from '../../assets/ux-lab-logo.svg';
import { sourceIconName } from './sourceIconName';

function property(p:VariantValues,key:string,fallback:string) { return String(p[key]??Object.entries(p).find(([k])=>k.startsWith(key+'#'))?.[1]??fallback); }
function flag(p:VariantValues,key:string,fallback=false) { const found=p[key]??Object.entries(p).find(([k])=>k.startsWith(key+'#'))?.[1];return found===undefined?fallback:isOn(found); }
const routes=[['Projects','Все проекты'],['Studies','Исследования проекта'],['Setup','Настройка исследования'],['Launch','Проверка и запуск'],['Overview','Обзор результатов'],['Heatmap','Тепловая карта'],['Funnel','Воронка'],['Participants','Участники'],['Signals','Сигналы затруднений'],['PDF','Отчёты']];

const routeIcons=['folderOpen','folderClosed','controlsHorizontal','play','visBarVertical','heatmap','filter','users','flag','document'];
export function ProductAction({children,kind='Secondary',state='Default',onClick,icon=false,iconRight,label,expanded,hasPopup,trackingId}:{children?:ReactNode;kind?:string;state?:string;onClick?:()=>void;icon?:boolean|string;iconRight?:string;label?:string;expanded?:boolean;hasPopup?:'menu';trackingId?:string}) {
  return <span className={styles.buttonSlot}><EuiButton size="s" color="text" className={styles.button} data-kind={kind} data-state={state} isDisabled={state==='Disabled'} isLoading={state==='Loading'} onClick={onClick} aria-label={label} aria-expanded={expanded} aria-haspopup={hasPopup} data-ux-target={trackingId}>{icon?<DesignIcon type={typeof icon==='string'?icon:'playFilled'}/>:null}{children}{iconRight?<DesignIcon type={iconRight} className={iconRight==='arrowDown'&&expanded!==undefined?styles.dropdownChevron:undefined}/>:null}</EuiButton></span>;
}
function AsyncState({state,onRetry}:{state:string;onRetry:()=>void}) {
  return <div className={styles.empty} role={state==='Loading'?'status':undefined}>{state==='Loading'?<><EuiLoadingSpinner size="m"/><p>Загрузка данных</p></>:<><h3>{state==='Error'?'Не удалось загрузить данные':state==='FilteredEmpty'?'Ничего не найдено':'Пока нет данных'}</h3><p>{state==='Error'?'Повторите попытку.':state==='FilteredEmpty'?'Измените параметры фильтра.':'Данные появятся после начала исследования.'}</p>{state==='Error'||state==='FilteredEmpty'?<ProductAction onClick={onRetry}>{state==='Error'?'Повторить загрузку':'Сбросить фильтры'}</ProductAction>:null}</>}</div>;
}
export function ProductComponent({name,values:p}:{name:string;values:VariantValues}) {
  const id=useId();
  const [selected,setSelected]=useVariantState(isOn(p.Selected));
  const [checkValue,setCheckValue]=useVariantState(String(p.Value||'Off'));
  const checked=checkValue==='On';
  const [value,setValue]=useVariantState(String(p.value??''));
  const [active,setActive]=useVariantState(String(p.Active||'Projects'));
  const [state,setState]=useVariantState(String(p.State||'Default'));
  const disabled=state==='Disabled';
  const emit=(newValue:unknown)=>{if(typeof p.onChange==='function')p.onChange(newValue);};
  const click=()=>{if(typeof p.onClick==='function')p.onClick();};
  const label=property(p,'Label','Действие');
  const child=p.children as ReactNode;
  const field=(type=String(p.Type||'Text'))=><label className={styles.field} data-state={state}><span>{property(p,'Label','Название')}</span>{type==='Textarea'?<textarea aria-label={property(p,'Label','')} aria-describedby={`${id}-field-help`} disabled={disabled} value={value} placeholder="Введите текст" onChange={e=>{setValue(e.target.value);emit(e.target.value);}} aria-invalid={state==='Invalid'}/>:type==='Select'?<span className={styles.fieldSelect}><select aria-label={property(p,'Label','')} aria-describedby={`${id}-field-help`} disabled={disabled} value={value} onChange={e=>{setValue(e.target.value);emit(e.target.value);}} aria-invalid={state==='Invalid'}><option value="">Выберите значение</option>{(Array.isArray(p.options)?p.options:['Первый вариант','Второй вариант']).map(option=><option key={String(option)}>{String(option)}</option>)}</select><DesignIcon type="arrowDown"/></span>:<input aria-label={property(p,'Label','')} aria-describedby={`${id}-field-help`} disabled={disabled} value={value} type={type==='Password'?'password':type==='Search'?'search':'text'} placeholder={type==='Search'?'Поиск':'Введите значение'} onChange={e=>{setValue(e.target.value);emit(e.target.value);}} aria-invalid={state==='Invalid'}/>}<span id={`${id}-field-help`} className={styles.muted}>{state==='Invalid'?'Проверьте значение':flag(p,'ShowHelp')?property(p,'Help','Пояснение к полю'):null}</span></label>;
  const outcome=(status=String(p.Status||'Achieved'))=><span className={styles.outcome} data-status={status}><DesignIcon type={status==='Achieved'?'checkInCircleFilled':status==='NotAchieved'?'error':'minusInCircle'}/>{status==='Achieved'?'Цель достигнута':status==='NotAchieved'?'Цель не достигнута':'Нет оценки'}</span>;
  const coverage=(status=String(p.Status||'Complete'))=><span className={styles.coverage} data-status={status}><DesignIcon type={status==='Complete'?'checkInCircleFilled':'iInCircle'}/>{status==='Complete'?'Полные':status==='Partial'?'Неполные':'Недоступна'}</span>;
  const attempt=(mode=String(p.Mode||'Single'))=><AttemptActionPreview values={{...p,Mode:mode}}/>;
  if(name==='ProductButton')return <ProductAction trackingId={typeof p.trackingId==='string'?p.trackingId:undefined} kind={String(p.Kind||'Primary')} state={state} onClick={click} icon={typeof p.icon==='string'?p.icon:false} iconRight={typeof p.iconRight==='string'?p.iconRight:undefined}>{child||label}</ProductAction>;
  if(name==='Logo')return <span className={styles.logo}><img src={logoUrl} width={24} height={24} alt="UX-Lab"/></span>;
  if(name==='ProductNavItem')return <button className={styles.navItem} data-selected={selected} data-state={state} aria-current={selected?'page':undefined} onClick={()=>{setSelected(!selected);emit(!selected);click();}}><DesignIcon type={String(p.icon||'folderOpen')}/>{child||'Раздел'}</button>;
  if(name==='ProductTab')return <button role="tab" aria-selected={selected} className={styles.tab} data-state={state} onClick={()=>{setSelected(!selected);emit(!selected);click();}}>{child||'Вкладка'}</button>;
  if(name==='ProductField')return field();
  if(name==='ProductCheckbox')return <div className={styles.checkbox} data-state={state}><EuiCheckbox id={id} checked={checked} indeterminate={checkValue==='Mixed'} disabled={disabled} label={property(p,'Label','Включить раздел в отчёт')} onChange={e=>{setCheckValue(e.target.checked?'On':'Off');emit(e.target.checked);}}/></div>;
  if(name==='TaskChoiceCard')return <label className={styles.choice} data-selected={selected} data-state={state}><input type="radio" name={String(p.groupName||id)} checked={selected} disabled={disabled} onChange={()=>{setSelected(true);emit(true);}}/><span><strong className={styles.choiceTitle}>{property(p,'Title','Найти товар')}</strong><span>{property(p,'Description','Найдите подходящий товар и откройте его карточку.')}</span></span>{selected?<small className={styles.choiceCaption}>Выбрано</small>:null}</label>;
  if(name==='TaskOutcome')return outcome();
  if(name==='RecordingCoverage')return coverage();
  if(name==='AttemptAction')return attempt();
  if(name==='DataCoverage'){
    const status=String(p.Coverage||'Complete');
    return <section className={styles.card+' '+styles.dataCoverage} data-status={status}><h3><DesignIcon type="iInCircle" size="l"/>{status==='Complete'?'Данные полные':status==='Partial'?'Данные неполные':'Запись недоступна'}</h3><p className={styles.muted}>{property(p,'DetailText'+status,status==='Complete'?'События и запись доступны для анализа.':status==='Partial'?'Часть записи отсутствует. Это не означает неуспех задания.':'Причина недоступности уточняется.')}</p>{flag(p,'ShowAction',true)?status==='Unavailable'?<ProductAction onClick={click}>К участнику</ProductAction>:<button className={styles.contextLink} onClick={click}>Посмотреть данные <DesignIcon type="arrowRight"/></button>:null}</section>;
  }
  if(name==='SuccessMetric')return <SuccessMetricView values={p}/>;
  if(name==='ScenarioRow')return <ScenarioRowPreview values={p}/>;
  if(name==='ScenarioTable')return <ScenarioTablePreview values={p}/>;
  if(name==='SummaryMetric')return <section className={`${styles.card} ${styles.summaryMetric}`}><p className={styles.summaryLabel}>{label}</p><div className={styles.summaryValueRow}>{state==='Loading'?<EuiLoadingSpinner size="m"/>:<strong className={styles.metricValue}>{state==='NoData'?'—':property(p,'Value','20')}</strong>}{state==='Ready'&&flag(p,'ShowBadge')?<span className={styles.summaryBadge} data-tone={p.BadgeTone||'accent'}>{property(p,'Badge','90%')}</span>:null}</div><p className={styles.muted}>{property(p,'Hint','Уникальных в текущей выборке')}</p><p className={`${styles.muted} ${styles.summaryDetail}`}>{property(p,'Detail','Доли не рассчитываются без наблюдений.')}</p>{state==='Ready'&&flag(p,'ShowProgress')?<EuiProgress className={styles.summaryProgress} color="primary" value={Number.parseFloat(property(p,'Badge','90%'))||0} max={100} size="m" aria-label="Полнота данных"/>:null}{flag(p,'ShowLink')?<button className={styles.summaryLink} onClick={click}>{property(p,'LinkLabel','Посмотреть участников')}<DesignIcon type="arrowRight"/></button>:null}</section>;
  if(name==='NavMenu')return <nav className={styles.nav} aria-label="Основная навигация"><div className={styles.brand}><span className={styles.logo}><img src={logoUrl} width={24} height={24} alt=""/></span>UX-Lab</div><span className={styles.muted}>РАБОЧЕЕ ПРОСТРАНСТВО</span>{routes.map(([route,title],index)=>(p.Scope==='workspace'&&index>0)||(p.Scope==='project'&&index>1)||(p.studies&&route==='PDF')?null:<div key={route}>{index===1?<p className={styles.navCaption}>{property(p,'ProjectLabel','ПРОЕКТ: ИНТЕРНЕТ-МАГАЗИН')}</p>:index===2?<p className={styles.navCaption}>{property(p,'StudyLabel','ИССЛЕДОВАНИЕ: ПОКУПКА')}</p>:null}{route==='Studies'&&p.studies?<StudyNavigation studies={p.studies as StudyNavigationProps['studies']} selectedStudy={String(p.selectedStudy||'')} onSelectStudy={p.onSelectStudy as StudyNavigationProps['onSelectStudy']} active={active===route} onOpenStudies={()=>{setActive(route);emit(route);}}/>:<button className={styles.navItem} data-selected={active===route} aria-current={active===route?'page':undefined} onClick={()=>{setActive(route);emit(route);}}><DesignIcon type={routeIcons[index]}/>{property(p,route+'Label',title)}</button>}{route==='Studies'&&p.studies?<button className={styles.navItem} data-selected={active==='PDF'} aria-current={active==='PDF'?'page':undefined} onClick={()=>{setActive('PDF');emit('PDF');}}><DesignIcon type="document"/>Отчёты</button>:null}</div>)}<p className={styles.navFooter}>{property(p,'FooterText','Рабочее пространство команды')}</p></nav>;
  if(name==='HeatmapLegend')return <section className={styles.card}><h3>{p.Mode==='FirstClick'?'Первые клики':'Все клики'}</h3><div className={styles.heatScale} role="img" aria-label="Интенсивность от низкой к высокой"/><div className={styles.between}><span className={styles.muted}>Меньше</span><span className={styles.muted}>Больше</span></div><p>{property(p,'SampleBase','84 клика · 18 участников')}</p><p className={styles.muted}>{property(p,'DefinitionNote','Для текущей страницы, состояния и выборки.')}</p></section>;
  if(name==='ReplayControls')return <ReplayPreview values={p}/>;
  if(name==='FirstClickTargetRow')return <button type="button" className={styles.dataRow} data-selected={selected} data-state={state} aria-pressed={selected} onClick={()=>{setSelected(!selected);emit(!selected);}}><DesignIcon type={sourceIconName(property(p,'TargetIcon','132:579'))||'bullseye'} size="original" className={styles.targetIcon}/><span className={styles.targetLabels}><strong>{property(p,'Title','Добавить в корзину')}</strong><small>{property(p,'Description','Основное действие страницы')}</small></span><span className={styles.targetMetrics}><span>{property(p,'Count','6')}</span><span>{property(p,'Share','33%')}</span></span></button>;
  if(name==='ResearchTableRow')return <table className={styles.table}><tbody><tr data-state={state}>{Array.from({length:Number(p.Columns||2)},(_,n)=>state==='Header'?<th key={n} scope="col">Колонка {n+1}</th>:<td key={n}>Значение {n+1}</td>)}</tr></tbody></table>;
  if(name==='ParticipantRow')return <table className={styles.table}><tbody><tr data-state={state}>{<><td>{property(p,'ParticipantId','014')}</td><td>{property(p,'Attempt','1')}</td><td>{outcome()}</td><td>{property(p,'Duration','04:32')}</td><td>{property(p,'SignalCount','4')}</td><td>{coverage()}</td><td>{attempt()}</td></>}</tr></tbody></table>;
  if(name==='ParticipantsTable')return <ParticipantsTableExample values={p}/>;
  if(name==='FirstClickTargets')return <section className={styles.card}>{state==='Ready'?<><h3>Первые клики по элементам</h3>{['Добавить в корзину','Изображение товара','Выбор размера'].map((title,n)=><ProductComponent key={title} name="FirstClickTargetRow" values={{Title:title,Description:'Элемент страницы',Count:String([6,5,3][n]),Share:['33%','28%','17%'][n],Selected:active===title?'True':'False',onChange:()=>{setActive(title);emit(title);}}}/>)}</>:<AsyncState state={state} onRetry={()=>setState('Ready')}/>}</section>;
  throw new Error('Unmapped product component: '+name);
}

