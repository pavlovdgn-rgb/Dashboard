import {useState} from 'react';
import {EuiContextMenuItem,EuiContextMenuPanel,EuiPopover} from '@elastic/eui';
import {DesignIcon} from './CatalogComponent';
import styles from './ProductComponent.module.css';

export type StudyNavigationProps={studies:ReadonlyArray<{studyId:string;studyTitle:string}>;selectedStudy:string;onSelectStudy:(id:string)=>void;onOpenStudies:()=>void;active:boolean};
export function StudyNavigation({studies,selectedStudy,onSelectStudy,onOpenStudies,active}:StudyNavigationProps){
  const [expanded,setExpanded]=useState(false);
  const selected=studies.find(study=>study.studyId===selectedStudy);
  return <EuiPopover className={styles.studyPicker} isOpen={expanded} closePopover={()=>setExpanded(false)} anchorPosition="downLeft" repositionToCrossAxis={false} hasArrow={false} offset={4} panelPaddingSize="none" panelClassName={styles.studyPickerPanel} button={
    <button className={`${styles.navItem} ${styles.studyPickerTrigger}`} aria-label="Выбрать исследование" title={selected?.studyTitle} aria-haspopup="menu" aria-expanded={expanded} data-selected={active} onClick={()=>setExpanded(!expanded)}><DesignIcon type="folderClosed"/><span>{selected?.studyTitle||'Выбрать исследование'}</span><DesignIcon type={expanded?'arrowUp':'arrowDown'}/></button>
  }><EuiContextMenuPanel role="menu" aria-label="Исследования проекта" items={[
    ...studies.map(study=><EuiContextMenuItem key={study.studyId} role="menuitemradio" aria-checked={study.studyId===selectedStudy} icon={study.studyId===selectedStudy?'check':'empty'} onClick={()=>{setExpanded(false);onSelectStudy(study.studyId);}}>{study.studyTitle}</EuiContextMenuItem>),
    <EuiContextMenuItem key="all" role="menuitem" icon="folderOpen" onClick={()=>{setExpanded(false);onOpenStudies();}}>Все исследования проекта</EuiContextMenuItem>
  ]}/></EuiPopover>;
}
