import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ProductButton.module.css';
export type ProductButtonProps = CatalogProps & {
  "Kind"?: "Primary" | "Secondary" | "Tertiary";
  "State"?: "Default" | "Hover" | "Pressed" | "Focus" | "Disabled" | "Loading";
  "Size"?: "Small";
};
export function ProductButton(props: ProductButtonProps) { return <CatalogComponent catalogId="125:450" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
