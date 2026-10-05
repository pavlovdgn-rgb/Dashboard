import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Tooltip.module.css';
export type TooltipProps = CatalogProps & {
  "Title#32039:17"?: boolean;
  "Description#32039:18"?: string;
  "⮑ Title#32039:19"?: string;
  "Direction"?: "12:00 ↑" | "11:00" | "10:00" | "8:00" | "7:00" | "6:00 ↓" | "5:00" | "4:00" | "3:00 →" | "2:00" | "1::00" | "9:00 ←";
};
export function Tooltip(props: TooltipProps) { return <CatalogComponent catalogId="32039:390707" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
