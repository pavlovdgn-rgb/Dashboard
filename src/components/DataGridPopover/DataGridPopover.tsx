import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataGridPopover.module.css';
export type DataGridPopoverProps = CatalogProps & {
  "Content"?: "Display Options" | "Columns" | "Sorting" | "Keyboard shortcuts";
};
export function DataGridPopover(props: DataGridPopoverProps) { return <CatalogComponent catalogId="46305:10412" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
