import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Panel.module.css';
export type PanelProps = CatalogProps & {
  "Content#32642:5"?: string;
  "Padding size"?: "None" | "Small" | "Medium*" | "Large";
  "Color"?: "Plain*" | "Subdued" | "Primary" | "Success" | "Warning" | "Danger" | "Accent" | "Transparent";
  "Shadow"?: "True" | "False";
  "Border"?: "False" | "True";
  "Border radius"?: "True" | "False";
};
export function Panel(props: PanelProps) { return <CatalogComponent catalogId="32642:391756" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
