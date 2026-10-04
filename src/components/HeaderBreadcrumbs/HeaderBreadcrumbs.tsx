import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HeaderBreadcrumbs.module.css';
export type HeaderBreadcrumbsProps = CatalogProps & {

};
export function HeaderBreadcrumbs(props: HeaderBreadcrumbsProps) { return <CatalogComponent catalogId="9871:3787" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
