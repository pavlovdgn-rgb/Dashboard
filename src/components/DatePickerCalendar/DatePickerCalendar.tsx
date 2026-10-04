import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DatePickerCalendar.module.css';
export type DatePickerCalendarProps = CatalogProps & {
  "Time"?: "Off" | "On" | "Only";
};
export function DatePickerCalendar(props: DatePickerCalendarProps) { return <CatalogComponent catalogId="14787:3001" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
