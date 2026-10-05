import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DescriptionListItem.module.css';
export type DescriptionListItemProps = CatalogProps & {
  "Type"?: "Stacked" | "Column" | "Inline";
  "Reverse"?: "No" | "Yes";
  "Compressed"?: "No" | "Yes";
  "Align"?: "Left" | "Center";
};
export function DescriptionListItem(props: DescriptionListItemProps) { return <CatalogComponent catalogId="14711:170" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
