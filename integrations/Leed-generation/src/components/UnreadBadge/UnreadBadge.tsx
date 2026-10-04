import { cx } from '../../lib/cx'
import styles from './UnreadBadge.module.css'

export type UnreadBadgeSize = 'sm' | 'md'

export interface UnreadBadgeProps {
  size?: UnreadBadgeSize
  count: number
}

/**
 * UnreadBadge — ds/components.md → "UnreadBadge". Счётчик непрочитанных сообщений чата — красный кружок с числом.
 * Size: Sm (оверлей на ChatIconButton в ModuleNav) | Md (плашка ChatWindow.State=Minimized, строки ChatSwitcherPopover).
 */
export function UnreadBadge({ size = 'sm', count }: UnreadBadgeProps) {
  if (count <= 0) return null
  return <span className={cx(styles.badge, styles[size])}>{count}</span>
}
