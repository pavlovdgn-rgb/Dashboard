import { cx } from '../../lib/cx'
import styles from './StatusBadge.module.css'

export type StatusBadgeStatus = 'success' | 'error' | 'warning' | 'neutral'

export interface StatusBadgeProps {
  status: StatusBadgeStatus
  children: string
}

/**
 * Status Badge — ds/components.md → "Фидбэк / Status Badge". Status: Success|Error|Warning|Neutral.
 * Neutral рендерится голубым (color/extra/blue-10 / blue-100), не серым — так в самом дизайне Infotech_UI, см. находку в каталоге.
 */
export function StatusBadge({ status, children }: StatusBadgeProps) {
  return (
    <span className={cx(styles.badge, styles[status])}>
      <span className={styles.dot} aria-hidden="true" />
      {children}
    </span>
  )
}
