import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ExampleContent.module.css';
export type ExampleContentProps = CatalogProps & {
  "Content"?: "1" | "2" | "3";
};
export function ExampleContent(props: ExampleContentProps) { return <CatalogComponent catalogId="36606:398160" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
