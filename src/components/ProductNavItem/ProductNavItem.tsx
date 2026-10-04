import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ProductNavItem.module.css';
export type ProductNavItemProps = CatalogProps & {
  "Selected"?: "False" | "True";
  "State"?: "Default" | "Hover" | "Pressed" | "Focus";
};
export function ProductNavItem(props: ProductNavItemProps) { return <CatalogComponent catalogId="128:563" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
