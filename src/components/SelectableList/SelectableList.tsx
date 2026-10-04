import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableList.module.css';
export type SelectableListProps = CatalogProps & {

};
export function SelectableList(props: SelectableListProps) { return <CatalogComponent catalogId="14665:82129" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
