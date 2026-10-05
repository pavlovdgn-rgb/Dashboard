import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormCompressed.module.css';
export type FormCompressedProps = CatalogProps & {
  "Invalid"?: "False" | "True";
};
export function FormCompressed(props: FormCompressedProps) { return <CatalogComponent catalogId="15884:202224" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
