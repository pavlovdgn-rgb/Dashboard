import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HeaderDark.module.css';
export type HeaderDarkProps = CatalogProps & {
  "Show setup guides#47104:0"?: boolean;
  "Show feedback#47104:3"?: boolean;
  "Show AI Assistant#47104:6"?: boolean;
  "Mobile"?: "False" | "True";
};
export function HeaderDark(props: HeaderDarkProps) { return <CatalogComponent catalogId="26824:282882" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
