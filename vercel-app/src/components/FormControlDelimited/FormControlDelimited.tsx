import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControlDelimited.module.css';
export type FormControlDelimitedProps = CatalogProps & {
  "State"?: "Filled" | "Placeholder" | "Focus" | "Invalid" | "Disabled" | "Read-only";
  "Compressed"?: "False" | "True";
  "Prepend / Append"?: "None" | "Prepend" | "Append" | "Both";
  "Icon"?: "None" | "Left";
  "Loading?"?: "False" | "True";
  "Clearable?"?: "False" | "True";
};
export function FormControlDelimited(props: FormControlDelimitedProps) { return <CatalogComponent catalogId="14787:3326" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
