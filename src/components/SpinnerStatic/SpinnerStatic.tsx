import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SpinnerStatic.module.css';
export type SpinnerStaticProps = CatalogProps & {
  "Size"?: "XX-Large" | "X-Large" | "Large" | "Medium*" | "Small";
};
export function SpinnerStatic(props: SpinnerStaticProps) { return <CatalogComponent catalogId="13648:4315" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
