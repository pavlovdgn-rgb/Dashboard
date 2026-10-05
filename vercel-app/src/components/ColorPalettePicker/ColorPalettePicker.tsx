import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ColorPalettePicker.module.css';
export type ColorPalettePickerProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function ColorPalettePicker(props: ColorPalettePickerProps) { return <CatalogComponent catalogId="15884:173636" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
