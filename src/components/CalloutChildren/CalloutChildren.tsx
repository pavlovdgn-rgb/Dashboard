import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './CalloutChildren.module.css';
export type CalloutChildrenProps = CatalogProps & {

};
export function CalloutChildren(props: CalloutChildrenProps) { return <CatalogComponent catalogId="45915:7922" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
