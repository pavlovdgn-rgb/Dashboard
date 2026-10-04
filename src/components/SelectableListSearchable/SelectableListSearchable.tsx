import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListSearchable.module.css';
export type SelectableListSearchableProps = CatalogProps & {

};
export function SelectableListSearchable(props: SelectableListSearchableProps) { return <CatalogComponent catalogId="14674:8052" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
