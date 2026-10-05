import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Toast.module.css';
export type ToastProps = CatalogProps & {
  "Type"?: "Default" | "Success" | "Danger" | "Warning" | "Info";
  "Icon"?: "False" | "True";
  "Button"?: "False" | "True";
};
export function Toast(props: ToastProps) { return <CatalogComponent catalogId="13555:24644" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
