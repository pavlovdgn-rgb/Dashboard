import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TableCell.module.css';
export type TableCellProps = CatalogProps & {
  "Content"?: "Text" | "Link" | "Icon" | "Checkbox" | "Badge" | "Status" | "Expander" | "Actions" | "Text + Icon";
  "State"?: "Default" | "Hover" | "Selected";
  "Compressed"?: "False" | "True";
  "Disabled"?: "False" | "True";
};
export function TableCell(props: TableCellProps) { return <CatalogComponent catalogId="15038:108556" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
