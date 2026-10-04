import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TimelineIcon.module.css';
export type TimelineIconProps = CatalogProps & {
  "Type"?: "Avatar" | "Icon" | "Photo";
  "Size"?: "Medium" | "Small";
  "Position"?: "Middle" | "Top" | "Top (no lines)";
};
export function TimelineIcon(props: TimelineIconProps) { return <CatalogComponent catalogId="26861:283314" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
