import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListLoading.module.css';
export type SelectableListLoadingProps = CatalogProps & {

};
export function SelectableListLoading(props: SelectableListLoadingProps) { return <CatalogComponent catalogId="16122:18050" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
