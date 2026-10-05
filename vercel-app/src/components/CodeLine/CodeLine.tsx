import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CodeLine.module.css';
export type CodeLineProps = CatalogProps & {

};
export function CodeLine(props: CodeLineProps) { return <CatalogComponent catalogId="41028:3667" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
