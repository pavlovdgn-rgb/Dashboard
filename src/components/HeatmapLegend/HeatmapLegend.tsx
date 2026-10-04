import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HeatmapLegend.module.css';
export type HeatmapLegendProps = CatalogProps & {
  "SampleBase#83:4"?: string;
  "DefinitionNote#83:5"?: string;
  "Mode"?: "AllClicks" | "FirstClick";
};
export function HeatmapLegend(props: HeatmapLegendProps) { return <CatalogComponent catalogId="83:730" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
