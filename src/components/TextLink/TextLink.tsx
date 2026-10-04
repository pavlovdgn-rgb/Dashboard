import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextLink.module.css';
export type TextLinkProps = CatalogProps & {
  "External URL#32177:6"?: boolean;
  "Text#32177:7"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextLink(props: TextLinkProps) { return <CatalogComponent catalogId="32177:399780" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
