import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Tour.module.css';
export type TourProps = CatalogProps & {
  "Title#36391:3"?: boolean;
  "Meta Title#36391:5"?: boolean;
  "Description#36391:16"?: boolean;
  "Next#36435:0"?: boolean;
  "Skip#36435:9"?: boolean;
  "Dots#36441:48"?: boolean;
  "Arrow"?: "↑ Top" | "-> Right" | "↓ Bottom" | "← Left";
};
export function Tour(props: TourProps) { return <CatalogComponent catalogId="36391:397462" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
