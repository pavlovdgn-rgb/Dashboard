import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Flyout.module.css';
export type FlyoutProps = CatalogProps & {
  "Footer#32618:19"?: boolean;
  "Close Icon#32618:20"?: boolean;
  "Callout#32618:21"?: boolean;
  "Primary Button#32618:22"?: boolean;
  "Secondary Button#32618:27"?: boolean;
  "Description#32624:0"?: boolean;
  "Close Button#32644:10"?: boolean;
  "Type"?: "Overlay" | "Push";
  "Tabs"?: "False" | "True";
};
export function Flyout(props: FlyoutProps) { return <CatalogComponent catalogId="32618:396153" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
