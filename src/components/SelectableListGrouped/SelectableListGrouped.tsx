import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListGrouped.module.css';
export type SelectableListGroupedProps = CatalogProps & {

};
export function SelectableListGrouped(props: SelectableListGroupedProps) { return <CatalogComponent catalogId="14674:1139" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
