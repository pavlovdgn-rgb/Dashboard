import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControl.module.css';
export type FormControlProps = CatalogProps & {
  "Type"?: "Text" | "Search" | "Select" | "Number" | "Textarea" | "Password" | "Combobox" | "Color palette";
  "Compressed"?: "True" | "False";
  "State"?: "Filled" | "Placeholder" | "Focus" | "Invalid" | "Read-only" | "Disabled";
  "Prepend / Append"?: "None" | "Prepend" | "Append" | "Both";
  "Icon"?: "None" | "Left" | "Right" | "Both";
  "Loading"?: "False" | "True";
  "Clearble"?: "False" | "True";
};
export function FormControl(props: FormControlProps) { return <CatalogComponent catalogId="13580:25572" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
