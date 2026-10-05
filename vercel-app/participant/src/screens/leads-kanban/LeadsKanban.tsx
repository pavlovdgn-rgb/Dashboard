import { useState, type DragEvent } from 'react'
import { KanbanCard } from '../../components/KanbanCard'
import { useChatWindow } from '../../data/ChatWindowContext'
import { useLeads } from '../../data/LeadsContext'
import { useToast } from '../../data/ToastContext'
import { formatRelativeTime } from '../../data/format'
import { STATUS_LABEL, type LeadStatus } from '../../data/types'
import { initials } from '../../data/leads'
import { AppShell } from '../_shared/AppShell'
import { InteractionBlocker } from '../_shared/InteractionBlocker'
import { LeadCardPanel } from '../_shared/LeadCardPanel'
import { ModuleNav } from '../_shared/ModuleNav'
import { NewLeadModal } from '../_shared/NewLeadModal'
import { SkeletonBar } from '../_shared/SkeletonBar'
import { useLeadFilters } from '../_shared/useLeadFilters'
import { useLeadOverlay } from '../_shared/useLeadOverlay'
import { useSimulatedLoading } from '../_shared/useSimulatedLoading'
import { LeadsFiltersBar } from '../leads-table/parts/LeadsFiltersBar'

const COLUMN_ORDER: LeadStatus[] = ['new', 'in_progress', 'callback', 'qualified', 'rejected']

export function LeadsKanban() {
  const { leads, overdueCount, updateStatus, getLead } = useLeads()
  const { openChat } = useChatWindow()
  const { showToast } = useToast()
  const filters = useLeadFilters(leads)
  const loading = useSimulatedLoading()
  const [newLeadOpen, setNewLeadOpen] = useState(false)
  const { overlay, openCard, close } = useLeadOverlay()
  const overlayLead = overlay ? getLead(overlay.leadId) : null

  // Drag and drop между колонками — тот же нативный HTML5 DnD, что в Storybook (Sandboxes/Канбан-доска),
  // здесь вызывает реальный updateStatus вместо локального demo-состояния.
  const [draggedId, setDraggedId] = useState<string | null>(null)
  const [draggedFromStatus, setDraggedFromStatus] = useState<LeadStatus | null>(null)
  const [dragOverStatus, setDragOverStatus] = useState<LeadStatus | null>(null)

  function handleDragOver(e: DragEvent<HTMLDivElement>, status: LeadStatus) {
    e.preventDefault()
    setDragOverStatus(status)
  }

  function handleDrop(targetStatus: LeadStatus) {
    if (draggedId && draggedFromStatus && draggedFromStatus !== targetStatus) {
      updateStatus(draggedId, targetStatus)
      showToast('success', `Статус обновлён: ${STATUS_LABEL[targetStatus]}`)
    }
    setDraggedId(null)
    setDraggedFromStatus(null)
    setDragOverStatus(null)
  }

  const columns = COLUMN_ORDER.map((status) => ({
    status,
    label: STATUS_LABEL[status],
    leads: filters.filtered.filter((l) => l.status === status),
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
        <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
          {COLUMN_ORDER.map((status) => (
            <div key={status} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)', width: 340, flexShrink: 0 }}>
              <SkeletonBar width={140} height={20} />
              <SkeletonBar width="100%" height={120} radius="var(--radius-sm)" />
              <SkeletonBar width="100%" height={120} radius="var(--radius-sm)" />
            </div>
          ))}
        </div>
      ) : (
        <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)', overflowX: 'auto', alignItems: 'flex-start' }}>
          {columns.map((column) => (
            <div
              key={column.status}
              onDragOver={(e) => handleDragOver(e, column.status)}
              onDragLeave={() => setDragOverStatus((s) => (s === column.status ? null : s))}
              onDrop={() => handleDrop(column.status)}
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 'var(--space-sm)',
                width: 340,
                flexShrink: 0,
                minHeight: 120,
                padding: 'var(--space-xs)',
                borderRadius: 'var(--radius-sm)',
                outline: dragOverStatus === column.status && draggedFromStatus !== column.status ? '2px dashed var(--color-brand-primary)' : 'none',
                outlineOffset: -2,
              }}
            >
              <span className="ds-desktop-main-semibold" style={{ color: 'var(--color-text-primary)' }}>
                {column.label} ({column.leads.length})
              </span>
              {column.leads.length === 0 ? (
                <div style={{ padding: 'var(--space-xl) 0', textAlign: 'center' }}>
                  <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
                    {filters.isFiltered ? 'Ничего не найдено' : 'Нет лидов в этом статусе'}
                  </span>
                </div>
              ) : (
                column.leads.map((lead) => (
                  <div
                    key={lead.id}
                    draggable
                    onDragStart={() => {
                      setDraggedId(lead.id)
                      setDraggedFromStatus(column.status)
                    }}
                    onDragEnd={() => {
                      setDraggedId(null)
                      setDraggedFromStatus(null)
                      setDragOverStatus(null)
                    }}
                    onClick={() => openCard(lead.id)}
                    data-track="lead-card"
                    style={{ cursor: draggedId === lead.id ? 'grabbing' : 'grab', opacity: draggedId === lead.id ? 0.4 : 1 }}
                  >
                    <KanbanCard
                      channel={lead.channel === 'form' ? 'Форма' : lead.channel === 'call' ? 'Звонок' : 'Чат'}
                      nameCompany={`${lead.name}, ${lead.company}`}
                      score={lead.score}
                      timeText={lead.overdue ? `${formatRelativeTime(lead.lastContactAt)} — Просрочен` : formatRelativeTime(lead.lastContactAt)}
                      managerName={lead.owner ?? undefined}
                      managerInitials={lead.owner ? initials(lead.owner) : undefined}
                      overdue={lead.overdue}
                    />
                  </div>
                ))
              )}
            </div>
          ))}
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
