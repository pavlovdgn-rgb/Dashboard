import { AppShell } from '../_shared/AppShell'
import { ModuleNav } from '../_shared/ModuleNav'
import { SkeletonBar } from '../_shared/SkeletonBar'
import { LeadsFiltersBar } from '../leads-table/parts/LeadsFiltersBar'

const WIDTHS = [900, 700, 850, 600, 780, 650]

export function LoadingState() {
  return (
    <AppShell>
      <ModuleNav badge={{ label: '3 просрочено', status: 'warning' }} unreadCount={3} />
      <LeadsFiltersBar />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
        {WIDTHS.map((w, i) => (
          <SkeletonBar key={i} width={w} height={32} />
        ))}
      </div>
    </AppShell>
  )
}
