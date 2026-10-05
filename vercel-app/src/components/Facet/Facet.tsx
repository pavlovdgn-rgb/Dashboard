import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Facet.module.css';
export type FacetProps = CatalogProps & {
  "State"?: "Default" | "Hover" | "Focus";
  "Icon"?: "True" | "False";
  "Selected"?: "False" | "True";
  "Disabled"?: "False" | "True";
  "Loading"?: "False" | "True";
};
export function Facet(props: FacetProps) { return <CatalogComponent catalogId="13653:64632" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
