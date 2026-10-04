import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Radio.module.css';
export type RadioProps = CatalogProps & {
  "Label"?: "True" | "False";
  "Checked"?: "True" | "False";
  "State"?: "Default" | "Disabled" | "Focus";
};
export function Radio(props: RadioProps) { return <CatalogComponent catalogId="13581:25220" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
