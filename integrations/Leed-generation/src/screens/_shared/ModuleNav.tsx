import { useMemo, useRef, useState } from 'react'
import { Avatar } from '../../components/Avatar'
import { ChatSwitcherPopover } from '../../components/ChatSwitcherPopover'
import { StatusBadge, type StatusBadgeStatus } from '../../components/StatusBadge'
import { UnreadBadge } from '../../components/UnreadBadge'
import { useChatWindow } from '../../data/ChatWindowContext'
import { buildChatSummaries } from '../../data/chatSummaries'
import { useLeads } from '../../data/LeadsContext'
import { useClickOutside } from '../../lib/useClickOutside'
import { ChatBubbleIcon } from './icons'
import styles from './ModuleNav.module.css'

export interface ModuleNavProps {
  title?: string
  badge?: { label: string; status: StatusBadgeStatus }
  userName?: string
  userInitials?: string
  /** Явный override — если не передан, считается из живых данных (useLeads().unreadChatsCount). Нужен
   *  только loading/empty-демо экранам без реальных лидов, чтобы показать правдоподобную статичную цифру. */
  unreadCount?: number
}

/**
 * ModuleNav — строка шапки продукта: заголовок+статус слева (контекст текущего экрана), иконка
 * чата+пользователь справа (глобальное, не зависит от экрана) — две смысловые группы разнесены дистанцией,
 * не тонкой линией (см. находку в ds/components.md → ChatIconButton: разделитель-Spacer между бейджем и
 * иконкой чата в одном кластере путаницу решал не до конца, оба бейджа с цифрами читались как пара).
 * Нижний разделитель — теперь всегда (был опциональным `divider` пропом, но аудит `screens_audit`
 * 2026-08-29 показал: он нужен единообразно везде, не только на экранах без своего FiltersBar/Tabs-ряда).
 *
 * Кнопка чата — не просто иконка: сама открывает ChatSwitcherPopover (реальные данные из useLeads()) и
 * сама решает, какой чат открыть (useChatWindow().openChat), не завязана на конкретный экран — тот же
 * компонент, тот же клик, на любой из ~26 инстанс ModuleNav в приложении. Раньше был проп `onChatClick`
 * без единого вызывающего экрана (кнопка ничего не делала) — убран, реальное поведение теперь внутри.
 */
export function ModuleNav({ title = 'Генератор лидов', badge, userName = 'Марина Кузнецова', userInitials = 'МК', unreadCount }: ModuleNavProps) {
  const { leads, unreadChatsCount } = useLeads()
  const { openChat } = useChatWindow()
  const [switcherOpen, setSwitcherOpen] = useState(false)
  const anchorRef = useRef<HTMLDivElement>(null)
  useClickOutside(anchorRef, switcherOpen, () => setSwitcherOpen(false))

  const chats = useMemo(() => buildChatSummaries(leads), [leads])
  const resolvedUnread = unreadCount ?? unreadChatsCount

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-lg)',
        padding: 'var(--space-xl)',
        background: 'var(--color-bg-surface-primary)',
        borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
        width: '100%',
        flexShrink: 0,
      }}
    >
      <span className="ds-desktop-header-1-regular" style={{ color: 'var(--color-text-primary)' }}>
        {title}
      </span>
      {badge && <StatusBadge status={badge.status}>{badge.label}</StatusBadge>}
      <span style={{ flex: '1 1 0%' }} />
      <div ref={anchorRef} style={{ position: 'relative', flexShrink: 0 }}>
        <button
          type="button"
          className={styles.chatButton}
          aria-label="Чаты"
          aria-haspopup="true"
          aria-expanded={switcherOpen}
          onClick={() => setSwitcherOpen((v) => !v)}
        >
          <ChatBubbleIcon />
        </button>
        {resolvedUnread > 0 && (
          <span style={{ position: 'absolute', top: -6, right: -6 }}>
            <UnreadBadge size="sm" count={resolvedUnread} />
          </span>
        )}
        {switcherOpen && (
          <div style={{ position: 'absolute', top: 'calc(100% + 8px)', right: 0, zIndex: 45 }}>
            <ChatSwitcherPopover
              chats={chats}
              onSelect={(id) => {
                setSwitcherOpen(false)
                openChat(id)
              }}
            />
          </div>
        )}
      </div>
      <span style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', flexShrink: 0 }}>
        <Avatar initials={userInitials} />
        <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)', whiteSpace: 'nowrap' }}>
          {userName}
        </span>
      </span>
    </div>
  )
}
