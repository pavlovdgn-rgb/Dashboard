import { useState } from 'react'

export type LeadOverlay = { leadId: string } | null

/**
 * Состояние slide-over карточки лида для LeadsTable/LeadsKanban — открывается локальным state поверх
 * текущего экрана, без navigate(). Раньше сюда же входил и чат (`kind: 'card' | 'chat'`, докнутая
 * ChatOverlay поверх этого же слота) — с переходом на плавающий ChatWindow чат стал отдельным глобальным
 * состоянием (см. ChatWindowContext), не завязанным на этот оверлей: карточка лида и окно чата теперь
 * независимы и могут быть открыты одновременно.
 */
export function useLeadOverlay() {
  const [overlay, setOverlay] = useState<LeadOverlay>(null)

  return {
    overlay,
    openCard: (leadId: string) => setOverlay({ leadId }),
    close: () => setOverlay(null),
  }
}
