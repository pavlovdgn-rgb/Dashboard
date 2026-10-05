import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SummaryMetric.module.css';
export type SummaryMetricProps = CatalogProps & {
  "Label#171:0"?: string;
  "Value#171:4"?: string;
  "Hint#171:8"?: string;
  "ShowLink#171:12"?: boolean;
  "Detail#202:0"?: string;
  "Badge#202:4"?: string;
  "ShowBadge#202:8"?: boolean;
  "ShowProgress#202:12"?: boolean;
  "State"?: "Ready" | "Loading" | "NoData";
};
export function SummaryMetric(props: SummaryMetricProps) { return <CatalogComponent catalogId="171:1801" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
