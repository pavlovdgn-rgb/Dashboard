import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Timeline.module.css';
export type TimelineProps = CatalogProps & {
  "verticalAlign"?: "Center" | "Top";
  "Children"?: "Markdown Editor" | "Panel transparent" | "Panel with color" | "Split Panel";
};
export function Timeline(props: TimelineProps) { return <CatalogComponent catalogId="26861:286195" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
