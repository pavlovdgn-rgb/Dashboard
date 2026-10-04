import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Modal.module.css';
export type ModalProps = CatalogProps & {

};
export function Modal(props: ModalProps) { return <CatalogComponent catalogId="32634:391703" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
