import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilterButtonDualToggle.module.css';
export type FilterButtonDualToggleProps = CatalogProps & {
  "Compressed"?: "false" | "true";
};
export function FilterButtonDualToggle(props: FilterButtonDualToggleProps) { return <CatalogComponent catalogId="39838:185" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
