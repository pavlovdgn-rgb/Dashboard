import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DataCoverage.module.css';
export type DataCoverageProps = CatalogProps & {
  "ShowAction#86:10"?: boolean;
  "DetailTextComplete#89:0"?: string;
  "DetailTextPartial#89:4"?: string;
  "DetailTextUnavailable#89:8"?: string;
  "Coverage"?: "Complete" | "Partial" | "Unavailable";
};
export function DataCoverage(props: DataCoverageProps) { return <CatalogComponent catalogId="86:370" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
