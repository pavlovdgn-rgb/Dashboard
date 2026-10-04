import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Dots.module.css';
export type DotsProps = CatalogProps & {
  "1st step#36441:18"?: boolean;
  "2nd step#36441:24"?: boolean;
  "3rd step#36441:30"?: boolean;
  "4th step#36441:36"?: boolean;
  "5th step#36441:42"?: boolean;
  "Active step"?: "1" | "2" | "3" | "4" | "5";
};
export function Dots(props: DotsProps) { return <CatalogComponent catalogId="36391:398507" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
