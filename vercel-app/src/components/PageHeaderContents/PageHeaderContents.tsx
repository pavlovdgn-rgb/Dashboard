import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageHeaderContents.module.css';
export type PageHeaderContentsProps = CatalogProps & {
  "Left content"?: "Tabs as titles" | "Title" | "Title & Tabs";
  "Right content"?: "Buttons" | "None" | "Time or Custom";
  "Description?"?: "False" | "True";
  "Breadcrumbs"?: "False" | "True";
};
export function PageHeaderContents(props: PageHeaderContentsProps) { return <CatalogComponent catalogId="24329:291092" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
