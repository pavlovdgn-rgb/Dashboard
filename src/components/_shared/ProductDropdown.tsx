import { useLayoutEffect, useRef, useState } from 'react';
import { EuiContextMenuItem, EuiContextMenuPanel, EuiPopover } from '@elastic/eui';
import { ProductAction } from './ProductComponent';
import styles from './ProductComponent.module.css';

/** ProductButton + the source EUI menu: consistent gutters instead of an OS select popup. */
export function ProductDropdown({label,value,options,onChange,icon,placeholder,appearance='button',disabled=false}:{label:string;value:string;options:{value:string;label:string}[];onChange:(value:string)=>void;icon?:string;placeholder?:string;appearance?:'button'|'field';disabled?:boolean}) {
  const [open,setOpen]=useState(false);
  const anchor=useRef<HTMLSpanElement>(null);
  const [width,setWidth]=useState<number>();
  useLayoutEffect(()=>{
    const element=anchor.current;if(!element)return;
    const measure=()=>setWidth(element.getBoundingClientRect().width);
    measure();const observer=new ResizeObserver(measure);observer.observe(element);
    return()=>observer.disconnect();
  },[]);
  const dropdown=<EuiPopover isOpen={open&&!disabled} closePopover={()=>setOpen(false)} hasArrow={false} offset={4} panelPaddingSize="none" panelStyle={{width}} panelClassName={styles.dropdownPanel} anchorPosition="downLeft" button={<span ref={anchor} className={styles.dropdownAnchor}><ProductAction state={disabled?'Disabled':'Default'} label={label} icon={icon} iconRight="arrowDown" expanded={open&&!disabled} hasPopup="menu" onClick={()=>setOpen(!open)}>{options.find(option=>option.value===value)?.label||placeholder}</ProductAction></span>}>
    <EuiContextMenuPanel className={styles.dropdownMenu} role="menu" aria-label={label} initialFocusedItemIndex={Math.max(0,options.findIndex(option=>option.value===value))} items={options.map(option=><EuiContextMenuItem role="menuitemradio" aria-checked={option.value===value} className={styles.dropdownItem} key={option.value} icon={option.value===value?'check':'empty'} onClick={()=>{onChange(option.value);setOpen(false);}}>{option.label}</EuiContextMenuItem>)}/>
  </EuiPopover>;
  return appearance==='field'?<div className={styles.dropdownField}><span className={styles.muted}>{label}</span>{dropdown}</div>:dropdown;
}
