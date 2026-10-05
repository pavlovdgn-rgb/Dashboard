import { cx } from '../../lib/cx'
import styles from './Avatar.module.css'

export type AvatarSize = 'sm' | 'md'

export interface AvatarProps {
  size?: AvatarSize
  initials: string
}

/** Avatar — ds/components.md → "Действия / Avatar". Size: Sm(24)|Md(32), круг с инициалами. */
export function Avatar({ size = 'md', initials }: AvatarProps) {
  return <span className={cx(styles.circle, styles[size])}>{initials}</span>
}
