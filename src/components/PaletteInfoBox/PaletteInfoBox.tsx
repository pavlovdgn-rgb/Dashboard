import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PaletteInfoBox.module.css';
export type PaletteInfoBoxProps = CatalogProps & {

};
export function PaletteInfoBox(props: PaletteInfoBoxProps) { return <CatalogComponent catalogId="16160:208428" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
