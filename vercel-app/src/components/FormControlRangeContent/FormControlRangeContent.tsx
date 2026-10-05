import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './FormControlRangeContent.module.css';
export type FormControlRangeContentProps = CatalogProps & {
  "Invalid"?: "False" | "True";
};
export function FormControlRangeContent(props: FormControlRangeContentProps) { return <CatalogComponent catalogId="28545:409159" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
