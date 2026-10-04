import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListColorPalletes.module.css';
export type SelectableListColorPalletesProps = CatalogProps & {

};
export function SelectableListColorPalletes(props: SelectableListColorPalletesProps) { return <CatalogComponent catalogId="15884:184289" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
