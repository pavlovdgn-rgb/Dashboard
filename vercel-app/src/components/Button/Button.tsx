import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Button.module.css';
export type ButtonProps = CatalogProps & {
  "Icon left#30956:3"?: boolean;
  "Text#30956:4"?: string;
  "Icon right#30956:5"?: boolean;
  "⮑  Icon left#30964:4"?: string;
  "Loading text#30997:0"?: string;
  "⮑  Icon right#31056:0"?: string;
  "⮑  Icon#31150:0"?: string;
  "Left spinner#31616:0"?: boolean;
  "Right spinner#31616:157"?: boolean;
  "Style"?: "Default*" | "Filled" | "Empty";
  "Color"?: "Primary*" | "Neutral" | "Success" | "Warning" | "Danger" | "Accent";
  "Size"?: "Medium*" | "Small" | "Extra Small";
  "Disabled"?: "False" | "True";
  "Loading"?: "False" | "True";
  "Icon only"?: "True" | "False";
};
export function Button(props: ButtonProps) { return <CatalogComponent catalogId="31735:391399" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
