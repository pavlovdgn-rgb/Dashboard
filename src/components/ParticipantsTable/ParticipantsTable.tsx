import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ParticipantsTable.module.css';
export type ParticipantsTableProps = CatalogProps & {
  "State"?: "Ready" | "Loading" | "Empty" | "FilteredEmpty" | "Error";
};
export function ParticipantsTable(props: ParticipantsTableProps) { return <CatalogComponent catalogId="153:1605" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
