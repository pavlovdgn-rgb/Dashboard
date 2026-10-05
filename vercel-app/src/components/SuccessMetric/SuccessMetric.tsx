import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SuccessMetric.module.css';
export type SuccessMetricProps = CatalogProps & {
  "FractionValue#132:0"?: string;
  "PercentValue#132:4"?: string;
  "BaseValue#132:8"?: string;
  "FractionZero#132:12"?: string;
  "PercentZero#132:16"?: string;
  "BaseZero#132:20"?: string;
  "FractionNoData#132:24"?: string;
  "PercentNoData#132:28"?: string;
  "BaseNoData#132:32"?: string;
  "Data"?: "Value" | "Zero" | "NoData";
};
export function SuccessMetric(props: SuccessMetricProps) { return <CatalogComponent catalogId="132:574" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
