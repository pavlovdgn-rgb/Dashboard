import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextParagraph.module.css';
export type TextParagraphProps = CatalogProps & {
  "Text#32296:32"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextParagraph(props: TextParagraphProps) { return <CatalogComponent catalogId="32296:391647" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
