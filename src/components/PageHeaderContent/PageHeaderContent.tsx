import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './PageHeaderContent.module.css';
export type PageHeaderContentProps = CatalogProps & {

};
export function PageHeaderContent(props: PageHeaderContentProps) { return <CatalogComponent catalogId="24329:284522" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
