import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Breadcrumb.module.css';
export type BreadcrumbProps = CatalogProps & {
  "Divider#42289:1"?: boolean;
  "Truncated"?: "True" | "False";
  "Interactive"?: "False" | "True";
  "Hover"?: "False" | "True";
};
export function Breadcrumb(props: BreadcrumbProps) { return <CatalogComponent catalogId="42289:81" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
