import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Textarea.module.css';
export type TextareaProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function Textarea(props: TextareaProps) { return <CatalogComponent catalogId="15883:148276" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
