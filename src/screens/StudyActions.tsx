import { useState } from 'react';
import { EuiButton, EuiButtonIcon, EuiContextMenuItem, EuiContextMenuPanel, EuiPopover } from '@elastic/eui';
import type { Study } from '../data/workspace';
import { useResearch } from '../data/researchStore';
import { useWireRoute } from './useWireRoute';
import menuStyles from '../components/_shared/ProductComponent.module.css';
import s from './Workspace.module.css';

/** One visible next step; secondary launch management stays in the row menu. */
export function StudyActions({study}:{study:Study}) {
  const [open,setOpen]=useState(false);
  const store=useResearch(),{navigate}=useWireRoute();
  const go=(screen:'setup'|'overview'|'launch')=>{
    setOpen(false);
    store.activateStudy(study.id);
    navigate({screen,scenario:'',item:''});
  };
  return <div className={s.studyActions}>
    <EuiButton data-row-action className={s.studyAction} size="s" iconType="arrowRight" iconSide="right" onClick={()=>go(study.status==='draft'?'setup':'overview')}>
      {study.status==='draft'?'Продолжить настройку':'Результаты'}
    </EuiButton>
    {study.status==='active'?<EuiPopover isOpen={open} closePopover={()=>setOpen(false)} anchorPosition="downRight" panelPaddingSize="none" panelClassName={menuStyles.dropdownPanel} button={
      <EuiButtonIcon className={s.studyMore} iconType="boxesHorizontal" aria-label={`Дополнительные действия: ${study.title}`} aria-haspopup="menu" aria-expanded={open} onClick={()=>setOpen(!open)}/>
    }>
      <EuiContextMenuPanel initialFocusedItemIndex={0} aria-label={`Действия исследования: ${study.title}`} items={[
        <EuiContextMenuItem key="launch" className={menuStyles.dropdownItem} icon="play" onClick={()=>go('launch')}>Управление запуском</EuiContextMenuItem>,
      ]}/>
    </EuiPopover>:<span aria-hidden="true"/>}
  </div>;
}
