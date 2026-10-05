import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './NumberField.module.css';
export type NumberFieldProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function NumberField(props: NumberFieldProps) { return <CatalogComponent catalogId="15883:139856" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
