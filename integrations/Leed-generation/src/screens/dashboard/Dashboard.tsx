import { useState } from 'react'
import { FunnelBar } from '../../components/FunnelBar'
import { MetricCard } from '../../components/MetricCard'
import { Table, type TableColumn } from '../../components/Table'
import { useLeads } from '../../data/LeadsContext'
import { DASHBOARD_FUNNEL, DASHBOARD_FUNNEL_MAX, DASHBOARD_METRICS, DASHBOARD_TEAM } from '../../data/dashboardStats'
import { AppShell } from '../_shared/AppShell'
import { ModuleNav } from '../_shared/ModuleNav'
import { NewLeadModal } from '../_shared/NewLeadModal'
import { SkeletonBar } from '../_shared/SkeletonBar'
import { useLeadFilters } from '../_shared/useLeadFilters'
import { useSimulatedLoading } from '../_shared/useSimulatedLoading'
import { LeadsFiltersBar } from '../leads-table/parts/LeadsFiltersBar'

const TEAM_COLUMNS: TableColumn[] = [
  { key: 'manager', label: 'Менеджер', width: 440 },
  { key: 'inProgress', label: 'Лидов в работе', width: 320 },
  { key: 'conversion', label: 'Конверсия', width: 300 },
  { key: 'overdue', label: 'Просрочено', width: 296 },
]

export function Dashboard() {
  const { leads, overdueCount } = useLeads()
  const filters = useLeadFilters(leads)
  const loading = useSimulatedLoading()
  const [newLeadOpen, setNewLeadOpen] = useState(false)

  const filteredOverdue = filters.filtered.filter((l) => l.overdue).length

  const metrics = [
    DASHBOARD_METRICS[0],
    DASHBOARD_METRICS[1],
    { label: 'Просроченные лиды', value: String(filteredOverdue), caption: 'требуют внимания', trend: filteredOverdue > 0 ? ('negative' as const) : ('positive' as const) },
    DASHBOARD_METRICS[2],
  ]

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
        <>
          <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
            {[0, 1, 2, 3].map((i) => (
              <div key={i} style={{ flex: 1 }}>
                <SkeletonBar width="100%" height={92} radius="var(--radius-focus)" />
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, padding: 'var(--space-xl)', width: '100%' }}>
            <SkeletonBar width={280} height={20} />
            {[740, 620, 320, 420, 140].map((w, i) => (
              <SkeletonBar key={i} width={w} height={28} />
            ))}
          </div>
        </>
      ) : (
        <>
          <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)', flexWrap: 'wrap' }}>
            {metrics.map((metric) => (
              <div key={metric.label} style={{ flex: '1 1 200px', minWidth: 200 }}>
                <MetricCard label={metric.label} value={metric.value} caption={metric.caption} trend={metric.trend} />
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)', padding: 'var(--space-xl)', width: '100%' }}>
            <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
              Воронка лидов по статусам
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)', width: '100%', maxWidth: 760 }}>
              {DASHBOARD_FUNNEL.map((stage) => (
                <FunnelBar key={stage.label} label={stage.label} value={stage.value} percent={(stage.value / DASHBOARD_FUNNEL_MAX) * 100} tone={stage.tone} />
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)', padding: 'var(--space-xl)', width: '100%' }}>
            <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
              Нагрузка команды
            </span>
            <div style={{ width: 'fit-content' }}>
              <Table columns={TEAM_COLUMNS} rows={DASHBOARD_TEAM} />
            </div>
          </div>
        </>
      )}

      {newLeadOpen && <NewLeadModal onClose={() => setNewLeadOpen(false)} />}
    </AppShell>
  )
}
