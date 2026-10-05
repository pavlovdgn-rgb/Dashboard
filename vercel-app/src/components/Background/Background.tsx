import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Background.module.css';
export type BackgroundProps = CatalogProps & {
  "Display"?: "Plain" | "Subdued" | "Primary" | "Success" | "Warning" | "Danger" | "Accent" | "Transparent";
  "Shadow"?: "false" | "true";
  "Border"?: "false" | "true";
  "Disabled"?: "false" | "true";
};
export function Background(props: BackgroundProps) { return <CatalogComponent catalogId="36238:395223" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
