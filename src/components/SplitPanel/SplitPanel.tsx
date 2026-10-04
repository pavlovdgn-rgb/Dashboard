import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SplitPanel.module.css';
export type SplitPanelProps = CatalogProps & {
  "Direction"?: "Vertical" | "Horizontal" | "Direction3";
  "Border"?: "False" | "True";
  "Shadow"?: "True" | "False";
  "Border radius"?: "True" | "False";
};
export function SplitPanel(props: SplitPanelProps) { return <CatalogComponent catalogId="32670:392917" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
