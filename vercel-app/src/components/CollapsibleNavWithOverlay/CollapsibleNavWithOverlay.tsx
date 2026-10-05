import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CollapsibleNavWithOverlay.module.css';
export type CollapsibleNavWithOverlayProps = CatalogProps & {

};
export function CollapsibleNavWithOverlay(props: CollapsibleNavWithOverlayProps) { return <CatalogComponent catalogId="15213:169" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
