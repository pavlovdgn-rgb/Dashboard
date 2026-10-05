import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataGridToolbar.module.css';
export type DataGridToolbarProps = CatalogProps & {
  "Text #46240:0"?: boolean;
  "Sorted#46240:1"?: boolean;
  "Bulk Actions Button#46290:0"?: boolean;
  "Show columns#46905:0"?: boolean;
  "Border"?: "None" | "All" | "Horizontal";
};
export function DataGridToolbar(props: DataGridToolbarProps) { return <CatalogComponent catalogId="46305:10170" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
