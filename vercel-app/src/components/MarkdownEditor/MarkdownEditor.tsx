import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './MarkdownEditor.module.css';
export type MarkdownEditorProps = CatalogProps & {
  "Type"?: "Default" | "Errors" | "Attachment Error" | "Focus";
};
export function MarkdownEditor(props: MarkdownEditorProps) { return <CatalogComponent catalogId="16512:211159" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
