import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SideNavNestedIndicator.module.css';
export type SideNavNestedIndicatorProps = CatalogProps & {
  "Show"?: "True" | "False";
  "Is child?"?: "True" | "False";
  "Is last?"?: "True" | "False";
};
export function SideNavNestedIndicator(props: SideNavNestedIndicatorProps) { return <CatalogComponent catalogId="14643:2" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
