import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './BodyVertical.module.css';
export type BodyVerticalProps = CatalogProps & {
  "Padding Size"?: "Large" | "Medium" | "Small" | "None";
};
export function BodyVertical(props: BodyVerticalProps) { return <CatalogComponent catalogId="36674:396011" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
