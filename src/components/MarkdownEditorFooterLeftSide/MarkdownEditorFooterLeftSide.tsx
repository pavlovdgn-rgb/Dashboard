import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './MarkdownEditorFooterLeftSide.module.css';
export type MarkdownEditorFooterLeftSideProps = CatalogProps & {
  "Type"?: "Attachment error" | "Errors" | "Attachment";
};
export function MarkdownEditorFooterLeftSide(props: MarkdownEditorFooterLeftSideProps) { return <CatalogComponent catalogId="16512:210927" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
