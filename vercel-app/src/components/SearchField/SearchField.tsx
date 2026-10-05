import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SearchField.module.css';
export type SearchFieldProps = CatalogProps & {
  "State"?: "Placeholder" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function SearchField(props: SearchFieldProps) { return <CatalogComponent catalogId="15883:136359" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
