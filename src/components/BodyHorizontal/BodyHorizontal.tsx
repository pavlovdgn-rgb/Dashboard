import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './BodyHorizontal.module.css';
export type BodyHorizontalProps = CatalogProps & {
  "Padding size"?: "Large" | "Medium" | "Small" | "None";
};
export function BodyHorizontal(props: BodyHorizontalProps) { return <CatalogComponent catalogId="36686:394689" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
