import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Tab.module.css';
export type TabProps = CatalogProps & {
  "Append#32617:4"?: boolean;
  "⮑ Prepend#32617:5"?: string;
  "Prepend#32617:6"?: boolean;
  "⮑ Append#32617:7"?: string;
  "Text#32618:0"?: string;
  "Selected"?: "False" | "True";
  "Disabled"?: "False" | "True";
  "Size"?: "Small" | "Large" | "X-Large" | "Medium*";
};
export function Tab(props: TabProps) { return <CatalogComponent catalogId="32617:392183" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
