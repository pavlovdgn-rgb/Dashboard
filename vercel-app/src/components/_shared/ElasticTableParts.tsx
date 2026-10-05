import { useId } from 'react';
import * as E from '@elastic/eui';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';
import styles from './ElasticComponent.module.css';

export function ElasticTablePart({index:i,values:p}:{index:number;values:VariantValues}) {
  const id=useId();
  const [selected,setSelected]=useVariantState(p.Selection==='None'?0:p.Selection==='Whole page'?10:3);
  const [checked,setChecked]=useVariantState(p.State==='Selected');
  const [ascending,setAscending]=useVariantState(p.Sort==='Ascending');
  const [expanded,setExpanded]=useVariantState(false);
  const disabled=isOn(p.Disabled);
  const action=()=>{if(typeof p.onClick==='function')p.onClick();};
  if(i===177||i===178)return <div className={styles.utilityBar}><span>Показаны 1–10 из 100</span><div className={styles.row}>{selected?<><span>{selected} выбрано</span>{isOn(p['Multiple pages'])?<E.EuiButtonEmpty size="s" onClick={()=>setSelected(100)}>Выбрать все 100</E.EuiButtonEmpty>:null}<E.EuiButtonEmpty size="s" onClick={()=>setSelected(0)}>Снять выбор</E.EuiButtonEmpty></>:null}{isOn(p['Extra actions'])||i===178?<E.EuiButtonEmpty size="s" onClick={action}>Действие</E.EuiButtonEmpty>:null}</div></div>;
  const content=p.Content==='Checkbox'?<E.EuiCheckbox id={id} aria-label="Выбрать строку" checked={checked} disabled={disabled} onChange={()=>setChecked(!checked)}/>:
    p.Content==='Badge'?<E.EuiBadge>Метка</E.EuiBadge>:
    p.Content==='Link'?<E.EuiLink disabled={disabled} onClick={action}>Подробнее</E.EuiLink>:
    p.Content==='Actions'?<E.EuiButtonEmpty size="s" isDisabled={disabled} onClick={action}>Действие</E.EuiButtonEmpty>:
    p.Content==='Status'?<E.EuiHealth color="success">Готово</E.EuiHealth>:
    p.Content==='Icon'?<DesignIcon/>:
    p.Content==='Expander'?<E.EuiButtonIcon iconType={DesignIcon} aria-label="Развернуть строку" aria-expanded={expanded} isDisabled={disabled} onClick={()=>setExpanded(!expanded)}/>:
    p.Content==='Text + Icon'?<span className={styles.row}><DesignIcon/>Значение</span>:'Значение';
  return <E.EuiTable compressed={isOn(p.Compressed)}>{i===174?<E.EuiTableHeader><E.EuiTableHeaderCell isSorted={p.Sort!=='None'} isSortAscending={ascending} onSort={p.Sort==='None'?undefined:()=>setAscending(!ascending)} tooltipProps={isOn(p.Tooltip)?{content:'Описание столбца'}:undefined}>Заголовок</E.EuiTableHeaderCell></E.EuiTableHeader>:i===175?<E.EuiTableFooter><E.EuiTableFooterCell>Итого</E.EuiTableFooterCell></E.EuiTableFooter>:<E.EuiTableBody><E.EuiTableRow isSelected={checked}><E.EuiTableRowCell>{content}</E.EuiTableRowCell></E.EuiTableRow>{expanded?<E.EuiTableRow><E.EuiTableRowCell>Подробности строки</E.EuiTableRowCell></E.EuiTableRow>:null}</E.EuiTableBody>}</E.EuiTable>;
}
