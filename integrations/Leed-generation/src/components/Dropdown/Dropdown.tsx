import { useRef, useState } from 'react'
import { cx } from '../../lib/cx'
import { useClickOutside } from '../../lib/useClickOutside'
import styles from './Dropdown.module.css'

export interface DropdownProps {
  label: string
  options?: string[]
  onSelect?: (option: string) => void
  disabled?: boolean
}

/** Dropdown — ds/components.md → "Ввод / Dropdown". State: closed|open (клик) |hover (нативно) |disabled. Шеврон поворачивается на 180° в открытом состоянии. */
export function Dropdown({ label, options, onSelect, disabled = false }: DropdownProps) {
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef<HTMLDivElement>(null)
  useClickOutside(wrapperRef, open, () => setOpen(false))

  return (
    <div className={styles.wrapper} ref={wrapperRef}>
      <button
        type="button"
        className={cx(styles.trigger, open && styles.open, disabled && styles.disabled)}
        disabled={disabled}
        onClick={() => setOpen((v) => !v)}
      >
        <span className={styles.triggerLabel}>{label}</span>
        <svg className={cx(styles.chevron, open && styles.open)} viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open && options && options.length > 0 && (
        <div className={styles.panel}>
          {options.map((option) => (
            <button
              key={option}
              type="button"
              className={styles.option}
              onClick={() => {
                onSelect?.(option)
                setOpen(false)
              }}
            >
              {option}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
