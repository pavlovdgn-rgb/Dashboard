import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageSidebar.module.css';
export type PageSidebarProps = CatalogProps & {
  "State"?: "Default" | "Collapsed";
};
export function PageSidebar(props: PageSidebarProps) { return <CatalogComponent catalogId="20156:274200" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
