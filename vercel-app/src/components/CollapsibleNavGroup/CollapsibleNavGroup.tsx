import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CollapsibleNavGroup.module.css';
export type CollapsibleNavGroupProps = CatalogProps & {
  "Background"?: "None" | "Light" | "Dark";
  "Collapsed"?: "Yes" | "No";
};
export function CollapsibleNavGroup(props: CollapsibleNavGroupProps) { return <CatalogComponent catalogId="20785:279182" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
