import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Steps.module.css';
export type StepsProps = CatalogProps & {
  "titleSize"?: "Medium" | "Small" | "XSmall" | "XXSmall";
  "Status"?: "False" | "True";
};
export function Steps(props: StepsProps) { return <CatalogComponent catalogId="44287:4510" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
