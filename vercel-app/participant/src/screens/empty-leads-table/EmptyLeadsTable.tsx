import { AppShell } from '../_shared/AppShell'
import { EmptyState } from '../_shared/EmptyState'
import { ModuleNav } from '../_shared/ModuleNav'
import { NoMessageIcon } from '../_shared/icons'
import { LeadsFiltersBar } from '../leads-table/parts/LeadsFiltersBar'

export function EmptyLeadsTable() {
  return (
    <AppShell>
      <ModuleNav badge={{ label: '3 просрочено', status: 'warning' }} unreadCount={3} />
      <LeadsFiltersBar />
      <EmptyState
        icon={<NoMessageIcon />}
        title="Лидов пока нет"
        body="Заявки из формы, звонка и чата появятся здесь автоматически, как только придут первые обращения"
      />
    </AppShell>
  )
}
