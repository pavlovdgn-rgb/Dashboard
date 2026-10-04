import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ScenarioRow.module.css';
export type ScenarioRowProps = CatalogProps & {
  "Title#135:0"?: string;
  "Description#135:7"?: string;
  "Started#135:14"?: string;
  "Completed#135:21"?: string;
  "Incomplete#135:28"?: string;
  "Selected"?: "False" | "True";
  "State"?: "Default" | "Hover" | "Focus";
};
export function ScenarioRow(props: ScenarioRowProps) { return <CatalogComponent catalogId="135:1062" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
