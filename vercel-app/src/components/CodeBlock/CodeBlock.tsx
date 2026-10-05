import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CodeBlock.module.css';
export type CodeBlockProps = CatalogProps & {
  "↳ overflowHeight#41035:6"?: boolean;
  "↳ isCopiable#41035:7"?: boolean;
  "lineNumbers#41035:8"?: boolean;
  "transparentBackground#41581:0"?: boolean;
  "scrollbar#41581:3"?: boolean;
  "Controls"?: "True" | "False";
};
export function CodeBlock(props: CodeBlockProps) { return <CatalogComponent catalogId="41035:20638" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
