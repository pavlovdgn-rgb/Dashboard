import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './NavMenu.module.css';
export type NavMenuProps = CatalogProps & {
  "FooterText#153:16"?: string;
  "ProjectLabel#153:27"?: string;
  "StudyLabel#153:38"?: string;
  "Active"?: "Projects" | "Studies" | "Setup" | "Launch" | "Overview" | "Heatmap" | "Funnel" | "Participants" | "Signals" | "PDF";
};
export function NavMenu(props: NavMenuProps) { return <CatalogComponent catalogId="153:2777" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
