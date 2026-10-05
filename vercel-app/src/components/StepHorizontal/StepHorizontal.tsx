import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './StepHorizontal.module.css';
export type StepHorizontalProps = CatalogProps & {
  "Size"?: "Medium" | "Small" | "XSmall";
  "Position"?: "First" | "Last" | "Middle";
  "Status"?: "default" | "incomplete" | "disabled" | "loading" | "warning" | "danger" | "complete" | "current";
};
export function StepHorizontal(props: StepHorizontalProps) { return <CatalogComponent catalogId="14775:90378" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
