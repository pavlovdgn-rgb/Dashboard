import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CheckboxBox.module.css';
export type CheckboxBoxProps = CatalogProps & {
  "Checked"?: "True" | "False";
  "Indeterminate"?: "False" | "True";
  "Disabled"?: "False" | "True";
  "Focus"?: "False" | "True";
  "Size"?: "Medium" | "Small";
};
export function CheckboxBox(props: CheckboxBoxProps) { return <CatalogComponent catalogId="16034:2" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
