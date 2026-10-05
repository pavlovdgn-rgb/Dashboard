import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Tabs.module.css';
export type TabsProps = CatalogProps & {
  "Border#32618:13"?: boolean;
  "Size"?: "Medium*" | "Small" | "Large" | "X-Large";
  "Expand"?: "False" | "True";
};
export function Tabs(props: TabsProps) { return <CatalogComponent catalogId="32618:392277" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
