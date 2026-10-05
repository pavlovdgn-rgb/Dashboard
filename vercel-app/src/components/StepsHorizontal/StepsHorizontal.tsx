import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './StepsHorizontal.module.css';
export type StepsHorizontalProps = CatalogProps & {
  "Size"?: "Medium" | "Small" | "XSmall";
};
export function StepsHorizontal(props: StepsHorizontalProps) { return <CatalogComponent catalogId="44199:23052" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
