import { cx } from '../../lib/cx'
import styles from './TimelineItem.module.css'

export type TimelineItemType = 'call' | 'form' | 'chat'

export interface TimelineItemProps {
  type: TimelineItemType
  title: string
  meta: string
  quote: string
}

/** TimelineItem — ds/components.md → "Данные / TimelineItem". Type: Call|Form|Chat — красит IconBadge (accent-круг без глифа, не иконка — см. отклонение в каталоге). */
export function TimelineItem({ type, title, meta, quote }: TimelineItemProps) {
  return (
    <div className={styles.row}>
      <span className={cx(styles.iconBadge, styles[type])} aria-hidden="true" />
      <div className={styles.content}>
        <span className={styles.title}>{title}</span>
        <span className={styles.meta}>{meta}</span>
        <span className={styles.quote}>«{quote}»</span>
      </div>
    </div>
  )
}
