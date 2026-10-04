import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextSmall.module.css';
export type TextSmallProps = CatalogProps & {
  "Text#32350:3"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextSmall(props: TextSmallProps) { return <CatalogComponent catalogId="32350:391882" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
