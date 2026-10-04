import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Progress.module.css';
export type ProgressProps = CatalogProps & {
  "Size"?: "X-Small - 2px" | "Small - 4px" | "Medium* - 8px" | "Large - 16px";
  "Color"?: "Success*" | "Primary" | "Warning" | "Danger" | "Subdued" | "Accent";
  "Label"?: "False" | "True";
};
export function Progress(props: ProgressProps) { return <CatalogComponent catalogId="13648:4438" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
