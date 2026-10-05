import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControlContentLeft.module.css';
export type FormControlContentLeftProps = CatalogProps & {
  "Prepend"?: "True" | "False";
  "Icon"?: "True" | "False";
  "State"?: "Filled" | "Placeholder" | "Disabled";
  "Compressed"?: "False" | "True";
};
export function FormControlContentLeft(props: FormControlContentLeftProps) { return <CatalogComponent catalogId="13610:44523" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
