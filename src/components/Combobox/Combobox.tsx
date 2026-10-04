import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Combobox.module.css';
export type ComboboxProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled" | "Placeholder";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function Combobox(props: ComboboxProps) { return <CatalogComponent catalogId="15883:161301" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
