import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Image.module.css';
export type ImageProps = CatalogProps & {
  "Size"?: "Small (120)" | "Medium (200)" | "Large (360)" | "X Large (600)" | "Custom (resizable)";
  "hasShadow"?: "true" | "false";
};
export function Image(props: ImageProps) { return <CatalogComponent catalogId="14711:1" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
