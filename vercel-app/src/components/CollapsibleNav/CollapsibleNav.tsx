import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CollapsibleNav.module.css';
export type CollapsibleNavProps = CatalogProps & {

};
export function CollapsibleNav(props: CollapsibleNavProps) { return <CatalogComponent catalogId="20785:286768" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
