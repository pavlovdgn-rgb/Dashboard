import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PasswordField.module.css';
export type PasswordFieldProps = CatalogProps & {
  "State"?: "Filled" | "Focus" | "Invalid" | "Disabled";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
  "Help text"?: "True" | "False";
};
export function PasswordField(props: PasswordFieldProps) { return <CatalogComponent catalogId="15883:143147" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
