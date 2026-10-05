import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Title.module.css';
export type TitleProps = CatalogProps & {
  "Title size"?: "Small (default)" | "XSmall";
};
export function Title(props: TitleProps) { return <CatalogComponent catalogId="36238:395217" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
