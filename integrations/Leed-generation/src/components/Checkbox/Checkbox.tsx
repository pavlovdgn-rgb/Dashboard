import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Checkbox.module.css'

export interface CheckboxProps {
  checked: boolean
  onChange?: (checked: boolean) => void
  disabled?: boolean
  label?: ReactNode
  id?: string
}

/**
 * Checkbox — ds/components.md → "Ввод / Checkbox". Checked=No|Yes; State: Normal|Hover|Disabled.
 * Мастер не несёт своего текстового лейбла — каждый инстанс в Figma оборачивается локальной строкой Checkbox+Text; здесь label — удобство API, не отход от анатомии.
 */
export function Checkbox({ checked, onChange, disabled = false, label, id }: CheckboxProps) {
  return (
    <label className={cx(styles.row, disabled && styles.disabled)} htmlFor={id}>
      <input
        id={id}
        type="checkbox"
        className={styles.input}
        checked={checked}
        disabled={disabled}
        onChange={(e) => onChange?.(e.target.checked)}
      />
      <span className={cx(styles.box, checked && styles.checked)}>
        {checked && (
          <svg className={styles.checkmark} viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <path d="M2 6L5 9L10 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </span>
      {label}
    </label>
  )
}
