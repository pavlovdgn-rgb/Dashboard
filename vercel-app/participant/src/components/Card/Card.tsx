import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import styles from './Card.module.css'

export type CardPadding = 'compact' | 'default'

export interface CardProps {
  padding?: CardPadding
  border?: boolean
  children: ReactNode
}

/**
 * Card — ds/components.md → "Контейнеры / Card". Padding: compact|default; Border: yes|no.
 * В Figma инстанс Card не принимает appendChild реальных детей (см. находку в каталоге) — в коде это ограничение не действует, children рендерятся как обычно.
 */
export function Card({ padding = 'default', border = false, children }: CardProps) {
  return <div className={cx(styles.card, padding === 'default' ? styles.paddingDefault : styles.paddingCompact, border && styles.bordered)}>{children}</div>
}
