import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControlContentRight.module.css';
export type FormControlContentRightProps = CatalogProps & {
  "Append"?: "True" | "False";
  "Clearable"?: "True" | "False";
  "Loading"?: "True" | "False";
  "Icon"?: "True" | "False";
  "State"?: "Default" | "Disabled" | "Invalid";
  "Compressed"?: "True" | "False";
  "Number"?: "False" | "True";
};
export function FormControlContentRight(props: FormControlContentRightProps) { return <CatalogComponent catalogId="13610:44963" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
