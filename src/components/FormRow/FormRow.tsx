import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormRow.module.css';
export type FormRowProps = CatalogProps & {
  "Column"?: "True" | "False";
};
export function FormRow(props: FormRowProps) { return <CatalogComponent catalogId="15884:208950" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
