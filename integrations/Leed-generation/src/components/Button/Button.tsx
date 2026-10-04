import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Button.module.css'

export type ButtonStyleVariant = 'primary' | 'secondary' | 'tertiary'
export type ButtonSize = 'm' | 's'

export interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'style'> {
  variant?: ButtonStyleVariant
  size?: ButtonSize
  leftIcon?: ReactNode
  rightIcon?: ReactNode
  loading?: boolean
  children: ReactNode
}

/** Button — ds/components.md → "Действия / Button". Style×Size are props; Hover/Pressed/Focused are native pseudo-classes. */
export function Button({
  variant = 'primary',
  size = 'm',
  leftIcon,
  rightIcon,
  loading = false,
  disabled,
  className,
  children,
  ...rest
}: ButtonProps) {
  const styleClass = variant === 'primary' ? styles.stylePrimary : variant === 'secondary' ? styles.styleSecondary : styles.styleTertiary
  const sizeClass = size === 'm' ? styles.sizeM : styles.sizeS

  return (
    <button
      type="button"
      className={cx(styles.button, styleClass, sizeClass, className)}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <span className={styles.loadingSpinner} aria-hidden="true" />
      ) : (
        leftIcon && <span className={styles.icon}>{leftIcon}</span>
      )}
      {children}
      {!loading && rightIcon && <span className={styles.icon}>{rightIcon}</span>}
    </button>
  )
}
