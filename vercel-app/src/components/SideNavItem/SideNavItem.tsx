import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SideNavItem.module.css';
export type SideNavItemProps = CatalogProps & {
  "Nested level"?: "0" | "1" | "2" | "3";
  "Open?"?: "False" | "True";
  "Has child items?"?: "False" | "True";
  "Icon?"?: "True" | "False";
  "Active?"?: "False" | "True";
};
export function SideNavItem(props: SideNavItemProps) { return <CatalogComponent catalogId="14645:214" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
