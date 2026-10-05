import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ToastList.module.css';
export type ToastListProps = CatalogProps & {
  "showClearAllButtonAt"?: "false" | "true";
};
export function ToastList(props: ToastListProps) { return <CatalogComponent catalogId="39196:447" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
