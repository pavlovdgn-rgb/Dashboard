import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FilePickerLargeInput.module.css';
export type FilePickerLargeInputProps = CatalogProps & {
  "State"?: "Disabled" | "Placeholder" | "Focus" | "Invalid" | "Filled";
};
export function FilePickerLargeInput(props: FilePickerLargeInputProps) { return <CatalogComponent catalogId="44632:22134" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
