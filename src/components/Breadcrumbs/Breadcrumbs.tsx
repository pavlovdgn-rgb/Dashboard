import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Breadcrumbs.module.css';
export type BreadcrumbsProps = CatalogProps & {

};
export function Breadcrumbs(props: BreadcrumbsProps) { return <CatalogComponent catalogId="42289:57842" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
