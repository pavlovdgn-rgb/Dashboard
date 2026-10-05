import type { ChangeEvent, KeyboardEvent, ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Input.module.css'

export type InputType = 'text' | 'textarea'

export interface InputProps {
  type?: InputType
  label?: string
  showLabel?: boolean
  value: string
  onChange?: (value: string) => void
  onKeyDown?: (e: KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  placeholder?: string
  hint?: string
  showHint?: boolean
  icon?: ReactNode
  showIcon?: boolean
  disabled?: boolean
  error?: boolean
  id?: string
}

/** Input — ds/components.md → "Ввод / Input". Type=Text|Textarea; State — Hover/Focus нативные, Error/Disabled — пропы. */
export function Input({
  type = 'text',
  label,
  showLabel = true,
  value,
  onChange,
  onKeyDown,
  placeholder,
  hint,
  showHint = false,
  icon,
  showIcon = false,
  disabled = false,
  error = false,
  id,
}: InputProps) {
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => onChange?.(e.target.value)

  return (
    <div className={styles.wrapper}>
      {label && showLabel && (
        <label className={styles.label} htmlFor={id}>
          {label}
        </label>
      )}
      <div className={cx(styles.field, type === 'textarea' && styles.textarea, error && styles.error, disabled && styles.disabled)}>
        {showIcon && icon && <span className={styles.icon}>{icon}</span>}
        {type === 'textarea' ? (
          <textarea id={id} className={styles.value} rows={3} value={value} onChange={handleChange} onKeyDown={onKeyDown} placeholder={placeholder} disabled={disabled} />
        ) : (
          <input id={id} className={styles.value} value={value} onChange={handleChange} onKeyDown={onKeyDown} placeholder={placeholder} disabled={disabled} />
        )}
      </div>
      {showHint && hint && <span className={cx(styles.hint, error && styles.error)}>{hint}</span>}
    </div>
  )
}
