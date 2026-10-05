import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HeaderBreadcrumb.module.css';
export type HeaderBreadcrumbProps = CatalogProps & {
  "Position"?: "First & Only" | "First" | "Middle" | "Last";
  "Linked"?: "False" | "True";
  "Collapsed"?: "False" | "True";
};
export function HeaderBreadcrumb(props: HeaderBreadcrumbProps) { return <CatalogComponent catalogId="15079:109018" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
