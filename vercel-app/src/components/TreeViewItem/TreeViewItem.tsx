import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TreeViewItem.module.css';
export type TreeViewItemProps = CatalogProps & {
  "Open?"?: "False" | "True";
  "Icon?"?: "True" | "False";
  "Arrow?"?: "True" | "False";
  "State"?: "Default" | "Focus";
  "Compressed?"?: "False" | "True";
};
export function TreeViewItem(props: TreeViewItemProps) { return <CatalogComponent catalogId="14652:151" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
