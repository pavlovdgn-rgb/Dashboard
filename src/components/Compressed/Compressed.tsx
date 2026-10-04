import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Compressed.module.css';
export type CompressedProps = CatalogProps & {
  "Checked"?: "True" | "False";
  "Disabled"?: "True" | "False";
};
export function Compressed(props: CompressedProps) { return <CatalogComponent catalogId="37824:396026" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
