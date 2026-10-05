import { useNavigate } from 'react-router-dom'
import { CallLogModalContent } from '../_shared/CallLogModalContent'
import { useSelectedLead } from '../_shared/useSelectedLead'

/** Route-обёртка над общей формой звонка (см. `CallLogModalContent`) — демо-лид по умолчанию совпадает с `screens/lead-card`. */
export function CallLogModal() {
  const navigate = useNavigate()
  const lead = useSelectedLead('lead-4')
  return <CallLogModalContent lead={lead} onClose={() => navigate('/leads-table')} />
}
