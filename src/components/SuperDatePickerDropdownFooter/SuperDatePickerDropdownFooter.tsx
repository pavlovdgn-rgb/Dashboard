import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SuperDatePickerDropdownFooter.module.css';
export type SuperDatePickerDropdownFooterProps = CatalogProps & {
  "Disabled"?: "True" | "False";
};
export function SuperDatePickerDropdownFooter(props: SuperDatePickerDropdownFooterProps) { return <CatalogComponent catalogId="20307:328531" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
