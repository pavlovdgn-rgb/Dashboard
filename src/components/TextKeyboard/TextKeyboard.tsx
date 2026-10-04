import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextKeyboard.module.css';
export type TextKeyboardProps = CatalogProps & {
  "Content#32286:1"?: string;
  "Size"?: "Medium" | "Small" | "X-Small";
};
export function TextKeyboard(props: TextKeyboardProps) { return <CatalogComponent catalogId="32286:391636" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
