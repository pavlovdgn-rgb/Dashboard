import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './RecordingCoverage.module.css';
export type RecordingCoverageProps = CatalogProps & {
  "Status"?: "Complete" | "Partial" | "Unavailable";
};
export function RecordingCoverage(props: RecordingCoverageProps) { return <CatalogComponent catalogId="152:964" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
