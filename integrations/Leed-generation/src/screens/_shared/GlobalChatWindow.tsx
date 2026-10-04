import { ChatWindow, type ChatWindowMessage } from '../../components/ChatWindow'
import { buildChatSummaries, trailingUnreadCount } from '../../data/chatSummaries'
import { useChatWindow } from '../../data/ChatWindowContext'
import { formatRelativeTime } from '../../data/format'
import { initials } from '../../data/leads'
import { useLeads } from '../../data/LeadsContext'

const CURRENT_MANAGER = 'Игорь Петров'

/**
 * Единственный на всё приложение рендер плавающего ChatWindow — смонтирован один раз в App.tsx рядом с
 * <Routes> (см. ChatWindowContext), поэтому НЕ размонтируется при переходах между разделами: то самое
 * «персистентно между Лиды→Канбан→Дашборд→Настройки» из ds/components.md. Сам компонент ChatWindow не
 * позиционирует себя (см. его же docblock) — fixed bottom/right назначает эта обёртка. Drag-перетаскивание
 * окна по экрану — отдельная задача, не входит сюда (та же граница, что и в компоненте).
 */
export function GlobalChatWindow() {
  const { activeLeadId, windowState, minimize, expand, closeChat, openChat } = useChatWindow()
  const { leads, getLead, addChatMessage } = useLeads()

  const lead = activeLeadId ? getLead(activeLeadId) : undefined
  if (!lead) return null

  const messages: ChatWindowMessage[] = lead.messages.map((m) => ({
    id: m.id,
    sender: m.sender,
    meta: `${m.authorLabel}, ${formatRelativeTime(m.at)}`,
    message: m.message,
  }))

  return (
    <div style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 45 }}>
      <ChatWindow
        state={windowState}
        leadName={lead.name}
        leadInitials={initials(lead.name)}
        messages={messages}
        unreadCount={trailingUnreadCount(lead.messages)}
        onSend={(text) => addChatMessage(lead.id, { sender: 'manager', authorLabel: `Менеджер (${CURRENT_MANAGER})`, message: text })}
        onMinimize={minimize}
        onExpand={expand}
        onClose={closeChat}
        chats={buildChatSummaries(leads)}
        onSelectChat={openChat}
      />
    </div>
  )
}
