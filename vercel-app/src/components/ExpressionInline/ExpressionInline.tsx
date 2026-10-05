import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ExpressionInline.module.css';
export type ExpressionInlineProps = CatalogProps & {
  "Clickable"?: "False" | "True";
  "Active"?: "False" | "True";
  "Color"?: "Success" | "Primary" | "Accent" | "Warning" | "Danger" | "Subdued";
  "Invalid"?: "False" | "True";
};
export function ExpressionInline(props: ExpressionInlineProps) { return <CatalogComponent catalogId="14849:51" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
