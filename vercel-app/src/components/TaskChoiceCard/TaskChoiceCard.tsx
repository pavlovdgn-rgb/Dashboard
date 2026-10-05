import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TaskChoiceCard.module.css';
export type TaskChoiceCardProps = CatalogProps & {
  "Title#260:0"?: string;
  "Description#260:9"?: string;
  "Selected"?: "False" | "True";
  "State"?: "Default" | "Hover" | "Focus" | "Disabled";
};
export function TaskChoiceCard(props: TaskChoiceCardProps) { return <CatalogComponent catalogId="260:3028" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
