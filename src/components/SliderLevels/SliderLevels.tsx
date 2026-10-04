import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SliderLevels.module.css';
export type SliderLevelsProps = CatalogProps & {
  "Labels"?: "True" | "False";
  "Compressed"?: "True" | "False";
};
export function SliderLevels(props: SliderLevelsProps) { return <CatalogComponent catalogId="15222:126396" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
