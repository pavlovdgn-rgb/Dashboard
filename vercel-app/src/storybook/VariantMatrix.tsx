import type { ComponentType } from 'react';
import catalog from '../components/catalog.json';
import type { CatalogProps } from '../components/_shared/CatalogComponent';
import styles from './catalog.module.css';

/** Every original combination is shown. Portal-heavy samples get their own document. */
export function VariantMatrix({catalogId,component:Component,storyId}:{catalogId:string;component:ComponentType<CatalogProps>;storyId:string}) {
  const entry=catalog.find(c=>c.id===catalogId)!;
  const isolated=entry.source==='elastic'&&/popover|modal|flyout|tour|auto refresh|date picker/i.test(entry.name);
  return <div className={styles.matrix} data-matrix-count={entry.variants.length}>{entry.variants.map((variant,n)=><article key={n} className={styles.variant}>
    <h3><a href={`?path=/story/${storyId}--variant-${String(n+1).padStart(3,'0')}`} target="_top">{Object.entries(variant).map(([key,value])=>`${key}: ${value}`).join(' · ')||'Default'}</a></h3>
    {isolated?<iframe title={`${entry.name} ${n+1}`} loading="lazy" src={`iframe.html?id=${storyId}--variant-${String(n+1).padStart(3,'0')}&viewMode=story`}/>:<div className={styles.example}><Component {...variant}/></div>}
  </article>)}</div>;
}
