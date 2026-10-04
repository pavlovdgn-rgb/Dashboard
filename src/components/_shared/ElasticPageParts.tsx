import { useState } from 'react';
import * as E from '@elastic/eui';
import type { VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';
import { ElasticDatePart } from './ElasticParts';
import styles from './ElasticComponent.module.css';

export function ElasticPagePart({index:i,values:p}:{index:number;values:VariantValues}) {
  const [tab,setTab]=useState('one');
  const [collapsed,setCollapsed]=useVariantState(p.State==='Collapsed'||p['Side bar']==='Collapsed');
  const [query,setQuery]=useState('');
  const [selected,setSelected]=useState('one');
  const action=()=>{if(typeof p.onClick==='function')p.onClick();};
  const sidebar=<E.EuiPageSidebar sticky={false} paddingSize="m" minWidth={0}><E.EuiButtonEmpty size="s" aria-expanded={!collapsed} onClick={()=>setCollapsed(!collapsed)}>{collapsed?'Развернуть':'Свернуть'}</E.EuiButtonEmpty>{!collapsed?<E.EuiSideNav aria-label="Разделы" items={[{id:'group',name:'Раздел',items:[{id:'one',name:'Первый элемент',isSelected:selected==='one',onClick:()=>setSelected('one')},{id:'two',name:'Второй элемент',isSelected:selected==='two',onClick:()=>setSelected('two')}]}]}/>:null}</E.EuiPageSidebar>;
  const headerProps={pageTitle:p['Left content']==='Tabs as titles'?undefined:'Заголовок страницы',description:isOn(p['Description?'])?'Описание страницы':undefined,
    breadcrumbs:isOn(p.Breadcrumbs)?[{text:'UX-Lab'},{text:'Раздел'}]:undefined,
    tabs:p['Left content']==='Title'||i===114?undefined:[{label:'Первая',isSelected:tab==='one',onClick:()=>setTab('one')},{label:'Вторая',isSelected:tab==='two',onClick:()=>setTab('two')}],
    rightSideItems:p['Right content']==='Buttons'?[<E.EuiButton key="action" fill onClick={action}>Действие</E.EuiButton>]:p['Right content']==='Time or Custom'?[<ElasticDatePart key="time" index={173} values={{}}/>]:undefined};
  const bottomBorder=p['Bottom border']==='Extended'?'extended' as const:isOn(p['Bottom border']);
  const restrictWidth=isOn(p['Restrict width']);
  if(i===114||i===115)return <E.EuiPageHeaderContent {...headerProps}/>;
  if(i===116)return sidebar;
  if(i===117)return <E.EuiPageHeader {...headerProps} bottomBorder={bottomBorder} restrictWidth={restrictWidth}/>;
  if(i===118)return <E.EuiPageSection restrictWidth={restrictWidth} bottomBorder={bottomBorder} alignment={p['Vertical alignment']==='Center'?'center':undefined} color={isOn(p.Panelled)?'plain':'transparent'}><E.EuiText><p>Содержимое страницы</p></E.EuiText></E.EuiPageSection>;
  if(i===120)return <div className={styles.row}><E.EuiSelect aria-label="Источник данных" options={[{text:'Пример данных'},{text:'Другой источник'}]}/><div className={styles.grow}><E.EuiFieldSearch aria-label="Поиск данных" placeholder="Введите запрос" value={query} onChange={e=>setQuery(e.target.value)} fullWidth/></div><ElasticDatePart index={173} values={{}}/></div>;
  return <E.EuiPage paddingSize="m" restrictWidth={restrictWidth}>{p['Side bar']!=='False'?sidebar:null}<E.EuiPageBody><E.EuiPageHeader {...headerProps}/>{p.Template==='Default'?<E.EuiPageSection><E.EuiPanel>Содержимое страницы</E.EuiPanel></E.EuiPageSection>:<E.EuiPageSection color={p.Template==='Empty content'?'plain':'transparent'}><E.EuiEmptyPrompt title={<h3>Нет данных</h3>} body={<p>Здесь появятся результаты.</p>}/></E.EuiPageSection>}{isOn(p['Bottom bar'])?<div className={styles.bottomBar}><span>Действия страницы</span><E.EuiButton onClick={action}>Сохранить</E.EuiButton></div>:null}</E.EuiPageBody></E.EuiPage>;
}
