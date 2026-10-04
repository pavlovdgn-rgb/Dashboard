import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Logo.module.css';
export type LogoProps = CatalogProps & {

};
export function Logo(props: LogoProps) { return <CatalogComponent catalogId="289:13519" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
