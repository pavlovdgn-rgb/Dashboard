import { useEffect } from 'react'
import { useChatWindow } from '../../data/ChatWindowContext'
import { useSelectedLead } from '../_shared/useSelectedLead'
import { LeadsKanban } from '../leads-kanban/LeadsKanban'

/**
 * Standalone route (реестр экранов) — демонстрация плавающего ChatWindow поверх Канбана: раньше здесь
 * была докнутая ChatOverlay (585+480px), устаревший паттерн (см. ds/components.md → ChatWindow, архив
 * Screen/ChatPanel в Figma). Открывает глобальное окно чата для лида по умолчанию сразу при заходе —
 * тот же ChatWindowContext, что и в реальном приложении, не локальная копия состояния.
 */
export function ChatPanel() {
  const lead = useSelectedLead('lead-2')
  const { openChat } = useChatWindow()

  useEffect(() => {
    openChat(lead.id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lead.id])

  return <LeadsKanban />
}
