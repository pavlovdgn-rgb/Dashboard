import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TableCellFooter.module.css';
export type TableCellFooterProps = CatalogProps & {
  "Compressed"?: "False" | "True";
};
export function TableCellFooter(props: TableCellFooterProps) { return <CatalogComponent catalogId="15129:1692" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
