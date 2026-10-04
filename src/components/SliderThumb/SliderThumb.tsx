import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SliderThumb.module.css';
export type SliderThumbProps = CatalogProps & {
  "Tooltip"?: "None" | "Left" | "Right";
};
export function SliderThumb(props: SliderThumbProps) { return <CatalogComponent catalogId="14757:83542" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
