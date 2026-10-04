import { cx } from '../../lib/cx'
import styles from './FunnelBar.module.css'

export type FunnelBarTone = 'neutral' | 'negative'

export interface FunnelBarProps {
  label: string
  value: number
  /** 0–100, доля полосы относительно максимального значения воронки — в Figma это resize корневого инстанса, здесь — ширина в процентах */
  percent: number
  tone?: FunnelBarTone
}

/** FunnelBar — ds/components.md → "Контейнеры / FunnelBar". Одна строка воронки: Label(168px fixed) → Bar(пропорциональная) → Value. */
export function FunnelBar({ label, value, percent, tone = 'neutral' }: FunnelBarProps) {
  return (
    <div className={styles.row}>
      <span className={styles.label}>{label}</span>
      <span className={styles.track}>
        <span className={cx(styles.bar, styles[tone])} style={{ width: `${percent}%` }} />
      </span>
      <span className={styles.value}>{value}</span>
    </div>
  )
}
