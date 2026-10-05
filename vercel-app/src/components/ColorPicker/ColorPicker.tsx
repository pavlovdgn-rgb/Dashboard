import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ColorPicker.module.css';
export type ColorPickerProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function ColorPicker(props: ColorPickerProps) { return <CatalogComponent catalogId="15884:167851" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
