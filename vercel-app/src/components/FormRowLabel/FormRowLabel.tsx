import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormRowLabel.module.css';
export type FormRowLabelProps = CatalogProps & {
  "State"?: "Default" | "Focus" | "Invalid";
  "Append"?: "None" | "Text" | "Icon";
};
export function FormRowLabel(props: FormRowLabelProps) { return <CatalogComponent catalogId="15883:126354" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
