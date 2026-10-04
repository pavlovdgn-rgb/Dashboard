import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './AvatarGroupList.module.css';
export type AvatarGroupListProps = CatalogProps & {

};
export function AvatarGroupList(props: AvatarGroupListProps) { return <CatalogComponent catalogId="26769:282323" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
