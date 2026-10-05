import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TableUtilityBar.module.css';
export type TableUtilityBarProps = CatalogProps & {
  "Multiple pages"?: "False" | "True";
  "Selection"?: "None" | "Whole page" | "Few";
  "Extra actions"?: "False" | "True";
};
export function TableUtilityBar(props: TableUtilityBarProps) { return <CatalogComponent catalogId="20805:282225" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
