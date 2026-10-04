import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SliderRange.module.css';
export type SliderRangeProps = CatalogProps & {
  "State"?: "Default" | "Empty";
  "Compressed"?: "True" | "False";
};
export function SliderRange(props: SliderRangeProps) { return <CatalogComponent catalogId="14757:83541" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
