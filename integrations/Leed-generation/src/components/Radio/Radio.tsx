import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Radio.module.css'

export interface RadioProps {
  selected: boolean
  onChange?: () => void
  disabled?: boolean
  label?: ReactNode
  name?: string
  id?: string
}

/** Radio — ds/components.md → "Ввод / Radio". Selected=No|Yes; State: Normal|Hover|Disabled. Label — как у Checkbox, удобство API поверх анатомии без своего лейбла. */
export function Radio({ selected, onChange, disabled = false, label, name, id }: RadioProps) {
  return (
    <label className={cx(styles.row, disabled && styles.disabled)} htmlFor={id}>
      <input id={id} type="radio" name={name} className={styles.input} checked={selected} disabled={disabled} onChange={() => onChange?.()} />
      <span className={cx(styles.circle, selected && styles.selected)}>{selected && <span className={styles.dot} />}</span>
      {label}
    </label>
  )
}
