import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Callout.module.css';
export type CalloutProps = CatalogProps & {
  "⮑ Icon#32350:7"?: boolean;
  "⮑ Icon glyph#32350:8"?: string;
  "Dismiss#45910:0"?: boolean;
  "Title#45910:18"?: boolean;
  "⮑ Children instance#45927:39"?: string;
  "Children#46750:0"?: boolean;
  "Color"?: "Success" | "Danger" | "Warning" | "Primary" | "Accent";
  "Size"?: "Medium" | "Small";
};
export function Callout(props: CalloutProps) { return <CatalogComponent catalogId="32350:392160" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
