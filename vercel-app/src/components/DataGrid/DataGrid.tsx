import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataGrid.module.css';
export type DataGridProps = CatalogProps & {
  "Toolbar#46516:0"?: boolean;
  "Pagination#46516:5"?: boolean;
  "Border"?: "None" | "Horizontal" | "All";
  "Padding"?: "Condensed" | "Normal" | "Expanded";
  "Structured By"?: "Row" | "Column";
};
export function DataGrid(props: DataGridProps) { return <CatalogComponent catalogId="46305:10421" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
