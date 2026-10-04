import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ListGroupItem.module.css';
export type ListGroupItemProps = CatalogProps & {
  "Size"?: "Medium" | "Small" | "X-Small";
  "Color"?: "Default" | "Primary" | "Subdued";
  "Icon"?: "True" | "False";
  "Extra action"?: "False" | "True";
  "State"?: "Default" | "Active" | "Hover" | "Disabled";
};
export function ListGroupItem(props: ListGroupItemProps) { return <CatalogComponent catalogId="15132:116102" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
