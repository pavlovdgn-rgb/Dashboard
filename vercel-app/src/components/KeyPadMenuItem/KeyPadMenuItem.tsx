import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './KeyPadMenuItem.module.css';
export type KeyPadMenuItemProps = CatalogProps & {
  "State"?: "Default" | "Hover";
  "Disabled"?: "True" | "False";
  "Active"?: "True" | "False";
  "Beta badge"?: "Text" | "Icon" | "None";
  "Checkable"?: "None" | "Single" | "Multi";
};
export function KeyPadMenuItem(props: KeyPadMenuItemProps) { return <CatalogComponent catalogId="13546:25989" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
