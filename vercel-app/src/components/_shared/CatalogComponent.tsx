import { createContext, useContext, type ReactNode } from 'react';
import { EuiIcon } from '@elastic/eui';
import catalog from '../catalog.json';
import { ElasticComponent } from './ElasticComponent';
import { ProductComponent } from './ProductComponent';
import styles from './CatalogComponent.module.css';
import { ProductTheme } from '../../tokens/ProductTheme';
import { isOn } from './variantValues';
import { iconAliases as aliases, sourceIconName } from './sourceIconName';

export type CatalogProps = {
  children?: ReactNode;
  className?: string;
  label?: string;
  onClick?: () => void;
  onChange?: (value: unknown) => void;
  [property: string]: unknown;
};
export type VariantValues = Record<string, unknown>;
const DefaultIcon=createContext('accessibility');
export function DesignIcon({type,size='m',className}:{type?:string;size?:'s'|'m'|'l'|'xl'|'original';className?:string}) { const fallback=useContext(DefaultIcon);return <EuiIcon type={aliases[type||fallback]||type||fallback} size={size} className={className} aria-hidden="true"/>; }
export function CatalogComponent({ catalogId, className, ...props }: CatalogProps & { catalogId: string }) {
  const entry = catalog.find(c => c.id === catalogId);
  if (!entry) throw new Error(`Unknown catalog entry: ${catalogId}`);
  const values = { ...entry.defaults, ...props } as VariantValues;
  const state = String(values.State || (isOn(values.Focus)||values.Type==='Focus' ? 'Focus' : isOn(values.Hover)?'Hover':'Default'));
  const icon=Object.entries(values).filter(([key])=>key.includes('Icon')).map(([,value])=>sourceIconName(value)).find(Boolean)||'accessibility';
  return <DefaultIcon.Provider value={icon}><div className={[styles.sample, className].join(' ')} data-component-id={catalogId} data-source={entry.source} data-state={state} data-selected={isOn(values.Selected)}>
    {entry.source === 'elastic'
      ? <ElasticComponent index={entry.sourceIndex} values={values} />
      : <ProductTheme><ProductComponent name={entry.name} values={values} /></ProductTheme>}
  </div></DefaultIcon.Provider>;
}
