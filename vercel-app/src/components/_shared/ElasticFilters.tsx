import * as E from '@elastic/eui';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { isOn } from './variantValues';
import { useVariantState } from './useVariantState';

export function ElasticFilters({index:i,values:p}:{index:number;values:VariantValues}) {
  const [active,setActive]=useVariantState(isOn(p.Selected)||isOn(p.Active)?'0':'');
  const disabled=isOn(p.Disabled);
  const choose=(id:string)=>{const next=active===id?'':id;setActive(next);if(typeof p.onChange==='function')p.onChange(next);};
  if(i>=62&&i<=64)return <E.EuiFacetGroup>{Array.from({length:i===63?4:1},(_,n)=><E.EuiFacetButton key={n} quantity={n+1} isSelected={active===String(n)} isDisabled={disabled} isLoading={isOn(p.Loading)} icon={isOn(p.Icon)||i===64?<DesignIcon/>:undefined} onClick={()=>choose(String(n))}>{i===63?`Элемент ${n+1}`:'Пример'}</E.EuiFacetButton>)}</E.EuiFacetGroup>;
  return <E.EuiFilterGroup compressed={isOn(p.Compressed)||p.Size==='Small'}>{Array.from({length:i===67?4:i===66?2:1},(_,n)=><E.EuiFilterButton key={n} hasActiveFilters={active===String(n)} isSelected={active===String(n)} isDisabled={disabled} numFilters={p.Count==='false'?undefined:n+1} numActiveFilters={active===String(n)?1:0} iconType={p.Icon&&p.Icon!=='None'?DesignIcon:undefined} iconSide={p.Icon==='Left'?'left':'right'} onClick={()=>choose(String(n))}>{i===67||i===66?`Фильтр ${n+1}`:'Фильтр'}</E.EuiFilterButton>)}</E.EuiFilterGroup>;
}
