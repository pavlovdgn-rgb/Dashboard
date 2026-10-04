import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CommentBase.module.css';
export type CommentBaseProps = CatalogProps & {

};
export function CommentBase(props: CommentBaseProps) { return <CatalogComponent catalogId="20788:283520" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
