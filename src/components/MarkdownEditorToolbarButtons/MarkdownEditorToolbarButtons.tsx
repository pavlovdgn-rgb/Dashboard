import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './MarkdownEditorToolbarButtons.module.css';
export type MarkdownEditorToolbarButtonsProps = CatalogProps & {

};
export function MarkdownEditorToolbarButtons(props: MarkdownEditorToolbarButtonsProps) { return <CatalogComponent catalogId="16961:248689" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
