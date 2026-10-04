import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageTemplates.module.css';
export type PageTemplatesProps = CatalogProps & {
  "Template"?: "Default" | "Empty content" | "Empty page";
  "Restrict width"?: "False" | "True";
  "Side bar"?: "Collapsed" | "False" | "True";
  "Bottom bar"?: "False" | "True";
};
export function PageTemplates(props: PageTemplatesProps) { return <CatalogComponent catalogId="24329:308827" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
