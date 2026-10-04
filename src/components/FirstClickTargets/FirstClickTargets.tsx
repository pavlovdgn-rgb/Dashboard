import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FirstClickTargets.module.css';
export type FirstClickTargetsProps = CatalogProps & {
  "State"?: "Ready" | "Loading" | "Empty" | "FilteredEmpty" | "Error";
};
export function FirstClickTargets(props: FirstClickTargetsProps) { return <CatalogComponent catalogId="135:778" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
