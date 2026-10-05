import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CommentTimelineIcon.module.css';
export type CommentTimelineIconProps = CatalogProps & {
  "Type"?: "Avatar" | "Collapsed";
  "Size"?: "Medium" | "Small";
  "Position"?: "Last" | "Center" | "Top";
};
export function CommentTimelineIcon(props: CommentTimelineIconProps) { return <CatalogComponent catalogId="20788:280591" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
