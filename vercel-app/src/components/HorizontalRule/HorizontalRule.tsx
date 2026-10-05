import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';
import styles from './HorizontalRule.module.css';
export type HorizontalRuleProps = CatalogProps & {
  "Margin"?: "None - 0px" | "X-small - 8px" | "Small - 12px" | "Medium - 16px" | "Large* - 24px" | "X-large - 32px" | "XX-large - 40px";
  "Size"?: "Full" | "Half" | "Quarter";
};
export function HorizontalRule(props: HorizontalRuleProps) { return <CatalogComponent catalogId="15154:113938" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }
