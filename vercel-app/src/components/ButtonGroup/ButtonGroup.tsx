import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ButtonGroup.module.css';
export type ButtonGroupProps = CatalogProps & {
  "Size"?: "Medium" | "Small*" | "Compressed";
  "Full width"?: "False" | "True";
  "Color"?: "Primary" | "Neutral*";
  "Disabled"?: "False" | "True";
  "Icon only"?: "False" | "True";
};
export function ButtonGroup(props: ButtonGroupProps) { return <CatalogComponent catalogId="31735:392753" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
