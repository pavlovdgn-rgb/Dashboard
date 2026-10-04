import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Chart.module.css';
export type ChartProps = CatalogProps & {
  "Color"?: "True" | "False";
  "Size"?: "Medium (default)" | "Large" | "X Large";
};
export function Chart(props: ChartProps) { return <CatalogComponent catalogId="13648:4291" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
