import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilterGroup.module.css';
export type FilterGroupProps = CatalogProps & {
  "Compressed"?: "false" | "true";
};
export function FilterGroup(props: FilterGroupProps) { return <CatalogComponent catalogId="39838:166" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
