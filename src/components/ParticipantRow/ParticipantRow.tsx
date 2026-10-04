import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ParticipantRow.module.css';
export type ParticipantRowProps = CatalogProps & {
  "ParticipantId#153:0"?: string;
  "Attempt#153:4"?: string;
  "Duration#153:8"?: string;
  "SignalCount#153:12"?: string;
  "State"?: "Default" | "Hover" | "Focus";
};
export function ParticipantRow(props: ParticipantRowProps) { return <CatalogComponent catalogId="153:692" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
