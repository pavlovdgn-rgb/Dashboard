import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FacetGroupHorizontal.module.css';
export type FacetGroupHorizontalProps = CatalogProps & {

};
export function FacetGroupHorizontal(props: FacetGroupHorizontalProps) { return <CatalogComponent catalogId="135:602" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
