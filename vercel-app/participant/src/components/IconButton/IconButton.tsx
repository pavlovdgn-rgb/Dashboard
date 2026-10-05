import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './IconButton.module.css'

export interface IconButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'style'> {
  icon: ReactNode
  'aria-label': string
}

/** Icon Button — ds/components.md → "Действия / Icon Button". Квадратная кнопка под иконку без подписи. */
export function IconButton({ icon, className, ...rest }: IconButtonProps) {
  return (
    <button type="button" className={cx(styles.iconButton, className)} {...rest}>
      {icon}
    </button>
  )
}
