import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataGridHeaderRow.module.css';
export type DataGridHeaderRowProps = CatalogProps & {
  "Border"?: "None" | "Horizontal" | "All";
  "Style"?: "Shade" | "Underline";
};
export function DataGridHeaderRow(props: DataGridHeaderRowProps) { return <CatalogComponent catalogId="46305:10129" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
