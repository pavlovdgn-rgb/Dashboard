import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DatePickerRange.module.css';
export type DatePickerRangeProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function DatePickerRange(props: DatePickerRangeProps) { return <CatalogComponent catalogId="15884:158445" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
