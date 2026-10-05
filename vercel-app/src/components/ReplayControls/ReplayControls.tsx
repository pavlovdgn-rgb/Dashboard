import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ReplayControls.module.css';
export type ReplayControlsProps = CatalogProps & {
  "PositionLabel#84:2"?: string;
  "Coverage"?: "Complete" | "Gap";
  "Playback"?: "Paused" | "Playing";
};
export function ReplayControls(props: ReplayControlsProps) { return <CatalogComponent catalogId="84:713" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
