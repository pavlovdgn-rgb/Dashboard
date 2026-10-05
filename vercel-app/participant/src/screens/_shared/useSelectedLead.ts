import { useLocation } from 'react-router-dom'
import { useLeads } from '../../data/LeadsContext'
import type { Lead } from '../../data/types'

interface LocationState {
  leadId?: string
}

/**
 * Overlay-экраны (LeadCard/ChatPanel/CallLogModal) читают, какой лид открыт, из `location.state.leadId`
 * (проставляется навигацией из LeadsTable/LeadsKanban/IncomingCallPopup). Прямой заход по route без state
 * (например, из ScreensIndex) — показывает `defaultId`, чтобы демо-маршрут из реестра остался рабочим сам по себе.
 */
export function useSelectedLead(defaultId: string): Lead {
  const location = useLocation()
  const { getLead, leads } = useLeads()
  const state = location.state as LocationState | null
  const lead = getLead(state?.leadId ?? defaultId)
  return lead ?? leads[0]
}
