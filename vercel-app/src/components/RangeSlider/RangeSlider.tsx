import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './RangeSlider.module.css';
export type RangeSliderProps = CatalogProps & {
  "Label"?: "None" | "Left" | "Right" | "Both";
  "Input"?: "None" | "Left" | "Right" | "Both";
  "Compressed"?: "False" | "True";
};
export function RangeSlider(props: RangeSliderProps) { return <CatalogComponent catalogId="14755:6227" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
