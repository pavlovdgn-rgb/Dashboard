import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Range.module.css';
export type RangeProps = CatalogProps & {
  "State"?: "Filled" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function Range(props: RangeProps) { return <CatalogComponent catalogId="15884:193897" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
