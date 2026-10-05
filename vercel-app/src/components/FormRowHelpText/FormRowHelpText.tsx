import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormRowHelpText.module.css';
export type FormRowHelpTextProps = CatalogProps & {
  "State"?: "Default" | "Invalid";
};
export function FormRowHelpText(props: FormRowHelpTextProps) { return <CatalogComponent catalogId="15883:126375" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
