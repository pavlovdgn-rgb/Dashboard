import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './BetaBadge.module.css';
export type BetaBadgeProps = CatalogProps & {
  "⮑ Icon#31998:0"?: string;
  "Text#31998:13"?: string;
  "Size"?: "Small" | "Medium*";
  "Color"?: "Hollow*" | "Accent" | "Subdued";
  "Icon only"?: "False" | "True";
};
export function BetaBadge(props: BetaBadgeProps) { return <CatalogComponent catalogId="31998:390412" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
