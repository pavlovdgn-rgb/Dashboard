import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SpinnerAnimated.module.css';
export type SpinnerAnimatedProps = CatalogProps & {
  "Size"?: "XX-Large" | "X-Large" | "Large" | "Medium*" | "Small";
  "Keyframe"?: "1" | "2" | "3" | "4";
};
export function SpinnerAnimated(props: SpinnerAnimatedProps) { return <CatalogComponent catalogId="27320:288580" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
