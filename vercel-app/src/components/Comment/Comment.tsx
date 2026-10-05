import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Comment.module.css';
export type CommentProps = CatalogProps & {
  "Type"?: "Update" | "Collapsed" | "Regular";
  "Color"?: "Primary" | "Plain";
};
export function Comment(props: CommentProps) { return <CatalogComponent catalogId="20788:280525" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
