import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ExpressionColumn.module.css';
export type ExpressionColumnProps = CatalogProps & {
  "Clickable"?: "True" | "False";
  "Active"?: "False" | "True";
  "Color"?: "Success" | "Primary" | "Accent" | "Warning" | "Danger" | "Subdued";
  "Invalid"?: "False" | "True";
};
export function ExpressionColumn(props: ExpressionColumnProps) { return <CatalogComponent catalogId="14850:110142" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
