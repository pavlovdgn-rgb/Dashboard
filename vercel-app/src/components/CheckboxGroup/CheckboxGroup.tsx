import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CheckboxGroup.module.css';
export type CheckboxGroupProps = CatalogProps & {
  "State"?: "Default" | "Invalid";
  "Compressed"?: "False" | "True";
  "Column display"?: "False" | "True";
  "Label"?: "True" | "False";
};
export function CheckboxGroup(props: CheckboxGroupProps) { return <CatalogComponent catalogId="15884:145646" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
