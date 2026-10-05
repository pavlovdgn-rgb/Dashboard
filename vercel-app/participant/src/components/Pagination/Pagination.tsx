import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Pagination.module.css'

export interface PaginationProps {
  active?: boolean
  disabled?: boolean
  onClick?: () => void
  icon?: ReactNode
  children?: ReactNode
}

/** Pagination — ds/components.md → "Навигация / Pagination". State: default|active|disabled. Prev/Next — тот же чип с icon вместо номера страницы (свои варианты Arrows-атомов, отдельной оси в наборе нет). */
export function Pagination({ active = false, disabled = false, onClick, icon, children }: PaginationProps) {
  return (
    <button type="button" className={cx(styles.chip, active && styles.active, disabled && styles.disabled)} disabled={disabled} onClick={onClick}>
      {icon ? <span className={styles.icon}>{icon}</span> : children}
    </button>
  )
}
