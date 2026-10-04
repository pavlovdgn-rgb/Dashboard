import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PaginationRowsPerPage.module.css';
export type PaginationRowsPerPageProps = CatalogProps & {

};
export function PaginationRowsPerPage(props: PaginationRowsPerPageProps) { return <CatalogComponent catalogId="22524:279617" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
