import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './StepIndicator.module.css';
export type StepIndicatorProps = CatalogProps & {
  "Status"?: "default" | "complete" | "incomplete" | "disabled" | "loading" | "warning" | "danger" | "current";
  "Size"?: "Small/Medium" | "XSmall" | "XXSmall";
};
export function StepIndicator(props: StepIndicatorProps) { return <CatalogComponent catalogId="14775:90261" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
