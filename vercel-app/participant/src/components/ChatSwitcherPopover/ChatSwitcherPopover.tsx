import { Avatar } from '../Avatar'
import { UnreadBadge } from '../UnreadBadge'
import { cx } from '../../lib/cx'
import styles from './ChatSwitcherPopover.module.css'

export interface ChatSummary {
  id: string
  initials: string
  name: string
  preview: string
  time: string
  unread: number
}

export interface ChatSwitcherPopoverProps {
  chats: ChatSummary[]
  onSelect: (id: string) => void
}

/**
 * ChatSwitcherPopover — ds/components.md → "ChatSwitcherPopover". Список активных переписок для быстрого
 * переключения — решает находку «слишком много кликов до чата с другим лидом» (строка/карточка → карточка
 * лида → «Написать в чат»). Два места вызова: ChatIconButton в ModuleNav, и клик по имени+шеврону в TitleBar
 * самого ChatWindow (см. ChatWindow.tsx). Клик по строке — открывает ChatWindow с этим лидом, окно одно на
 * весь интерфейс, не плодит несколько параллельных окон.
 */
export function ChatSwitcherPopover({ chats, onSelect }: ChatSwitcherPopoverProps) {
  return (
    <div className={styles.popover}>
      <div className={styles.header}>
        <span className="ds-desktop-main-semibold">Чаты</span>
      </div>
      {chats.map((chat) => (
        <button key={chat.id} type="button" className={cx(styles.row, chat.unread > 0 && styles.rowUnread)} onClick={() => onSelect(chat.id)}>
          <Avatar size="sm" initials={chat.initials} />
          <div className={styles.textCol}>
            <span className={cx('ds-desktop-main-regular', chat.unread > 0 && styles.nameUnread)} style={{ color: 'var(--color-text-primary)' }}>
              {chat.name}
            </span>
            <span className="ds-desktop-breadcrumbs-regular" style={{ color: 'var(--color-text-secondary)' }}>
              {chat.preview}
            </span>
          </div>
          <div className={styles.metaCol}>
            <span className="ds-desktop-breadcrumbs-regular" style={{ color: 'var(--color-text-secondary)' }}>
              {chat.time}
            </span>
            {chat.unread > 0 && <UnreadBadge size="sm" count={chat.unread} />}
          </div>
        </button>
      ))}
    </div>
  )
}
