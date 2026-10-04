import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Dot.module.css';
export type DotProps = CatalogProps & {
  "Filled"?: "true" | "false";
};
export function Dot(props: DotProps) { return <CatalogComponent catalogId="36391:398502" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
