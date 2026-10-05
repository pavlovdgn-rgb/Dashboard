import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'

export type ChatWindowState = 'expanded' | 'minimized'

interface ChatWindowContextValue {
  /** null — окно закрыто, ничего не рендерится (см. GlobalChatWindow.tsx). */
  activeLeadId: string | null
  windowState: ChatWindowState
  /** Открывает чат с лидом (Expanded) — если окно уже открыто с другим лидом, просто подменяет содержимое,
   *  не плодит второе окно (см. ds/components.md → ChatSwitcherPopover). Вызывается из ChatIconButton
   *  в ModuleNav и из «Написать в чат» на LeadCardPanel. */
  openChat: (leadId: string) => void
  minimize: () => void
  expand: () => void
  closeChat: () => void
}

const ChatWindowContext = createContext<ChatWindowContextValue | null>(null)

/**
 * Глобальное состояние плавающего окна чата (ChatWindow) — одно окно на весь интерфейс. Провайдер стоит
 * в App.tsx выше <Routes>, поэтому переживает переход между разделами CRM (Лиды→Канбан→Дашборд→Настройки),
 * как и задумано дизайном (ds/components.md → ChatWindow: «персистентно между разделами»). Сам рендер
 * окна — в GlobalChatWindow.tsx, смонтирован один раз рядом с <Routes>.
 */
export function ChatWindowProvider({ children }: { children: ReactNode }) {
  const [activeLeadId, setActiveLeadId] = useState<string | null>(null)
  const [windowState, setWindowState] = useState<ChatWindowState>('expanded')

  const openChat = useCallback((leadId: string) => {
    setActiveLeadId(leadId)
    setWindowState('expanded')
  }, [])
  const minimize = useCallback(() => setWindowState('minimized'), [])
  const expand = useCallback(() => setWindowState('expanded'), [])
  const closeChat = useCallback(() => setActiveLeadId(null), [])

  const value = useMemo<ChatWindowContextValue>(
    () => ({ activeLeadId, windowState, openChat, minimize, expand, closeChat }),
    [activeLeadId, windowState, openChat, minimize, expand, closeChat],
  )

  return <ChatWindowContext.Provider value={value}>{children}</ChatWindowContext.Provider>
}

export function useChatWindow(): ChatWindowContextValue {
  const ctx = useContext(ChatWindowContext)
  if (!ctx) throw new Error('useChatWindow must be used within ChatWindowProvider')
  return ctx
}
