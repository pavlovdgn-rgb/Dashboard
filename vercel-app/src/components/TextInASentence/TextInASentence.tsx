import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './TextInASentence.module.css';
export type TextInASentenceProps = CatalogProps & {
  "Example"?: "Keyboard" | "Link";
};
export function TextInASentence(props: TextInASentenceProps) { return <CatalogComponent catalogId="32347:391902" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
