import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TableCellHeader.module.css';
export type TableCellHeaderProps = CatalogProps & {
  "Sort"?: "Ascending" | "Descending" | "None";
  "Compressed"?: "No" | "Yes";
  "Tooltip"?: "No" | "Yes";
};
export function TableCellHeader(props: TableCellHeaderProps) { return <CatalogComponent catalogId="15035:3348" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
