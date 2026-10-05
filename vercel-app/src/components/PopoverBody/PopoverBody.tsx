import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PopoverBody.module.css';
export type PopoverBodyProps = CatalogProps & {

};
export function PopoverBody(props: PopoverBodyProps) { return <CatalogComponent catalogId="38872:21244" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
