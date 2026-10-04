import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PaginationButton.module.css';
export type PaginationButtonProps = CatalogProps & {
  "State"?: "Active" | "Default" | "Disabled" | "Ellipsis";
};
export function PaginationButton(props: PaginationButtonProps) { return <CatalogComponent catalogId="14939:107463" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
