import { cx } from '../../lib/cx'
import styles from './Toast.module.css'

export type ToastStatus = 'success' | 'error' | 'warning' | 'info'

export interface ToastProps {
  status?: ToastStatus
  children: string
}

/** Toast — ds/components.md → "Ввод / Toast". Status: success|error|warning|info. Иконка переиспользует Exclamation Mark в Figma; здесь — currentColor-глиф. */
export function Toast({ status = 'success', children }: ToastProps) {
  return (
    <span className={cx(styles.toast, styles[status])}>
      <svg className={styles.icon} viewBox="0 0 16 16" fill="none" aria-hidden="true">
        <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" />
        <path d="M8 5V8.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="8" cy="11" r="0.75" fill="currentColor" />
      </svg>
      {children}
    </span>
  )
}
