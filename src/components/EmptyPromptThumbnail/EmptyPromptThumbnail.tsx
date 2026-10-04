import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './EmptyPromptThumbnail.module.css';
export type EmptyPromptThumbnailProps = CatalogProps & {
  "Type"?: "Primary" | "Secondary";
};
export function EmptyPromptThumbnail(props: EmptyPromptThumbnailProps) { return <CatalogComponent catalogId="23023:279440" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
