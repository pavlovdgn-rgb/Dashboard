import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FirstClickTargetRow.module.css';
export type FirstClickTargetRowProps = CatalogProps & {
  "TargetIcon#132:36"?: string;
  "Title#132:43"?: string;
  "Description#132:50"?: string;
  "Count#132:57"?: string;
  "Share#132:64"?: string;
  "Selected"?: "False" | "True";
  "State"?: "Default" | "Hover" | "Focus";
};
export function FirstClickTargetRow(props: FirstClickTargetRowProps) { return <CatalogComponent catalogId="132:634" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
