import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './SelectableListItem.module.css';
export type SelectableListItemProps = CatalogProps & {
  "Type"?: "Selectable" | "Group title" | "Super select" | "Context menu (S)" | "Context menu (M)" | "Search" | "Color palette" | "Loading" | "Empty" | "Custom (S)" | "Custom (M)";
  "Checked?"?: "Off" | "On" | "N/A";
  "Disabled?"?: "False" | "True";
  "State"?: "Default" | "Focus";
  "Extras"?: "None" | "Prepend" | "Append" | "Both";
};
export function SelectableListItem(props: SelectableListItemProps) { return <CatalogComponent catalogId="14664:0" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
