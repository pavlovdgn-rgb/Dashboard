import { cx } from '../../lib/cx'
import styles from './Tabs.module.css'

export interface TabsProps {
  active?: boolean
  disabled?: boolean
  onClick?: () => void
  children: string
}

/** Tabs — ds/components.md → "Навигация / Tabs". Один инстанс = один таб; State: default|active|disabled. Композиция ряда — на стороне потребителя. */
export function Tabs({ active = false, disabled = false, onClick, children }: TabsProps) {
  return (
    <button type="button" className={cx(styles.tab, active && styles.active, disabled && styles.disabled)} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  )
}
