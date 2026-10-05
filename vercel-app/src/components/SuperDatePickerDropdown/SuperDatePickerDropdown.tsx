import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SuperDatePickerDropdown.module.css';
export type SuperDatePickerDropdownProps = CatalogProps & {
  "Tab select"?: "Calendar" | "Quick select";
};
export function SuperDatePickerDropdown(props: SuperDatePickerDropdownProps) { return <CatalogComponent catalogId="14792:135915" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
