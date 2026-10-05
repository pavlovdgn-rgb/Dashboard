import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormBasic.module.css';
export type FormBasicProps = CatalogProps & {
  "Invalid"?: "False" | "True";
};
export function FormBasic(props: FormBasicProps) { return <CatalogComponent catalogId="15884:200789" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
