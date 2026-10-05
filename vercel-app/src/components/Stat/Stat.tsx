import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Stat.module.css';
export type StatProps = CatalogProps & {
  "Size"?: "Large" | "Small" | "X-Small";
  "Color"?: "Text (Defualt)" | "Primary" | "Secondary" | "Warning" | "Danger" | "Accent";
  "Align"?: "Left" | "Center" | "Right";
  "Reverse"?: "True" | "False";
  "Loading"?: "False" | "True";
};
export function Stat(props: StatProps) { return <CatalogComponent catalogId="14638:71133" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
