import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './ColorPaletteDisplay.module.css';
export type ColorPaletteDisplayProps = CatalogProps & {
  "Palette"?: "Color blind" | "Color blind (natural)";
};
export function ColorPaletteDisplay(props: ColorPaletteDisplayProps) { return <CatalogComponent catalogId="15884:173623" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
