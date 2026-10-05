import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './AutoRefresh.module.css';
export type AutoRefreshProps = CatalogProps & {
  "Paused"?: "true" | "false";
  "Open"?: "false" | "true";
};
export function AutoRefresh(props: AutoRefreshProps) { return <CatalogComponent catalogId="23938:281323" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
