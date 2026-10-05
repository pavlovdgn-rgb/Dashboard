import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextHeading.module.css';
export type TextHeadingProps = CatalogProps & {
  "Text#32296:1"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
  "Level"?: "Heading 1" | "Heading 2" | "Heading 3" | "Heading 4" | "Heading 5" | "Heading 6";
};
export function TextHeading(props: TextHeadingProps) { return <CatalogComponent catalogId="32296:391640" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
