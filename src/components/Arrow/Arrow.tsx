import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Arrow.module.css';
export type ArrowProps = CatalogProps & {

};
export function Arrow(props: ArrowProps) { return <CatalogComponent catalogId="36391:398493" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
