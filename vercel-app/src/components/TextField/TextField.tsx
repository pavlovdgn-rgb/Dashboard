import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextField.module.css';
export type TextFieldProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function TextField(props: TextFieldProps) { return <CatalogComponent catalogId="13676:796" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
