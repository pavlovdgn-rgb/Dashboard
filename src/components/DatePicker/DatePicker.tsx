import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DatePicker.module.css';
export type DatePickerProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function DatePicker(props: DatePickerProps) { return <CatalogComponent catalogId="15884:160184" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
