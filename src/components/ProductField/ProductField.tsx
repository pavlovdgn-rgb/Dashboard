import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ProductField.module.css';
export type ProductFieldProps = CatalogProps & {
  "Label#203:42"?: string;
  "Help#203:63"?: string;
  "ShowHelp#203:84"?: boolean;
  "Type"?: "Text" | "Textarea" | "Select" | "Search" | "Password";
  "State"?: "Default" | "Focus" | "Invalid" | "Disabled";
};
export function ProductField(props: ProductFieldProps) { return <CatalogComponent catalogId="203:4474" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
