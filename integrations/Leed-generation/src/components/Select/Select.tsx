import { useRef, useState } from 'react'
import { cx } from '../../lib/cx'
import { useClickOutside } from '../../lib/useClickOutside'
import styles from './Select.module.css'

export interface SelectProps {
  value: string
  onChange?: (value: string) => void
  options: string[]
  disabled?: boolean
  error?: boolean
}

/**
 * Select — ds/components.md → "Ввод / Select". Специализация Input под паттерн выбора из Dropdown.Panel.
 * State: default|hover|focus|error|disabled. **Не нативный `<select>`** — тот отдаёт направление открытия
 * браузеру/ОС и может открыться вверх поверх собственного поля; здесь панель управляется самим компонентом
 * и всегда открывается вниз, как и Dropdown.
 */
export function Select({ value, onChange, options, disabled = false, error = false }: SelectProps) {
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef<HTMLDivElement>(null)
  useClickOutside(wrapperRef, open, () => setOpen(false))

  return (
    <div className={styles.wrapper} ref={wrapperRef}>
      <button
        type="button"
        className={cx(styles.select, open && styles.open, error && styles.error, disabled && styles.disabled)}
        disabled={disabled}
        onClick={() => setOpen((v) => !v)}
      >
        <span className={styles.value}>{value}</span>
        <svg className={cx(styles.chevron, open && styles.open)} viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open && options.length > 0 && (
        <div className={styles.panel}>
          {options.map((option) => (
            <button
              key={option}
              type="button"
              className={styles.option}
              onClick={() => {
                onChange?.(option)
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
