import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TableUtilityBarBase.module.css';
export type TableUtilityBarBaseProps = CatalogProps & {

};
export function TableUtilityBarBase(props: TableUtilityBarBaseProps) { return <CatalogComponent catalogId="20805:284019" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
