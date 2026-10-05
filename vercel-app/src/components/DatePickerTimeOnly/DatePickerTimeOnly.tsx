import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DatePickerTimeOnly.module.css';
export type DatePickerTimeOnlyProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function DatePickerTimeOnly(props: DatePickerTimeOnlyProps) { return <CatalogComponent catalogId="15884:162483" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
