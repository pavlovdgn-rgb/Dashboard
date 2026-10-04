import { useState } from 'react';
import { EuiToast, EuiButtonEmpty, EuiToolTip } from '@elastic/eui';
import type { VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import styles from './ElasticComponent.module.css';

export function ElasticNotifications({index,values:p}:{index:number;values:VariantValues}) {
  const [visible,setVisible]=useState(index===196?[0,1,2]:[0]);
  const get=(key:string)=>p[key]??Object.entries(p).find(([name])=>name.startsWith(key+'#'))?.[1];
  if(index===197){
    const hour=parseInt(String(p.Direction));
    const position=hour===3?'right':hour===9?'left':[4,5,6,7,8].includes(hour)?'bottom':'top';
    return <EuiToolTip content={String(get('Description')||'Пояснение к действию')} title={isOn(get('Title'))?String(get('⮑ Title')||'Заголовок'):undefined} position={position}>{p.children as React.ReactElement||<button className={styles.textButton}>Наведите курсор</button>}</EuiToolTip>;
  }
  const color=p.Type==='Danger'?'danger':p.Type==='Warning'?'warning':p.Type==='Success'?'success':p.Type==='Info'?'primary':undefined;
  return <div className={styles.stack}>{index===196&&isOn(p.showClearAllButtonAt)&&visible.length?<EuiButtonEmpty onClick={()=>setVisible([])}>Очистить все</EuiButtonEmpty>:null}{visible.map(id=><EuiToast key={id} title={String(p.title||'Изменения сохранены')} color={color} iconType={isOn(p.Icon)?(p.Type==='Success'?'checkInCircleFilled':p.Type==='Danger'?'error':'info'):undefined} onClose={()=>setVisible(previous=>previous.filter(item=>item!==id))}><p>Краткое сообщение о результате.</p>{isOn(p.Button)?<EuiButtonEmpty size="s" onClick={()=>{if(typeof p.onClick==='function')p.onClick();}}>Действие</EuiButtonEmpty>:null}</EuiToast>)}{!visible.length?<EuiButtonEmpty onClick={()=>setVisible(index===196?[0,1,2]:[0])}>Показать уведомление</EuiButtonEmpty>:null}</div>;
}
