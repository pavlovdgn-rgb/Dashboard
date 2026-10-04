import { cx } from '../../lib/cx'
import { Avatar } from '../Avatar'
import styles from './KanbanCard.module.css'

export interface KanbanCardProps {
  channel: string
  nameCompany: string
  score: number
  timeText: string
  managerName?: string
  managerInitials?: string
  overdue?: boolean
}

/** KanbanCard — ds/components.md → "Ввод / KanbanCard". Overdue: No|Yes — единственная formal-ось, красит TimeText и border карточки. */
export function KanbanCard({ channel, nameCompany, score, timeText, managerName, managerInitials, overdue = false }: KanbanCardProps) {
  const assigned = Boolean(managerName)
  return (
    <div className={cx(styles.card, overdue && styles.overdue)}>
      <span className={styles.channelTag}>{channel}</span>
      <span className={styles.nameCompany}>{nameCompany}</span>
      <span className={styles.scoreRow}>
        <span className={styles.scoreLabel}>Скор</span>
        <span className={styles.scoreValue}>{score}</span>
      </span>
      <span className={cx(styles.timeText, overdue && styles.overdue)}>{timeText}</span>
      <span className={styles.managerRow}>
        {assigned && managerInitials && <Avatar size="sm" initials={managerInitials} />}
        <span className={cx(styles.managerName, !assigned && styles.unassigned)}>{managerName ?? 'не назначен'}</span>
      </span>
    </div>
  )
}
