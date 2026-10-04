import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '../../components/Button'
import { TextButton } from '../../components/TextButton'
import { useLeads } from '../../data/LeadsContext'
import { useToast } from '../../data/ToastContext'
import { LeadsTable } from '../leads-table/LeadsTable'
import { CallLogModalContent } from '../_shared/CallLogModalContent'

const CALLER_LEAD_ID = 'lead-6'

export function IncomingCallPopup() {
  const navigate = useNavigate()
  const { getLead } = useLeads()
  const { showToast } = useToast()
  const [visible, setVisible] = useState(true)
  const [answering, setAnswering] = useState(false)
  const lead = getLead(CALLER_LEAD_ID)

  if (!lead) return <LeadsTable />

  return (
    <div style={{ position: 'relative' }}>
      <LeadsTable />

      {visible && (
        <div
          style={{
            position: 'fixed',
            top: 'var(--space-xl)',
            right: 'var(--space-xl)',
            width: 360,
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-md)',
            background: 'var(--color-bg-surface-primary)',
            borderRadius: 'var(--radius-sm)',
            boxShadow: 'var(--shadow-md)',
            padding: 'var(--space-lg)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
            <span style={{ width: 20, height: 20, borderRadius: 'var(--radius-full)', background: 'var(--color-extra-blue-30)', flexShrink: 0 }} />
            <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>
              Входящий звонок
            </span>
          </div>
          <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
            {lead.name}, «{lead.company}»
          </span>
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
            {lead.phone}
          </span>
          <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
            <Button onClick={() => setAnswering(true)}>Ответить</Button>
            <TextButton
              onClick={() => {
                setVisible(false)
                showToast('warning', 'Звонок отклонён')
              }}
            >
              Отклонить
            </TextButton>
          </div>
          <TextButton onClick={() => navigate('/lead-card', { state: { leadId: lead.id } })}>Открыть карточку лида →</TextButton>
        </div>
      )}

      {answering && (
        <CallLogModalContent
          lead={lead}
          initialDirection="in"
          onClose={() => {
            setAnswering(false)
            setVisible(false)
          }}
        />
      )}
    </div>
  )
}
