import { useState } from 'react';
import { EuiSelectable, EuiSelectableListItem, EuiFieldSearch, EuiLoadingSpinner, EuiColorPaletteDisplay, EuiText, EuiContextMenuItem, type EuiSelectableOption } from '@elastic/eui';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';
import manifest from '../../tokens/manifest.json';

const palette=manifest.tokens.filter(t=>t.type==='COLOR'&&t.name.includes('Color Blind')).slice(0,6).map(t=>Object.values(t.values)[0]);
export function ElasticSelectable({values:p,index}:{values:VariantValues;index:number}) {
  const [checked,setChecked]=useVariantState(isOn(p['Checked?']));
  const [query,setQuery]=useState('');
  const [options,setOptions]=useState<EuiSelectableOption[]>([
    ...(index===145?[{label:'Группа А',isGroupLabel:true}]:[]),
    {label:'Первый элемент',...(index===146?{append:<small>Описание элемента</small>}:{}),...(index===147?{append:<EuiColorPaletteDisplay palette={palette} type="fixed"/>}:{})},
    {label:'Второй элемент',...(index===146?{append:<small>Описание элемента</small>}:{}),...(index===147?{append:<EuiColorPaletteDisplay palette={[...palette].reverse()} type="fixed"/>}:{})},
  ]);
  const disabled=isOn(p['Disabled?']);
  const onChange=()=>{if(!disabled){setChecked(!checked);if(typeof p.onChange==='function')p.onChange(!checked);}};
  if(index===140){
    const type=String(p.Type);
    if(type==='Loading')return <EuiLoadingSpinner size="m" aria-label="Загрузка"/>;
    if(type==='Empty')return <EuiText size="s">Нет элементов</EuiText>;
    if(type==='Search')return <EuiFieldSearch aria-label="Поиск элементов" value={query} onChange={event=>setQuery(event.target.value)}/>;
    if(type==='Group title')return <EuiText size="s"><strong>Группа элементов</strong></EuiText>;
    if(type.startsWith('Context menu'))return <EuiContextMenuItem size={type.endsWith('(S)')?'s':'m'} disabled={disabled} onClick={onChange}>Элемент меню</EuiContextMenuItem>;
    return <ul><EuiSelectableListItem checked={checked?'on':undefined} disabled={disabled} isFocused={p.State==='Focus'} showIcons={p['Checked?']!=='N/A'} onClick={onChange}
      prepend={p.Extras==='Prepend'||p.Extras==='Both'?<DesignIcon/>:undefined}
      append={type==='Color palette'?<EuiColorPaletteDisplay palette={palette} type="fixed"/>:p.Extras==='Append'||p.Extras==='Both'?<DesignIcon/>:undefined}>Элемент списка</EuiSelectableListItem></ul>;
  }
  return <EuiSelectable aria-label="Выбор элементов" searchable={index===142} isLoading={index===143}
    options={index===144?[]:options} onChange={setOptions} emptyMessage="Нет элементов" noMatchesMessage="Ничего не найдено">
    {(list,search)=><>{search}{list}</>}
  </EuiSelectable>;
}
