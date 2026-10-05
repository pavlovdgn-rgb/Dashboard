import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Badge.module.css';
export type BadgeProps = CatalogProps & {
  "Icon right#31918:5"?: boolean;
  "⮑  Icon right#31918:6"?: string;
  "⮑ Icon left#31918:7"?: string;
  "Icon left#31918:8"?: boolean;
  "Text#31918:9"?: string;
  "⮑ Icon#31918:18"?: string;
  "Color"?: "Default" | "Hollow" | "Primary" | "Accent" | "Success" | "Danger" | "Warning";
  "Disabled"?: "False" | "True";
  "Icon only"?: "False" | "True";
};
export function Badge(props: BadgeProps) { return <CatalogComponent catalogId="31918:390303" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
