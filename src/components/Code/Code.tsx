import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Code.module.css';
export type CodeProps = CatalogProps & {
  "Size"?: "X-Small" | "Small" | "Medium (default)";
};
export function Code(props: CodeProps) { return <CatalogComponent catalogId="15173:122940" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
