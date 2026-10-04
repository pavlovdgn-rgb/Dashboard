import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Footer.module.css';
export type FooterProps = CatalogProps & {
  "Button#36050:0"?: boolean;
  "Action#36050:4"?: boolean;
  "Align"?: "Left" | "Center" | "Right";
  "Disabled"?: "false" | "true";
};
export function Footer(props: FooterProps) { return <CatalogComponent catalogId="36238:395246" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
