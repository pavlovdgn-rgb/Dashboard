import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ListGroup.module.css';
export type ListGroupProps = CatalogProps & {

};
export function ListGroup(props: ListGroupProps) { return <CatalogComponent catalogId="15132:132472" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
