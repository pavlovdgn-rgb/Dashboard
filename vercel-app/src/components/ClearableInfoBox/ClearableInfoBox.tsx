import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ClearableInfoBox.module.css';
export type ClearableInfoBoxProps = CatalogProps & {

};
export function ClearableInfoBox(props: ClearableInfoBoxProps) { return <CatalogComponent catalogId="16160:207647" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
