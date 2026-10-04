import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Tooltip.module.css'

export type TooltipPosition = 'top' | 'bottom'

export interface TooltipProps {
  content: string
  position?: TooltipPosition
  children: ReactNode
}

/**
 * Tooltip — ds/components.md → "Ввод / Tooltip" (Node ID 47:508). Position: top|bottom, показывается по hover/focus триггера.
 * Сверено напрямую с Figma: bubble — color/bg/surface-secondary + color/text/on-dark, Desktop/Label Medium; arrow — треугольник
 * 11×5px того же цвета, что bubble, на стороне, обращённой к триггеру (снизу для Top, сверху для Bottom).
 */
export function Tooltip({ content, position = 'top', children }: TooltipProps) {
  const arrow = <span className={styles.arrow} aria-hidden="true" />
  return (
    <span className={styles.wrapper}>
      {children}
      <span className={cx(styles.popup, styles[position])} role="tooltip">
        {position === 'bottom' && arrow}
        <span className={styles.bubble}>{content}</span>
        {position === 'top' && arrow}
      </span>
    </span>
  )
}
