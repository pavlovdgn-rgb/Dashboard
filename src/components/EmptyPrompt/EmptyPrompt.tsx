import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './EmptyPrompt.module.css';
export type EmptyPromptProps = CatalogProps & {
  "Show Footer#36674:0"?: boolean;
  "Color"?: "Transparent" | "Plain" | "Plain + Border" | "Plain + Shadow" | "Subdued" | "Primary" | "Success" | "Warning" | "Danger" | "Accent";
  "Layout"?: "Vertical" | "Horizontal";
};
export function EmptyPrompt(props: EmptyPromptProps) { return <CatalogComponent catalogId="36674:394711" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
