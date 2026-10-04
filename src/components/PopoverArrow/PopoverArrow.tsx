import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PopoverArrow.module.css';
export type PopoverArrowProps = CatalogProps & {

};
export function PopoverArrow(props: PopoverArrowProps) { return <CatalogComponent catalogId="38872:21248" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
