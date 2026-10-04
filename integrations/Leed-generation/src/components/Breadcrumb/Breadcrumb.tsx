import { cx } from '../../lib/cx'
import styles from './Breadcrumb.module.css'

export interface BreadcrumbProps {
  current?: boolean
  onClick?: () => void
  children: string
}

/** Breadcrumb — ds/components.md → "Навигация / Breadcrumb". State: default|current. */
export function Breadcrumb({ current = false, onClick, children }: BreadcrumbProps) {
  return (
    <button type="button" className={cx(styles.crumb, current && styles.current)} onClick={onClick}>
      {children}
    </button>
  )
}
