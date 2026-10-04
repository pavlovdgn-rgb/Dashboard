import type { ChatSummary } from '../components/ChatSwitcherPopover'
import { initials } from './leads'
import { formatRelativeTime } from './format'
import type { Lead } from './types'

/**
 * Сколько подряд идущих сообщений от клиента в конце переписки остались без ответа менеджера — тот же
 * смысл, что у LeadsContext.unreadChatsCount, но как число на конкретный чат (для UnreadBadge в
 * ChatSwitcherPopover и на плашке ChatWindow.State=Minimized), а не общий признак «есть непрочитанное».
 */
export function trailingUnreadCount(messages: Lead['messages']): number {
  let count = 0
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].sender !== 'client') break
    count++
  }
  return count
}

/**
 * Список активных переписок для ChatSwitcherPopover — только лиды, где уже есть хоть одно сообщение,
 * свежие сверху. Общий источник для ModuleNav (ChatIconButton) и GlobalChatWindow (TitleBar самого окна) —
 * см. ds/components.md → ChatSwitcherPopover: «один и тот же компонент, два места вызова».
 */
export function buildChatSummaries(leads: Lead[]): ChatSummary[] {
  return leads
    .filter((l) => l.messages.length > 0)
    .slice()
    .sort((a, b) => b.lastContactAt - a.lastContactAt)
    .map((l) => {
      const last = l.messages[l.messages.length - 1]
      return {
        id: l.id,
        initials: initials(l.name),
        name: l.name,
        preview: last.message,
        time: formatRelativeTime(l.lastContactAt),
        unread: trailingUnreadCount(l.messages),
      }
    })
}
