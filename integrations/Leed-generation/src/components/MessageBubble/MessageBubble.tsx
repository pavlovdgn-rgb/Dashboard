import { cx } from '../../lib/cx'
import styles from './MessageBubble.module.css'

export type MessageBubbleSender = 'client' | 'manager'

export interface MessageBubbleProps {
  sender: MessageBubbleSender
  meta: string
  message: string
}

/** MessageBubble — ds/components.md → "Данные / MessageBubble". Sender: Client(слева)|Manager(справа), красит фон и выравнивание. */
export function MessageBubble({ sender, meta, message }: MessageBubbleProps) {
  return (
    <div className={cx(styles.row, styles[sender])}>
      <div className={styles.bubble}>
        <span className={styles.meta}>{meta}</span>
        <span className={styles.message}>{message}</span>
      </div>
    </div>
  )
}
