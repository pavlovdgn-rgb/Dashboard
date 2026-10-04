import { StatusBadge, type StatusBadgeStatus } from '../../components/StatusBadge'
import { Table, type TableColumn } from '../../components/Table'
import { SettingsShell } from '../_shared/SettingsShell'

interface UserRow {
  name: string
  email: string
  role: string
  roleTone: StatusBadgeStatus
  date: string
}

const USERS: UserRow[] = [
  { name: 'Игорь Петров', email: 'igor@company.ru', role: 'Менеджер', roleTone: 'neutral', date: '12.03.2026' },
  { name: 'Анна Смирнова', email: 'anna@company.ru', role: 'Менеджер', roleTone: 'neutral', date: '15.03.2026' },
  { name: 'Дмитрий Волков', email: 'dmitry@company.ru', role: 'Менеджер', roleTone: 'neutral', date: '15.03.2026' },
  { name: 'Марина Кузнецова', email: 'marina@company.ru', role: 'Руководитель', roleTone: 'success', date: '01.03.2026' },
  { name: 'Сергей Орлов', email: 'sergey@company.ru', role: 'Администратор', roleTone: 'warning', date: '01.03.2026' },
]

const COLUMNS: TableColumn[] = [
  { key: 'name', label: 'Имя', width: 280 },
  { key: 'email', label: 'Email', width: 'fill' },
  { key: 'role', label: 'Роль', width: 200 },
  { key: 'date', label: 'Дата добавления', width: 160 },
]

export function UserRolesSettings() {
  const rows = USERS.map((u) => ({
    name: u.name,
    email: u.email,
    role: <StatusBadge status={u.roleTone}>{u.role}</StatusBadge>,
    date: u.date,
  }))

  return (
    <SettingsShell active="Роли и права">
      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Роли и права</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Управление доступом сотрудников
        </div>
      </div>
      <Table columns={COLUMNS} rows={rows} />
    </SettingsShell>
  )
}
