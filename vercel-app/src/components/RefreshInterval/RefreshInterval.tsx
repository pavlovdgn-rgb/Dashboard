import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './RefreshInterval.module.css';
export type RefreshIntervalProps = CatalogProps & {
  "On"?: "True" | "False";
  "In popover"?: "False" | "True";
};
export function RefreshInterval(props: RefreshIntervalProps) { return <CatalogComponent catalogId="22632:275537" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
