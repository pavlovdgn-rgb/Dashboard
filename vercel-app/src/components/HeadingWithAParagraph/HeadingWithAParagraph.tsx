import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HeadingWithAParagraph.module.css';
export type HeadingWithAParagraphProps = CatalogProps & {
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function HeadingWithAParagraph(props: HeadingWithAParagraphProps) { return <CatalogComponent catalogId="32350:391695" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
