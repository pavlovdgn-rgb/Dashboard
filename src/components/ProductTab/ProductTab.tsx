import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ProductTab.module.css';
export type ProductTabProps = CatalogProps & {
  "Selected"?: "False" | "True";
  "State"?: "Default" | "Hover" | "Pressed" | "Focus";
  "Size"?: "Small";
};
export function ProductTab(props: ProductTabProps) { return <CatalogComponent catalogId="128:1055" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
