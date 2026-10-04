import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Avatar.module.css';
export type AvatarProps = CatalogProps & {
  "Type"?: "User" | "Spaces";
  "Content"?: "Initials" | "Image" | "Icon";
  "Size"?: "Small - 24px" | "Medium - 32px (default)" | "Large - 40px" | "X-Large - 64px";
};
export function Avatar(props: AvatarProps) { return <CatalogComponent catalogId="14755:585" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
