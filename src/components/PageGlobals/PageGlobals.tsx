import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageGlobals.module.css';
export type PageGlobalsProps = CatalogProps & {

};
export function PageGlobals(props: PageGlobalsProps) { return <CatalogComponent catalogId="44950:72050" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
