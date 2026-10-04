import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SliderTrack.module.css';
export type SliderTrackProps = CatalogProps & {
  "Compressed"?: "True" | "False";
};
export function SliderTrack(props: SliderTrackProps) { return <CatalogComponent catalogId="17068:2" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
