import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilePicker.module.css';
export type FilePickerProps = CatalogProps & {
  "Size"?: "Default" | "Large";
  "State"?: "Disabled" | "Filled" | "Focus" | "Invalid" | "Placeholder";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "False" | "True";
  "Help text"?: "False" | "True";
};
export function FilePicker(props: FilePickerProps) { return <CatalogComponent catalogId="26803:282479" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
