import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Popover.module.css';
export type PopoverProps = CatalogProps & {
  "Header#38265:0"?: boolean;
  "Footer#38265:5"?: boolean;
  "Arrow"?: "12:00 ↑" | "3:00 →" | "6:00 ↓" | "9:00 ←";
};
export function Popover(props: PopoverProps) { return <CatalogComponent catalogId="38872:21191" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
