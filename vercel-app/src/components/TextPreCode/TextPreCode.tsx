import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextPreCode.module.css';
export type TextPreCodeProps = CatalogProps & {
  "Text#31503:59"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextPreCode(props: TextPreCodeProps) { return <CatalogComponent catalogId="32296:392060" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
