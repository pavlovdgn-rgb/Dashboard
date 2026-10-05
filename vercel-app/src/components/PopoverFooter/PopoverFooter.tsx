import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PopoverFooter.module.css';
export type PopoverFooterProps = CatalogProps & {

};
export function PopoverFooter(props: PopoverFooterProps) { return <CatalogComponent catalogId="38872:21246" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
