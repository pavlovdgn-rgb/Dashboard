import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CommentList.module.css';
export type CommentListProps = CatalogProps & {

};
export function CommentList(props: CommentListProps) { return <CatalogComponent catalogId="20788:288513" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
