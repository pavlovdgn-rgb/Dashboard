import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Elastic.module.css';
export type ElasticProps = CatalogProps & {
  "Size"?: "Medium (default)" | "Large" | "X Large" | "XX Large";
};
export function Elastic(props: ElasticProps) { return <CatalogComponent catalogId="13648:4313" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
