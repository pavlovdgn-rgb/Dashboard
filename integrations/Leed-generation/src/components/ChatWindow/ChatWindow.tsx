import { useState } from 'react'
import { Avatar } from '../Avatar'
import { Button } from '../Button'
import { ChatSwitcherPopover, type ChatSummary } from '../ChatSwitcherPopover'
import { IconButton } from '../IconButton'
import { Input } from '../Input'
import { MessageBubble, type MessageBubbleSender } from '../MessageBubble'
import { UnreadBadge } from '../UnreadBadge'
import { ChevronDownIcon, CloseIcon, MinusIcon } from '../../screens/_shared/icons'
import styles from './ChatWindow.module.css'

export type ChatWindowState = 'expanded' | 'minimized'

export interface ChatWindowMessage {
  id: string
  sender: MessageBubbleSender
  meta: string
  message: string
}

export interface ChatWindowProps {
  state: ChatWindowState
  leadName: string
  leadInitials: string
  messages: ChatWindowMessage[]
  /** Непрочитанные именно в этом чате — показывается на плашке State=Minimized. */
  unreadCount?: number
  onSend: (text: string) => void
  onMinimize: () => void
  onExpand: () => void
  onClose: () => void
  /** Список для ChatSwitcherPopover — если не передан, имя/шеврон в TitleBar не кликабельны (переключаться некуда). */
  chats?: ChatSummary[]
  onSelectChat?: (id: string) => void
}

/**
 * ChatWindow — ds/components.md → "ChatWindow". TitleBar-переключатель — имя + шеврон 16px, БЕЗ ведущей
 * иконки-пузыря: в Figma её пробовали (2-я итерация чата, снимала путаницу с соседним шевроном «свернуть»),
 * но убрали финальным решением (3-я итерация) — пузырь скрывал единственный намёк, что элемент кликабелен.
 * Плавающее окно чата с лидом — перетаскиваемое поверх
 * интерфейса (НЕ докнутая справа slide-over панель, как было раньше в ChatConversationPanel), не блокирует
 * остальной интерфейс под собой, задумано как персистентное между разделами CRM (глобальный стейт, не
 * привязано к route). State: Expanded | Minimized.
 *
 * Компонент НЕ навязывает позиционирование (position/top/left) — родитель решает, где на экране разместить.
 * В живом приложении это GlobalChatWindow.tsx (fixed bottom/right, см. ChatWindowContext) — единственный
 * рендер на всё приложение, персистентный между разделами. Drag-перетаскивание окна по экрану всё ещё НЕ
 * реализовано — отдельная задача, не входит в подключение к живому приложению (2026-08-29).
 */
export function ChatWindow(props: ChatWindowProps) {
  // key={state} форсирует remount при Expanded↔Minimized — .stateTransition проигрывает fade+scale
  // keyframe заново на каждый remount (см. ChatWindow.module.css). Раньше переключение было мгновенным
  // React-свапом двух совсем разных деревьев (окно ↔ плашка) без единого кадра перехода — Storybook
  // «Interactive» это особенно подчёркивал, ведь только там state меняется вживую по клику.
  return (
    <div key={props.state} className={styles.stateTransition}>
      {props.state === 'minimized' ? <MinimizedPill {...props} /> : <ExpandedWindow {...props} />}
    </div>
  )
}

function MinimizedPill({ leadName, leadInitials, unreadCount = 0, onExpand }: ChatWindowProps) {
  return (
    <button type="button" className={styles.pill} onClick={onExpand}>
      <Avatar size="sm" initials={leadInitials} />
      <span className="ds-desktop-main-semibold" style={{ color: 'var(--color-text-primary)' }}>
        {leadName}
      </span>
      {unreadCount > 0 && <UnreadBadge size="sm" count={unreadCount} />}
      <span className={styles.pillChevron} aria-hidden="true">
        <ChevronDownIcon />
      </span>
    </button>
  )
}

function ExpandedWindow({ leadName, messages, onSend, onMinimize, onClose, chats, onSelectChat }: ChatWindowProps) {
  const [draft, setDraft] = useState('')
  const [switcherOpen, setSwitcherOpen] = useState(false)

  const send = () => {
    if (!draft.trim()) return
    onSend(draft.trim())
    setDraft('')
  }

  const canSwitch = !!chats && chats.length > 0

  return (
    <div className={styles.window}>
      <div className={styles.titleBar}>
        <button
          type="button"
          className={styles.switcherTrigger}
          onClick={() => canSwitch && setSwitcherOpen((v) => !v)}
          disabled={!canSwitch}
          aria-haspopup={canSwitch ? 'true' : undefined}
          aria-expanded={canSwitch ? switcherOpen : undefined}
        >
          <span className="ds-desktop-main-semibold" style={{ color: 'var(--color-text-primary)' }}>
            {leadName}
          </span>
          {canSwitch && (
            <span className={styles.switcherChevron} aria-hidden="true">
              <ChevronDownIcon />
            </span>
          )}
        </button>
        <span style={{ flex: '1 1 0%' }} />
        <IconButton icon={<MinusIcon />} aria-label="Свернуть" onClick={onMinimize} />
        <IconButton icon={<CloseIcon />} aria-label="Закрыть" onClick={onClose} />
      </div>

      {switcherOpen && canSwitch && (
        <div className={styles.switcherAnchor}>
          <ChatSwitcherPopover
            chats={chats!}
            onSelect={(id) => {
              setSwitcherOpen(false)
              onSelectChat?.(id)
            }}
          />
        </div>
      )}

      <div className={styles.messageList}>
        {messages.map((m) => (
          <MessageBubble key={m.id} sender={m.sender} meta={m.meta} message={m.message} />
        ))}
      </div>

      <div className={styles.composer}>
        <div style={{ flex: 1 }}>
          <Input
            value={draft}
            onChange={setDraft}
            placeholder="Написать сообщение..."
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault()
                send()
              }
            }}
          />
        </div>
        <Button onClick={send} disabled={!draft.trim()}>
          Отправить
        </Button>
      </div>
    </div>
  )
}

