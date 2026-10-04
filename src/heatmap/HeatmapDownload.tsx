import { useLayoutEffect,useRef,useState } from 'react';
import { EuiContextMenuItem,EuiContextMenuPanel,EuiPopover } from '@elastic/eui';
import { ProductAction } from '../components/_shared/ProductComponent';
import menu from '../components/_shared/ProductComponent.module.css';
import s from './LocalHeatmap.module.css';

export function HeatmapDownload({busy,disabled,onDownload}:{busy:boolean;disabled:boolean;onDownload:(format:'png'|'zip')=>void}) {
  const [open,setOpen]=useState(false),[width,setWidth]=useState<number>();
  const anchor=useRef<HTMLSpanElement>(null);
  useLayoutEffect(()=>{
    const element=anchor.current;if(!element)return;
    const measure=()=>setWidth(element.getBoundingClientRect().width);
    measure();const observer=new ResizeObserver(measure);observer.observe(element);
    return()=>observer.disconnect();
  },[]);
  const choose=(format:'png'|'zip')=>{setOpen(false);if(!busy&&!disabled)onDownload(format);};
  return <EuiPopover isOpen={open&&!busy&&!disabled} closePopover={()=>setOpen(false)} hasArrow={false} offset={8} panelPaddingSize="none" panelStyle={{width}} panelClassName={menu.dropdownPanel} anchorPosition="downRight" button={
    <span ref={anchor} className={s.downloadAnchor} role="group" aria-label="Скачивание тепловой карты" aria-busy={busy}>
      <ProductAction kind="Secondary" state={busy?'Loading':disabled?'Disabled':'Default'} icon={busy?undefined:'download'} onClick={()=>choose('png')}>{busy?'Подготовка…':'Скачать'}</ProductAction>
      <ProductAction kind="Secondary" state={busy||disabled?'Disabled':'Default'} label="Варианты скачивания" iconRight="arrowDown" expanded={open&&!busy&&!disabled} hasPopup="menu" onClick={()=>setOpen(!open)}/>
    </span>
  }><EuiContextMenuPanel role="menu" aria-label="Скачать тепловую карту" initialFocusedItemIndex={0} items={[
    <EuiContextMenuItem role="menuitem" key="png" className={menu.dropdownItem} onClick={()=>choose('png')}><span className={s.downloadChoice}><span>Текущий экран</span><span className={s.downloadFormat}>PNG</span></span></EuiContextMenuItem>,
    <EuiContextMenuItem role="menuitem" key="zip" className={menu.dropdownItem} onClick={()=>choose('zip')}><span className={s.downloadChoice}><span>Все экраны</span><span className={s.downloadFormat}>ZIP</span></span></EuiContextMenuItem>
  ]}/></EuiPopover>;
}
