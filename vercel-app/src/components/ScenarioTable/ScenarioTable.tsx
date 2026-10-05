import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ScenarioTable.module.css';
export type ScenarioTableProps = CatalogProps & {
  "State"?: "Ready" | "Loading" | "Empty" | "FilteredEmpty" | "Error" | "OverviewUnselected" | "OverviewSelected";
};
export function ScenarioTable(props: ScenarioTableProps) { return <CatalogComponent catalogId="136:715" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
