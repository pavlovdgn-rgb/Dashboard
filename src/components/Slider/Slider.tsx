import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Slider.module.css';
export type SliderProps = CatalogProps & {
  "Type"?: "Single" | "Dual";
  "Show range"?: "True" | "False";
  "Compressed"?: "False" | "True";
  "Ticks"?: "False" | "True";
  "Levels"?: "False" | "True";
};
export function Slider(props: SliderProps) { return <CatalogComponent catalogId="14757:86523" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
