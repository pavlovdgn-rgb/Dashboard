import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './AutoRefreshButton.module.css';
export type AutoRefreshButtonProps = CatalogProps & {
  "Paused"?: "true" | "false";
  "Open"?: "false" | "true";
};
export function AutoRefreshButton(props: AutoRefreshButtonProps) { return <CatalogComponent catalogId="23938:282840" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
