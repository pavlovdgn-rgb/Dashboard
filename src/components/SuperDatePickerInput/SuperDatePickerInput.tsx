import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SuperDatePickerInput.module.css';
export type SuperDatePickerInputProps = CatalogProps & {
  "Needs update"?: "False" | "True";
  "Time"?: "Absolute" | "Relative";
  "Show update button"?: "True" | "Icon only" | "False";
  "Auto refresh"?: "On" | "Off";
};
export function SuperDatePickerInput(props: SuperDatePickerInputProps) { return <CatalogComponent catalogId="22805:277057" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
