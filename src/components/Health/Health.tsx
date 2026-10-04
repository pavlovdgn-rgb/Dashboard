import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Health.module.css';
export type HealthProps = CatalogProps & {
  "Size"?: "Medium" | "Small" | "X Small";
  "Color"?: "Custom" | "Failure" | "Healthy" | "Unknown" | "Warning" | "Active";
};
export function Health(props: HealthProps) { return <CatalogComponent catalogId="13622:59599" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
