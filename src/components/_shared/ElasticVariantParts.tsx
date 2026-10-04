import { useId, useState, type CSSProperties } from 'react';
import * as E from '@elastic/eui';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';
import styles from './ElasticVariantParts.module.css';

const emit=(p:VariantValues,value:unknown)=>{if(typeof p.onChange==='function')p.onChange(value);};
const property=(p:VariantValues,key:string)=>p[key]??Object.entries(p).find(([name])=>name.startsWith(key+'#'))?.[1];
const avatarColor=(n:number)=>({'--avatar-fill':n===9?'var(--elastic-shades-light)':`var(--elastic-visualization-palettes-color-blind-behind-text-color-${n})`} as CSSProperties);

export function ElasticAvatarCollection({index,values:p}:{index:number;values:VariantValues}) {
  const initials=['AB','CD','EF','GH','IJ','KL','MN','OP','QR','ST'];
  const [options,setOptions]=useState<E.EuiSelectableOption[]>([{label:'Shared with',isGroupLabel:true},...initials.map((initial,n)=>({label:`Участник ${n+1}`,prepend:<E.EuiAvatar className={styles.avatar} style={avatarColor(n)} name={initial} initials={initial} type="space" size="s"/>}))]);
  const [open,setOpen]=useState(false);
  const list=<E.EuiPanel paddingSize="none" className={styles.avatarList}><E.EuiSelectable aria-label="Участники с доступом" options={options} onChange={setOptions} height={440} listProps={{showIcons:false}}>{list=>list}</E.EuiSelectable></E.EuiPanel>;
  if(index===6)return list;
  const size=p.Size==='X-Large'?'xl':p.Size==='Large'?'l':p.Size==='Medium'?'m':'s';
  return <E.EuiPopover isOpen={open} closePopover={()=>setOpen(false)} panelPaddingSize="none" button={<button className={styles.avatarGroup} data-size={size} aria-label="Показать участников" aria-expanded={open} onClick={()=>setOpen(!open)}>{initials.map((initial,n)=><E.EuiAvatar key={initial} className={styles.avatar} style={avatarColor(n)} name={n===9?'+1':initial} initials={n===9?'+1':initial} size={size}/>)}</button>}>{list}</E.EuiPopover>;
}

export function ElasticSourceCard({values:p}:{values:VariantValues}) {
  const id=useId();
  const [checked,setChecked]=useVariantState(isOn(p.Checked));
  const disabled=isOn(p.Disabled);
  const flag=(key:string,fallback=false)=>property(p,key)===undefined?fallback:isOn(property(p,key));
  const select=()=>{const next=p.Checkable==='Radio'?true:!checked;setChecked(next);emit(p,next);};
  if(p.Checkable==='Radio'||p.Checkable==='Checkbox')return <E.EuiPanel paddingSize="none" hasBorder hasShadow={false} className={styles.checkableCard} data-checked={checked}>
    <div className={styles.cardCheck}>{p.Checkable==='Radio'?<E.EuiRadio id={id} checked={checked} disabled={disabled} aria-label="Выбрать карточку" onChange={select}/>:<E.EuiCheckbox id={id} checked={checked} disabled={disabled} aria-label="Выбрать карточку" onChange={select}/>}</div>
    <label className={styles.cardDescription} htmlFor={id}>Описание карточки. Краткое пояснение в одну или две строки.</label>
  </E.EuiPanel>;
  const shared={title:flag('Title',true)?String(p.label||'Заголовок карточки'):'',description:flag('Description',true)?'Описание карточки. Краткое пояснение в одну или две строки.':undefined,isDisabled:disabled,icon:flag('Icon',true)?<DesignIcon/>:undefined,betaBadgeProps:flag('Badge')?{label:'Beta'}:undefined,selectable:flag('Selectable')?{isSelected:checked,onClick:select}:undefined};
  const footer=flag('Footer')?<E.EuiButton size="s" isDisabled={disabled} onClick={()=>{if(typeof p.onClick==='function')p.onClick();}}>Действие</E.EuiButton>:null;
  if(p.Layout==='Horizontal')return <E.EuiCard {...shared} className={styles.sourceCard} layout="horizontal">{footer}</E.EuiCard>;
  return <E.EuiCard {...shared} className={styles.sourceCard} layout="vertical" textAlign={String(p['Text Align']||'Left').toLowerCase() as 'left'|'center'|'right'} image={isOn(p.Image)?<div className={styles.cardImage} role="img" aria-label="Место изображения"/>:undefined} footer={footer}/>;
}

// EUI owns the controls; this small composition exposes the source's Open axis,
// which EuiAutoRefresh keeps private and therefore cannot be set by the catalog.
export function ElasticRefresh({index,values:p}:{index:number;values:VariantValues}) {
  const [open,setOpen]=useVariantState(isOn(p.Open));
  const [paused,setPaused]=useVariantState(index===1?!isOn(p.On):isOn(p.Paused));
  const [interval,setInterval]=useState(10000);
  const control=<E.EuiRefreshInterval isPaused={paused} refreshInterval={interval} onRefreshChange={next=>{setPaused(next.isPaused);setInterval(next.refreshInterval);emit(p,next);}}/>;
  if(index===1)return isOn(p['In popover'])?<E.EuiPanel paddingSize="s">{control}</E.EuiPanel>:control;
  const label=paused?'Off':`${interval/1000} seconds`;
  const toggle=()=>setOpen(!open);
  if(index===3)return <E.EuiPopover isOpen={open} closePopover={()=>setOpen(false)} button={<E.EuiButtonEmpty size="s" iconType={DesignIcon} aria-expanded={open} onClick={toggle}>{label}</E.EuiButtonEmpty>}>{control}</E.EuiPopover>;
  return <E.EuiInputPopover isOpen={open} closePopover={()=>setOpen(false)} input={<E.EuiFieldText aria-label="Автообновление" readOnly value={label} onClick={toggle} prepend={<E.EuiButtonEmpty size="s" color="text" onClick={toggle} aria-expanded={open} iconType={DesignIcon}>Auto refresh</E.EuiButtonEmpty>}/>}>{control}</E.EuiInputPopover>;
}

export function ElasticThumbnail({index,values:p}:{index:number;values:VariantValues}) {
  const [selected,setSelected]=useVariantState(p.State==='Selected');
  if(index===54)return <div className={styles.emptyThumbnail} data-primary={p.Type==='Primary'} aria-label={`Empty prompt · ${p.Type}`}>
    {p.Type==='Primary'?<div className={styles.illustration}><DesignIcon/></div>:null}<span className={styles.title}/><span className={styles.line}/><span className={styles.line}/><span className={styles.action}><span/></span>
  </div>;
  return <button className={styles.layoutThumbnail} data-type={String(p.Type)} data-selected={selected} aria-label={`Композиция ${p.Type}`} aria-pressed={selected} onClick={()=>{setSelected(!selected);emit(p,!selected);}}>
    {p.Type!=='Empty'?<span className={styles.sidebar}>{Array.from({length:5},(_,n)=><span key={n}/>)}</span>:null}
    <span className={styles.body}>{p.Type==='Multiple'?Array.from({length:6},(_,n)=><span key={n}/>):null}</span>
    {selected?<span className={styles.selectedIcon}><DesignIcon type="check"/></span>:null}
  </button>;
}

export function ElasticNestedNav({values:p}:{values:VariantValues}) {
  const [selected,setSelected]=useVariantState(isOn(p['Active?']));
  const [open,setOpen]=useVariantState(isOn(p['Open?']));
  const depth=Math.max(0,Math.min(3,Number(p['Nested level'])||0));
  return <div style={{paddingInlineStart:`calc(var(--size-base) * ${depth})`}} data-nested-level={depth}>
    <E.EuiSideNav aria-label="Навигация" items={[{id:'item',name:'Элемент',isSelected:selected,forceOpen:open,icon:isOn(p['Icon?'])?<DesignIcon/>:undefined,onClick:()=>{setSelected(!selected);setOpen(!open);emit(p,!selected);},items:isOn(p['Has child items?'])?[{id:'child',name:'Вложенный элемент',onClick:()=>emit(p,'child')}]:undefined}]}/>
  </div>;
}

export function ElasticFileField({index,values:p}:{index:number;values:VariantValues}) {
  const id=useId();
  const [revision,setRevision]=useState(0);
  const [filename,setFilename]=useVariantState(p.State==='Filled'?'example.txt':'');
  const invalid=p.State==='Invalid';
  return <E.EuiFormRow label={isOn(p.Label)?'Название поля':undefined} helpText={isOn(p['Help text'])?'Выберите файл':undefined} isInvalid={invalid} error={invalid?['Проверьте файл']:undefined} display={isOn(p['Column display'])?'columnCompressed':isOn(p.Compressed)?'rowCompressed':'row'}>
    <div><E.EuiFilePicker key={revision} id={id} aria-label="Выберите файл" initialPromptText={filename||'Выберите файл'} display={p.Size==='Large'||index===86?'large':'default'} disabled={p.State==='Disabled'} isInvalid={invalid} compressed={isOn(p.Compressed)} onChange={files=>{setFilename(files?.[0]?.name||'');emit(p,files);}}/>
    {filename?<E.EuiButtonEmpty size="xs" onClick={()=>{setFilename('');setRevision(v=>v+1);emit(p,null);}}>Удалить файл</E.EuiButtonEmpty>:null}</div>
  </E.EuiFormRow>;
}
