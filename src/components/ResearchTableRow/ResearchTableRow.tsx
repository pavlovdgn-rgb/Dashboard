import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ResearchTableRow.module.css';
export type ResearchTableRowProps = CatalogProps & {
  "Columns"?: "2" | "3" | "4" | "5" | "6" | "7" | "8";
  "State"?: "Default" | "Zebra" | "Selected" | "Header";
};
export function ResearchTableRow(props: ResearchTableRowProps) { return <CatalogComponent catalogId="203:5669" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
