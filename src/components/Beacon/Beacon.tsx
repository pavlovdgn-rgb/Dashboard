import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './Beacon.module.css';
export type BeaconProps = CatalogProps & {

};
export function Beacon(props: BeaconProps) { return <CatalogComponent catalogId="36458:395127" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
