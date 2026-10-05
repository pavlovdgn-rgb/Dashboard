import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilterButtonSingleToggle.module.css';
export type FilterButtonSingleToggleProps = CatalogProps & {
  "Compressed"?: "false" | "true";
};
export function FilterButtonSingleToggle(props: FilterButtonSingleToggleProps) { return <CatalogComponent catalogId="39838:192" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
