import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Status.module.css';
export type StatusProps = CatalogProps & {
  "Last step#44191:73"?: boolean;
  "Children#44199:139"?: string;
  "titleSize"?: "Medium" | "Small" | "XSmall" | "XXSmall";
  "status"?: "complete" | "incomplete" | "disabled" | "loading" | "warning" | "danger" | "current";
};
export function Status(props: StatusProps) { return <CatalogComponent catalogId="44287:2876" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
