import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './RadioGroup.module.css';
export type RadioGroupProps = CatalogProps & {
  "State"?: "Default" | "Invalid";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
};
export function RadioGroup(props: RadioGroupProps) { return <CatalogComponent catalogId="15884:149603" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
