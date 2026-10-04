import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataGridBodyRow.module.css';
export type DataGridBodyRowProps = CatalogProps & {
  "Borders"?: "None" | "Horizontal" | "All";
};
export function DataGridBodyRow(props: DataGridBodyRowProps) { return <CatalogComponent catalogId="46305:10098" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
