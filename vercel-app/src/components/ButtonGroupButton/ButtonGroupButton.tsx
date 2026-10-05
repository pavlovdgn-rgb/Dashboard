import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ButtonGroupButton.module.css';
export type ButtonGroupButtonProps = CatalogProps & {
  "Icon left#31434:0"?: boolean;
  "Icon right#31434:3"?: boolean;
  "⮑ Icon#31434:6"?: string;
  "⮑ Icon left#31434:19"?: string;
  "⮑ Icon right#31434:32"?: string;
  "Text#31451:0"?: string;
  "Selected"?: "True" | "False";
  "Color"?: "Primary" | "Neutral*";
  "Compressed"?: "False" | "True";
  "Disabled"?: "True" | "False";
  "Icon only"?: "True" | "False";
};
export function ButtonGroupButton(props: ButtonGroupButtonProps) { return <CatalogComponent catalogId="31735:392943" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
