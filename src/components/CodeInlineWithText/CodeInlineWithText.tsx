import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CodeInlineWithText.module.css';
export type CodeInlineWithTextProps = CatalogProps & {
  "Size"?: "X-Small" | "Medium" | "Small";
};
export function CodeInlineWithText(props: CodeInlineWithTextProps) { return <CatalogComponent catalogId="15996:5" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
