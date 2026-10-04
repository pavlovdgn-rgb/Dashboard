import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageHeader.module.css';
export type PageHeaderProps = CatalogProps & {
  "Bottom border"?: "Extended" | "False" | "True";
  "Restrict width"?: "False" | "True";
};
export function PageHeader(props: PageHeaderProps) { return <CatalogComponent catalogId="24329:283356" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
