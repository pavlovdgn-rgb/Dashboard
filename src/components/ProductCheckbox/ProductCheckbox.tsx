import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ProductCheckbox.module.css';
export type ProductCheckboxProps = CatalogProps & {
  "Label#282:0"?: string;
  "Value"?: "Off" | "On" | "Mixed";
  "State"?: "Default" | "Hover" | "Focus" | "Disabled";
};
export function ProductCheckbox(props: ProductCheckboxProps) { return <CatalogComponent catalogId="282:2918" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
