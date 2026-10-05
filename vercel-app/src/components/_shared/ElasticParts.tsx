import { useId, useMemo, useRef, useState, type ReactNode } from 'react';
import * as E from '@elastic/eui';
import { EuiRangeThumb } from '@elastic/eui/es/components/form/range/range_thumb';
import { EuiRangeTrack } from '@elastic/eui/es/components/form/range/range_track';
import { EuiRangeLevels } from '@elastic/eui/es/components/form/range/range_levels';
import { EuiMarkdownEditorFooter } from '@elastic/eui/es/components/markdown_editor/markdown_editor_footer';
import { EuiMarkdownEditorToolbar } from '@elastic/eui/es/components/markdown_editor/markdown_editor_toolbar';
import MarkdownActions from '@elastic/eui/es/components/markdown_editor/markdown_actions';
import { useI18nTimeOptions } from '@elastic/eui/es/components/date_picker/super_date_picker/time_options';
import { EuiPopoverArrow } from '@elastic/eui/es/components/popover/popover_arrow';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';
import styles from './ElasticParts.module.css';

const valueOf=(p:VariantValues,key:string)=>p[key]??Object.entries(p).find(([name])=>name.startsWith(key+'#'))?.[1];
const on=(p:VariantValues,key:string)=>isOn(valueOf(p,key));
const emit=(p:VariantValues,value:unknown)=>{if(typeof p.onChange==='function')p.onChange(value);};

export function ElasticFormPart({index:i,values:p}:{index:number;values:VariantValues}) {
  const id=useId();
  const [value,setValue]=useVariantState(p.State==='Placeholder'?'':String(p.value??'Пример значения'));
  const disabled=p.State==='Disabled';
  const invalid=p.State==='Invalid';
  const compressed=on(p,'Compressed');
  const change=(v:string)=>{setValue(v);emit(p,v);};
  const clear=on(p,'Clearable')||on(p,'Clearable?')?{onClick:()=>change(''),'aria-label':'Очистить значение'}:undefined;
  if(i>=75&&i<=78){
    const messages=['Selects have no readonly or placeholder state','Inputs can only be clearable if they have content and aren’t disabled','Palettes must have a selection','Comboboxes only support prepend/append for single selections, in which case just use the normal Select control type.'];
    return <div className={styles.infoBox}><E.EuiCallOut color="primary" size="s"><p>{messages[i-75]}</p></E.EuiCallOut></div>;
  }
  if(i===71||i===72)return <div className={styles.controlPart} data-compressed={compressed}>
    {i===72&&on(p,'Prepend')?<span className={styles.addon}>Prepend</span>:null}
    <E.EuiFormControlLayoutIcons iconsPosition="static" compressed={compressed} isDisabled={disabled} isInvalid={invalid} isLoading={on(p,'Loading')} icon={on(p,'Icon')?DesignIcon:undefined} clear={i===71?clear:undefined}/>
    {i===72?<span className={p.State==='Placeholder'?styles.placeholder:undefined}>{value||'Placeholder'}</span>:null}
    {i===71&&on(p,'Number')?<span className={styles.numberArrows}><DesignIcon/><DesignIcon/></span>:null}
    {i===71&&on(p,'Append')?<span className={styles.addon}>Append</span>:null}
  </div>;
  if(i===70)return <div className={styles.rangeContent} data-invalid={on(p,'Invalid')}><E.EuiFieldText aria-label="Начало диапазона" value={value} onChange={e=>change(e.target.value)} isInvalid={on(p,'Invalid')}/><span>→</span><E.EuiFieldText aria-label="Конец диапазона" defaultValue="Значение" isInvalid={on(p,'Invalid')}/></div>;
  if(i===73)return <E.EuiFormControlLayoutDelimited fullWidth compressed={compressed} isDisabled={disabled} isInvalid={invalid} readOnly={p.State==='Read-only'}
    prepend={/Prepend|Both/.test(String(p['Prepend / Append']))?'От':undefined} append={/Append|Both/.test(String(p['Prepend / Append']))?'До':undefined}
    icon={p.Icon==='Left'?DesignIcon:undefined} isLoading={on(p,'Loading?')} clear={clear}
    startControl={<E.EuiFieldText aria-label="Начало" value={value} onChange={e=>change(e.target.value)} disabled={disabled} readOnly={p.State==='Read-only'} isInvalid={invalid} placeholder="Начало"/>}
    endControl={<E.EuiFieldText aria-label="Конец" defaultValue={p.State==='Placeholder'?'':'Конец'} placeholder="Конец" disabled={disabled} readOnly={p.State==='Read-only'} isInvalid={invalid}/>}/>;
  return <E.EuiFormControlLayout fullWidth compressed={compressed} isDisabled={disabled} isInvalid={invalid} readOnly={p.State==='Read-Only'} inputId={id}>
    <div id={id} className={styles.controlBackground} data-state={String(p.State)} data-resizable={on(p,'Resizable')} aria-label="Фон поля"/>
  </E.EuiFormControlLayout>;
}

export function ElasticMarkdownPart({index:i,values:p}:{index:number;values:VariantValues}) {
  const id=useId();
  const file=useRef<HTMLInputElement>(null);
  const [preview,setPreview]=useState(false);
  const [attachment,setAttachment]=useState('');
  const actions=useMemo(()=>new MarkdownActions(id,[]),[id]);
  const errors=p.Type==='Errors'?['Проверьте Markdown']:[];
  if(i===112)return <><EuiMarkdownEditorToolbar markdownActions={actions} uiPlugins={[]} viewMode={preview?'viewing':'editing'} onClickPreview={()=>setPreview(!preview)}/><textarea id={id} className={styles.offscreen} aria-label="Текст для форматирования" defaultValue="Пример текста"/></>;
  return <><EuiMarkdownEditorFooter uiPlugins={[]} isUploadingFiles={false} openFiles={()=>file.current?.click()} errors={errors} hasUnacceptedItems={p.Type==='Attachment error'} dropHandlers={[{supportedFiles:['.md','.txt'],accepts:type=>type==='text/plain',getFormattingForItem:()=>({text:'Вложение',config:{block:true}})}]}/><input className={styles.offscreen} type="file" accept=".md,.txt" ref={file} onChange={e=>setAttachment(e.target.files?.[0]?.name||'')}/>{attachment?<E.EuiText size="s">{attachment}</E.EuiText>:null}</>;
}

export function ElasticRangePart({index:i,values:p}:{index:number;values:VariantValues}) {
  const [value,setValue]=useVariantState(Number(p.value??40));
  const [pair,setPair]=useState<[number,number]>([20,70]);
  const [width,setWidth]=useState(400);
  const compressed=on(p,'Compressed');
  const disabled=p.State==='Disabled';
  const levels=[{min:0,max:30,color:'success' as const},{min:30,max:70,color:'warning' as const},{min:70,max:100,color:'danger' as const}];
  const update=(v:number)=>{setValue(v);emit(p,v);};
  if(i===133)return <div className={styles.rangeFragment} data-empty={p.State==='Empty'} data-compressed={compressed}><EuiRangeThumb min={0} max={100} value={value} role="slider" aria-label="Положение ползунка" aria-valuemin={0} aria-valuemax={100} aria-valuenow={value} tabIndex={0} onKeyDown={e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();update(Math.max(0,Math.min(100,value+(e.key==='ArrowRight'?1:-1))));}}}/></div>;
  if(i===135){const thumb=<EuiRangeThumb min={0} max={100} value={value} role="slider" aria-label="Положение ползунка" aria-valuemin={0} aria-valuemax={100} aria-valuenow={value} tabIndex={0} onKeyDown={e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();update(Math.max(0,Math.min(100,value+(e.key==='ArrowRight'?1:-1))));}}}/>;return <div className={styles.thumbPart}>{p.Tooltip==='None'?thumb:<E.EuiToolTip content={String(value)} position={p.Tooltip==='Left'?'left':'right'}>{thumb}</E.EuiToolTip>}</div>;}
  if(i===136)return <div className={styles.levelPart} data-compressed={compressed}><EuiRangeLevels min={0} max={100} levels={levels} trackWidth={width}/>{on(p,'Labels')?<div className={styles.between}><span>Низкий</span><span>Средний</span><span>Высокий</span></div>:null}</div>;
  if(i===137)return <div className={styles.trackPart} data-compressed={compressed}><EuiRangeTrack min={0} max={100} step={1} value={value} trackWidth={width} compressed={compressed}/></div>;
  const common={'aria-label':'Диапазон',min:0,max:100,compressed,disabled,showTicks:on(p,'Ticks'),ticks:on(p,'Ticks')?[{value:0,label:'0'},{value:50,label:'50'},{value:100,label:'100'}]:undefined,levels:on(p,'Levels')?levels:undefined,showRange:p['Show range']!=='False'&&p.State!=='Empty',showInput:i===138||!!p.Input&&p.Input!=='None',showLabels:!!p.Label&&p.Label!=='None'&&p.Label!=='False',onResize:setWidth};
  const rangeControl=i===132||p.Type==='Dual'?<E.EuiDualRange {...common} value={pair} onChange={v=>{const next:[number,number]=[Number(v[0]),Number(v[1])];setPair(next);emit(p,next);}}/>:<E.EuiRange {...common} value={value} onChange={e=>update(Number((e.target as HTMLInputElement).value))}/>;
  const control=<div className={styles.rangePart} data-input={String(p.Input)} data-labels={String(p.Label)}>{rangeControl}</div>;
  return i===138?<E.EuiFormRow label={on(p,'Label')?'Диапазон':undefined} helpText={on(p,'Help text')?'Выберите значение':undefined} isInvalid={p.State==='Invalid'} error={p.State==='Invalid'?['Проверьте значение']:undefined} display={on(p,'Column display')?'columnCompressed':compressed?'rowCompressed':'row'}>{control}</E.EuiFormRow>:control;
}

export function ElasticDatePart({index:i,values:p}:{index:number;values:VariantValues}) {
  const timeOptions=useI18nTimeOptions();
  const [start,setStart]=useVariantState(p.Time==='Absolute'?'2026-09-23T09:00:00.000Z':'now-15m');
  const [end,setEnd]=useState('now');
  const [paused,setPaused]=useVariantState(p['Auto refresh']!=='On');
  const [round,setRound]=useState(true);
  const [open,setOpen]=useVariantState(p.State==='Active / Open');
  const [needsUpdate,setNeedsUpdate]=useVariantState(on(p,'Needs update')||p.State==='Needs updating');
  const apply=()=>{setNeedsUpdate(false);emit(p,{start,end});};
  const quickSelect=<E.EuiQuickSelect start={start} end={end} timeOptions={timeOptions} applyTime={({start,end})=>{setStart(start);setEnd(end);setNeedsUpdate(true);setOpen(false);emit(p,{start,end});}}/>;
  if(i===168)return <E.EuiPopover isOpen={open} closePopover={()=>setOpen(false)} button={<E.EuiButtonIcon aria-label="Быстрый выбор периода" iconType={DesignIcon} display="base" onClick={()=>setOpen(!open)} aria-expanded={open}/>}>{quickSelect}</E.EuiPopover>;
  if(i===170)return <div className={styles.dateButtons}><E.EuiPopover isOpen={open} closePopover={()=>setOpen(false)} button={<E.EuiButton size="s" fill={open||needsUpdate} iconType={DesignIcon} onClick={()=>setOpen(!open)} aria-expanded={open}>Last 15 min</E.EuiButton>}>{quickSelect}</E.EuiPopover><E.EuiButtonIcon size="s" display={needsUpdate?'fill':'base'} aria-label="Обновить данные" iconType={DesignIcon} onClick={apply} isLoading={p.State==='Auto refresh'}/></div>;
  if(i===172)return <E.EuiPopoverFooter><div className={styles.between}><E.EuiSwitch label="Округлить до ближайшей минуты" checked={round} onChange={()=>setRound(!round)} compressed disabled={on(p,'Disabled')}/><E.EuiButton size="s" fill isDisabled={on(p,'Disabled')} onClick={apply}>Применить</E.EuiButton></div></E.EuiPopoverFooter>;
  if(i===171)return <E.EuiRelativeTab value={start} onChange={setStart} dateFormat="DD.MM.YYYY HH:mm" labelPrefix="Начало" timeOptions={timeOptions}/>;
  if(i===169)return p['Tab select']==='Quick select'?<E.EuiQuickSelect start={start} end={end} timeOptions={timeOptions} applyTime={({start,end})=>{setStart(start);setEnd(end);emit(p,{start,end});}}/>:<E.EuiDatePopoverContent value={start} onChange={setStart} position="start" dateFormat="DD.MM.YYYY" timeFormat="HH:mm" timeOptions={timeOptions}/>;
  return <div className={styles.dateButtons}><E.EuiSuperDatePicker start={start} end={end} isPaused={paused} refreshInterval={10000} onRefresh={apply} onRefreshChange={({isPaused})=>setPaused(isPaused)} onTimeChange={({start,end})=>{setStart(start);setEnd(end);setNeedsUpdate(p['Show update button']!=='False');emit(p,{start,end});}} showUpdateButton={false}/>{p['Show update button']!=='False'?<E.EuiSuperUpdateButton needsUpdate={needsUpdate} onClick={apply} iconOnly={p['Show update button']==='Icon only'} showTooltip={false}/>:null}</div>;
}

export function ElasticPopoverPart({index:i,values:p}:{index:number;values:VariantValues}) {
  const [open,setOpen]=useState(false);
  const body=<E.EuiText size="s"><p>{p.children as ReactNode||'Содержимое подсказки'}</p></E.EuiText>;
  const footer=<E.EuiButton size="m" onClick={()=>{setOpen(false);if(typeof p.onClick==='function')p.onClick();}}>Действие</E.EuiButton>;
  if(i===127)return <div className={styles.popoverBody}>{body}</div>;
  if(i===128)return <E.EuiPopoverFooter>{footer}</E.EuiPopoverFooter>;
  if(i===129)return <div className={styles.arrowPart}><EuiPopoverArrow position="bottom"/></div>;
  return <E.EuiPopover button={<E.EuiButtonEmpty onClick={()=>setOpen(!open)}>Открыть</E.EuiButtonEmpty>} isOpen={open} closePopover={()=>setOpen(false)} anchorPosition={String(p.Arrow).startsWith('3')?'rightCenter':String(p.Arrow).startsWith('9')?'leftCenter':String(p.Arrow).startsWith('12')?'upCenter':'downCenter'}>{on(p,'Header')?<E.EuiPopoverTitle>Заголовок</E.EuiPopoverTitle>:null}{body}{on(p,'Footer')?<E.EuiPopoverFooter>{footer}</E.EuiPopoverFooter>:null}</E.EuiPopover>;
}

export function ElasticTourPart({index:i,values:p}:{index:number;values:VariantValues}) {
  const [open,setOpen]=useState(false);
  const [step,setStep]=useState(1);
  if(i===198||i===199)return <span className={styles.beacon} data-arrow={i===198} aria-hidden="true"><span/><span/><span/></span>;
  if(i===200||i===201)return <ul className={styles.dots}>{Array.from({length:i===201?1:5},(_,n)=>{const key=['1st step','2nd step','3rd step','4th step','5th step'][n];return i===200&&valueOf(p,key)!==undefined&&!on(p,key)?null:<E.EuiTourStepIndicator key={n} number={n+1} status={i===201?(on(p,'Filled')?'active':'incomplete'):Number(p['Active step'])===n+1?'active':'incomplete'}/>;})}</ul>;
  return <E.EuiTourStep panelClassName={on(p,'Dots')?undefined:styles.tourNoDots} isStepOpen={open} onFinish={()=>setOpen(false)} closePopover={()=>setOpen(false)} title={on(p,'Title')?'Знакомство с разделом':''} subtitle={on(p,'Meta Title')?'Начало работы':undefined} content={on(p,'Description')?<p>Описание возможности.</p>:null} step={step} stepsTotal={5} anchorPosition={String(p.Arrow).includes('Right')?'rightCenter':String(p.Arrow).includes('Left')?'leftCenter':String(p.Arrow).includes('Top')?'upCenter':'downCenter'} footerAction={<div className={styles.between}>{on(p,'Skip')?<E.EuiButtonEmpty size="s" onClick={()=>setOpen(false)}>Пропустить</E.EuiButtonEmpty>:null}{on(p,'Next')?<E.EuiButton size="s" onClick={()=>setStep(step===5?1:step+1)}>Далее</E.EuiButton>:null}</div>} decoration="none"><E.EuiButton onClick={()=>setOpen(true)}>Показать подсказку</E.EuiButton></E.EuiTourStep>;
}
