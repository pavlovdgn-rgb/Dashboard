import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SearchBar.module.css';
export type SearchBarProps = CatalogProps & {

};
export function SearchBar(props: SearchBarProps) { return <CatalogComponent catalogId="15138:3267" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
