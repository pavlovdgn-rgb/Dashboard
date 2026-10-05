import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FacetButton.module.css';
export type FacetButtonProps = CatalogProps & {

};
export function FacetButton(props: FacetButtonProps) { return <CatalogComponent catalogId="134:23060" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
