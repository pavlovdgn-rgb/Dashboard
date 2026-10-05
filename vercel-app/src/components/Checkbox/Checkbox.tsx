import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Checkbox.module.css';
export type CheckboxProps = CatalogProps & {
  "Label"?: "True" | "False";
  "Checked"?: "True" | "False";
  "Indeterminate"?: "False" | "True";
  "Disabled"?: "False" | "True";
  "Focus"?: "False" | "True";
};
export function Checkbox(props: CheckboxProps) { return <CatalogComponent catalogId="13581:24987" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
