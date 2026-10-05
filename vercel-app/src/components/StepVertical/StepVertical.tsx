import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './StepVertical.module.css';
export type StepVerticalProps = CatalogProps & {
  "Status"?: "True" | "False";
};
export function StepVertical(props: StepVerticalProps) { return <CatalogComponent catalogId="44287:3458" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
