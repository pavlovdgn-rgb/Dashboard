import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Header.module.css';
export type HeaderProps = CatalogProps & {
  "Mobile"?: "False" | "True";
};
export function Header(props: HeaderProps) { return <CatalogComponent catalogId="26824:283060" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
