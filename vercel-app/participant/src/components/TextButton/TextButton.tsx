import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './TextButton.module.css'

export interface TextButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'style'> {
  rightIcon?: ReactNode
  children: ReactNode
}

/** Text Button — ds/components.md → "Действия / Text Button". Link-style, no background, для второстепенных действий. */
export function TextButton({ rightIcon, className, children, ...rest }: TextButtonProps) {
  return (
    <button type="button" className={cx(styles.textButton, className)} {...rest}>
      {children}
      {rightIcon && <span className={styles.icon}>{rightIcon}</span>}
    </button>
  )
}
