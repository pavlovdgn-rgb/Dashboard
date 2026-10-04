import { useNavigate } from 'react-router-dom'
import { useChatWindow } from '../../data/ChatWindowContext'
import { InteractionBlocker } from '../_shared/InteractionBlocker'
import { LeadCardPanel } from '../_shared/LeadCardPanel'
import { useSelectedLead } from '../_shared/useSelectedLead'
import { LeadsKanban } from '../leads-kanban/LeadsKanban'

/** Standalone route (реестр экранов) — карточка поверх Канбана, лид по умолчанию (или из location.state, если пришли по ссылке).
 *  «Написать в чат» открывает глобальное плавающее окно (ChatWindowContext) — тот же вход, что и из ModuleNav/LeadsKanban,
 *  не локальный ChatOverlay (устарел вместе с докнутым паттерном, см. ds/components.md → ChatWindow). */
export function LeadCard() {
  const navigate = useNavigate()
  const lead = useSelectedLead('lead-4')
  const { openChat } = useChatWindow()

  return (
    <div style={{ position: 'relative' }}>
      <LeadsKanban />
      <InteractionBlocker />
      <LeadCardPanel lead={lead} onClose={() => navigate('/leads-kanban')} onWriteChat={() => openChat(lead.id)} />
    </div>
  )
}
