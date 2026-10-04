import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControlBackground.module.css';
export type FormControlBackgroundProps = CatalogProps & {
  "Resizable#44601:0"?: boolean;
  "State"?: "Disabled" | "Focus" | "Invalid" | "Normal" | "Read-Only";
};
export function FormControlBackground(props: FormControlBackgroundProps) { return <CatalogComponent catalogId="13581:24745" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
