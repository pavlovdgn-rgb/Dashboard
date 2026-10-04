import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SuperDatePickerButton.module.css';
export type SuperDatePickerButtonProps = CatalogProps & {
  "State"?: "Default" | "Active / Open" | "Needs updating" | "Auto refresh";
};
export function SuperDatePickerButton(props: SuperDatePickerButtonProps) { return <CatalogComponent catalogId="14795:111805" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
