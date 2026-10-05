import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextBlockquote.module.css';
export type TextBlockquoteProps = CatalogProps & {
  "Text#32296:54"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextBlockquote(props: TextBlockquoteProps) { return <CatalogComponent catalogId="32296:392036" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
