import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CollapsibleNavGroupHeader.module.css';
export type CollapsibleNavGroupHeaderProps = CatalogProps & {

};
export function CollapsibleNavGroupHeader(props: CollapsibleNavGroupHeaderProps) { return <CatalogComponent catalogId="44991:80757" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
