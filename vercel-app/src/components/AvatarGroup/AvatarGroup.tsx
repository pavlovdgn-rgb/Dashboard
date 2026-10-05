import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './AvatarGroup.module.css';
export type AvatarGroupProps = CatalogProps & {
  "Size"?: "Large" | "Medium" | "Small" | "X-Large";
};
export function AvatarGroup(props: AvatarGroupProps) { return <CatalogComponent catalogId="26768:281544" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
