import { AppShell } from '../_shared/AppShell'
import { ModuleNav } from '../_shared/ModuleNav'
import { SkeletonBar } from '../_shared/SkeletonBar'
import { LeadsFiltersBar } from '../leads-table/parts/LeadsFiltersBar'

const FUNNEL_WIDTHS = [740, 620, 320, 420, 140]
const TEAM_WIDTHS = [1792, 1650, 1720, 1580]

export function LoadingDashboard() {
  return (
    <AppShell>
      <ModuleNav badge={{ label: '3 просрочено', status: 'warning' }} unreadCount={3} />
      <LeadsFiltersBar />

      <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
        {[0, 1, 2, 3].map((i) => (
          <div key={i} style={{ flex: 1 }}>
            <SkeletonBar width="100%" height={92} radius="var(--radius-focus)" />
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, padding: 'var(--space-xl)', width: '100%' }}>
        <SkeletonBar width={280} height={20} />
        {FUNNEL_WIDTHS.map((w, i) => (
          <SkeletonBar key={i} width={w} height={28} />
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, padding: 'var(--space-xl)', width: '100%' }}>
        <SkeletonBar width={240} height={20} />
        {TEAM_WIDTHS.map((w, i) => (
          <SkeletonBar key={i} width={w} height={32} />
        ))}
      </div>
    </AppShell>
  )
}
