import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ComboboxInfoBox.module.css';
export type ComboboxInfoBoxProps = CatalogProps & {

};
export function ComboboxInfoBox(props: ComboboxInfoBoxProps) { return <CatalogComponent catalogId="16160:208934" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
