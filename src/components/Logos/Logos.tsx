import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Logos.module.css';
export type LogosProps = CatalogProps & {
  "Size"?: "Medium (default)" | "Large" | "X Large";
};
export function Logos(props: LogosProps) { return <CatalogComponent catalogId="13648:4314" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
