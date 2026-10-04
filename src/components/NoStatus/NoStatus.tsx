import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './NoStatus.module.css';
export type NoStatusProps = CatalogProps & {
  "Last step#44191:73"?: boolean;
  "Children#44199:139"?: string;
  "titleSize"?: "Medium" | "Small" | "XSmall" | "XXSmall";
};
export function NoStatus(props: NoStatusProps) { return <CatalogComponent catalogId="44287:2331" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
