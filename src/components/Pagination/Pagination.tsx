import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Pagination.module.css';
export type PaginationProps = CatalogProps & {
  "Type"?: "Few" | "Many" | "Many in between" | "Mobile / Indeterminate" | "Compressed" | "Many is last";
};
export function Pagination(props: PaginationProps) { return <CatalogComponent catalogId="14939:107721" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
