import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Spacer.module.css';
export type SpacerProps = CatalogProps & {
  "Size"?: "XS - 4px" | "S - 8px" | "M - 16px" | "L - 24px (Default)" | "XL - 32px" | "XXL - 40px";
  "Direction"?: "Horizontal" | "Vertical";
};
export function Spacer(props: SpacerProps) { return <CatalogComponent catalogId="14917:33" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
