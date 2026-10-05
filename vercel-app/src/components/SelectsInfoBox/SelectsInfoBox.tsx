import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectsInfoBox.module.css';
export type SelectsInfoBoxProps = CatalogProps & {

};
export function SelectsInfoBox(props: SelectsInfoBoxProps) { return <CatalogComponent catalogId="16160:207356" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
