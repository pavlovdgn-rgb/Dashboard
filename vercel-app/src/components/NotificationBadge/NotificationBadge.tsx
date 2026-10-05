import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './NotificationBadge.module.css';
export type NotificationBadgeProps = CatalogProps & {
  "Count#31998:26"?: string;
  "Color"?: "Subdued" | "Accent" | "Success";
  "Size"?: "Medium" | "Small";
};
export function NotificationBadge(props: NotificationBadgeProps) { return <CatalogComponent catalogId="13546:25393" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
