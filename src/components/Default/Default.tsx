import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Default.module.css';
export type DefaultProps = CatalogProps & {
  "Checked"?: "True" | "False";
  "Disabled"?: "False" | "True";
};
export function Default(props: DefaultProps) { return <CatalogComponent catalogId="37824:395926" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
