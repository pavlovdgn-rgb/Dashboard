import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './LayoutThumbnail.module.css';
export type LayoutThumbnailProps = CatalogProps & {
  "Type"?: "Sidebar" | "Empty" | "Multiple";
  "State"?: "Default" | "Selected";
};
export function LayoutThumbnail(props: LayoutThumbnailProps) { return <CatalogComponent catalogId="22907:283773" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
