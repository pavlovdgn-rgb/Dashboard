import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Accordion.module.css';
export type AccordionProps = CatalogProps & {
  "Extra action#32609:2"?: boolean;
  "Expand"?: "False" | "True";
  "Arrow display"?: "Left" | "Right";
  "Loading"?: "False" | "True";
  "Disabled"?: "False" | "True";
};
export function Accordion(props: AccordionProps) { return <CatalogComponent catalogId="32609:392204" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
