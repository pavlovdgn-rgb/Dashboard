import { cx } from '../../lib/cx'
import styles from './Toggle.module.css'

export interface ToggleProps {
  on: boolean
  onChange?: (on: boolean) => void
  disabled?: boolean
  'aria-label'?: string
}

/** Toggle — ds/components.md → "Ввод / Toggle". Position=Off|On; State: Normal|Hover|Disabled. */
export function Toggle({ on, onChange, disabled = false, ...rest }: ToggleProps) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      className={cx(styles.track, on && styles.on, disabled && styles.disabled)}
      disabled={disabled}
      onClick={() => onChange?.(!on)}
      {...rest}
    >
      <span className={styles.thumb} />
    </button>
  )
}
