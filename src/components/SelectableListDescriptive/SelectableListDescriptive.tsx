import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListDescriptive.module.css';
export type SelectableListDescriptiveProps = CatalogProps & {

};
export function SelectableListDescriptive(props: SelectableListDescriptiveProps) { return <CatalogComponent catalogId="14665:82478" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
