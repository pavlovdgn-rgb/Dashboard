import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListEmpty.module.css';
export type SelectableListEmptyProps = CatalogProps & {

};
export function SelectableListEmpty(props: SelectableListEmptyProps) { return <CatalogComponent catalogId="16122:18049" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
