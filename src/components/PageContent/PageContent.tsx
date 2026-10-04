import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageContent.module.css';
export type PageContentProps = CatalogProps & {
  "Bottom border"?: "Extended" | "False" | "True";
  "Restrict width"?: "False" | "True";
  "Vertical alignment"?: "Center" | "Top";
  "Panelled"?: "False" | "True";
};
export function PageContent(props: PageContentProps) { return <CatalogComponent catalogId="24329:303983" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
