import { Checkbox } from '../../components/Checkbox'
import { StatusBadge } from '../../components/StatusBadge'
import { Table, type TableColumn } from '../../components/Table'
import { useChatWindow } from '../../data/ChatWindowContext'
import { useLeads } from '../../data/LeadsContext'
import { STATUS_LABEL, STATUS_TONE } from '../../data/types'
import { CHANNEL_LABEL } from '../../data/types'
import { formatRelativeTime } from '../../data/format'
import { AppShell } from '../_shared/AppShell'
import { EmptyState } from '../_shared/EmptyState'
import { InteractionBlocker } from '../_shared/InteractionBlocker'
import { LeadCardPanel } from '../_shared/LeadCardPanel'
import { ModuleNav } from '../_shared/ModuleNav'
import { NewLeadModal } from '../_shared/NewLeadModal'
import { SkeletonBar } from '../_shared/SkeletonBar'
import { NoMessageIcon } from '../_shared/icons'
import { TextButton } from '../../components/TextButton'
import { useLeadFilters } from '../_shared/useLeadFilters'
import { useLeadOverlay } from '../_shared/useLeadOverlay'
import { useSimulatedLoading } from '../_shared/useSimulatedLoading'
import { useState } from 'react'
import { LeadsFiltersBar } from './parts/LeadsFiltersBar'

const COLUMNS: TableColumn[] = [
  { key: 'checkbox', label: '', width: 40, headerType: 'checkbox' },
  { key: 'channel', label: 'Канал', width: 120 },
  { key: 'nameCompany', label: 'Имя и компания', width: 'fill' },
  { key: 'score', label: 'Скор', width: 90 },
  { key: 'status', label: 'Статус', width: 200 },
  { key: 'lastContact', label: 'Последний контакт', width: 200 },
  { key: 'owner', label: 'Ответственный', width: 200 },
]

const SKELETON_WIDTHS = [900, 700, 850, 600, 780, 650]

export function LeadsTable() {
  const { leads, overdueCount, getLead } = useLeads()
  const { openChat } = useChatWindow()
  const filters = useLeadFilters(leads)
  const loading = useSimulatedLoading()
  const [newLeadOpen, setNewLeadOpen] = useState(false)
  const { overlay, openCard, close } = useLeadOverlay()
  const overlayLead = overlay ? getLead(overlay.leadId) : null

  const rows = filters.filtered.map((lead) => ({
    checkbox: (
      <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }} onClick={(e) => e.stopPropagation()}>
        <Checkbox checked={false} />
      </div>
    ),
    channel: CHANNEL_LABEL[lead.channel],
    nameCompany: `${lead.name}, ${lead.company}`,
    score: lead.score,
    status: (
      <StatusBadge status={lead.overdue ? 'error' : STATUS_TONE[lead.status]}>
        {lead.overdue ? `${STATUS_LABEL[lead.status]} · Просрочен` : STATUS_LABEL[lead.status]}
      </StatusBadge>
    ),
    lastContact: formatRelativeTime(lead.lastContactAt),
    owner: lead.owner ?? 'не назначен',
  }))

  return (
    <AppShell>
      <ModuleNav badge={{ label: `${overdueCount} просрочено`, status: overdueCount > 0 ? 'warning' : 'success' }} />
      <LeadsFiltersBar
        search={filters.search}
        onSearchChange={filters.setSearch}
        channel={filters.channel}
        onChannelChange={filters.setChannel}
        owner={filters.owner}
        onOwnerChange={filters.setOwner}
        onReset={filters.reset}
        onNewLead={() => setNewLeadOpen(true)}
      />

      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
          {SKELETON_WIDTHS.map((w, i) => (
            <SkeletonBar key={i} width={w} height={32} />
          ))}
        </div>
      ) : filters.filtered.length === 0 ? (
        filters.isFiltered ? (
          <EmptyState
            icon={<NoMessageIcon />}
            title="Ничего не найдено"
            body="Попробуйте изменить запрос или сбросить фильтры"
            action={<TextButton onClick={filters.reset}>Сбросить фильтры</TextButton>}
          />
        ) : (
          <EmptyState
            icon={<NoMessageIcon />}
            title="Лидов пока нет"
            body="Заявки из формы, звонка и чата появятся здесь автоматически, как только придут первые обращения"
          />
        )
      ) : (
        <div style={{ padding: 'var(--space-xl)', overflowX: 'auto' }}>
          <Table
            columns={COLUMNS}
            rows={rows}
            onRowClick={(i) => openCard(filters.filtered[i].id)}
            rowDataTrack="lead-row"
          />
        </div>
      )}

      {newLeadOpen && <NewLeadModal onClose={() => setNewLeadOpen(false)} />}
      {overlayLead && (
        <>
          <InteractionBlocker />
          <LeadCardPanel lead={overlayLead} onClose={close} onWriteChat={() => openChat(overlayLead.id)} />
        </>
      )}
    </AppShell>
  )
}
