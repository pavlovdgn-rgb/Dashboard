import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilterButton.module.css';
export type FilterButtonProps = CatalogProps & {
  "With next#39823:0"?: boolean;
  "Active"?: "False" | "true";
  "Count"?: "true" | "false";
  "Icon"?: "None" | "Left" | "Right";
  "Disabled"?: "False" | "True";
  "Size"?: "Medium*" | "Small";
};
export function FilterButton(props: FilterButtonProps) { return <CatalogComponent catalogId="39838:197" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
