import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CollapsibleNavGroupBase.module.css';
export type CollapsibleNavGroupBaseProps = CatalogProps & {

};
export function CollapsibleNavGroupBase(props: CollapsibleNavGroupBaseProps) { return <CatalogComponent catalogId="20785:283722" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
