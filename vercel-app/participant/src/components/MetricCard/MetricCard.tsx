import { cx } from '../../lib/cx'
import styles from './MetricCard.module.css'

export type MetricCardTrend = 'neutral' | 'positive' | 'negative'

export interface MetricCardProps {
  label: string
  value: string
  caption: string
  trend?: MetricCardTrend
}

/** MetricCard — ds/components.md → "Контейнеры / MetricCard". Trend красит только Value; Caption всегда secondary. */
export function MetricCard({ label, value, caption, trend = 'neutral' }: MetricCardProps) {
  return (
    <div className={styles.card}>
      <span className={styles.label}>{label}</span>
      <span className={cx(styles.value, styles[trend])}>{value}</span>
      <span className={styles.caption}>{caption}</span>
    </div>
  )
}
