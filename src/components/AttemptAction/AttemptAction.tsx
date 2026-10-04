import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './AttemptAction.module.css';
export type AttemptActionProps = CatalogProps & {
  "Mode"?: "Single" | "Multiple" | "Unavailable";
};
export function AttemptAction(props: AttemptActionProps) { return <CatalogComponent catalogId="152:996" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
