import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './DescribedFormGroup.module.css';
export type DescribedFormGroupProps = CatalogProps & {
  "Ratio"?: "Half*" | "Third" | "Quarter";
};
export function DescribedFormGroup(props: DescribedFormGroupProps) { return <CatalogComponent catalogId="27008:287534" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
