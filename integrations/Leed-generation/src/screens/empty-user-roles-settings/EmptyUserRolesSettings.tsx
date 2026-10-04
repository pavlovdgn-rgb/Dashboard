import { SettingsShell } from '../_shared/SettingsShell'
import { EmptyState } from '../_shared/EmptyState'
import { NoMessageIcon } from '../_shared/icons'

export function EmptyUserRolesSettings() {
  return (
    <SettingsShell active="Роли и права">
      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Роли и права</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Управление доступом сотрудников
        </div>
      </div>
      <EmptyState icon={<NoMessageIcon />} title="Пока нет сотрудников" body="Сотрудники появятся здесь, как только будут добавлены в систему" />
    </SettingsShell>
  )
}
