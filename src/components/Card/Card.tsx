import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Card.module.css';
export type CardProps = CatalogProps & {
  "Badge#36039:12"?: boolean;
  "Footer#36039:15"?: boolean;
  "Selectable#36039:18"?: boolean;
  "Icon#36039:29"?: boolean;
  "Description#36039:37"?: boolean;
  "Title#36081:0"?: boolean;
  "Layout"?: "Vertical" | "Horizontal";
  "Image"?: "false" | "true";
  "Text Align"?: "Left" | "Center" | "Right";
  "Disabled"?: "false" | "true";
  "Checkable"?: "NA" | "Radio" | "Checkbox";
  "Checked"?: "false" | "true";
};
export function Card(props: CardProps) { return <CatalogComponent catalogId="36238:395271" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
