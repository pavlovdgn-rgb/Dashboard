import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectField.module.css';
export type SelectFieldProps = CatalogProps & {
  "State"?: "Default" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function SelectField(props: SelectFieldProps) { return <CatalogComponent catalogId="15883:129716" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
