import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Switch.module.css';
export type SwitchProps = CatalogProps & {
  "Show Label#37824:3"?: boolean;
  "Label#37824:4"?: string;
  "Checked"?: "True" | "False";
  "Compressed"?: "True" | "False";
  "Disabled"?: "False" | "True";
};
export function Switch(props: SwitchProps) { return <CatalogComponent catalogId="37824:396069" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
