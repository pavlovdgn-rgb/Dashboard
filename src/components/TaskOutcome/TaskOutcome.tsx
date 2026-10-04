import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TaskOutcome.module.css';
export type TaskOutcomeProps = CatalogProps & {
  "Status"?: "Achieved" | "NotAchieved" | "NotAssessed";
};
export function TaskOutcome(props: TaskOutcomeProps) { return <CatalogComponent catalogId="152:948" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
