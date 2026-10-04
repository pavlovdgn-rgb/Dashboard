import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './BottomBar.module.css';
export type BottomBarProps = CatalogProps & {

};
export function BottomBar(props: BottomBarProps) { return <CatalogComponent catalogId="44964:58721" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
