import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './RadioButton.module.css';
export type RadioButtonProps = CatalogProps & {
  "Checked"?: "True" | "False";
  "Disabled"?: "False" | "True";
  "Focus"?: "False" | "True";
  "Size"?: "Medium" | "Small";
};
export function RadioButton(props: RadioButtonProps) { return <CatalogComponent catalogId="16033:196057" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
