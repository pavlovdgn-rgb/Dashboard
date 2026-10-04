import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TimelineTopAligned.module.css';
export type TimelineTopAlignedProps = CatalogProps & {

};
export function TimelineTopAligned(props: TimelineTopAlignedProps) { return <CatalogComponent catalogId="26861:285156" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
