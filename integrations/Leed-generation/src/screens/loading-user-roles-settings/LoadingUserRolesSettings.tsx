import { SettingsShell } from '../_shared/SettingsShell'
import { SkeletonBar } from '../_shared/SkeletonBar'

const ROW_WIDTHS = [1400, 1500, 1300, 1450, 1350]

export function LoadingUserRolesSettings() {
  return (
    <SettingsShell active="Роли и права">
      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Роли и права</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Управление доступом сотрудников
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <SkeletonBar width={1552} height={24} />
        {ROW_WIDTHS.map((w, i) => (
          <SkeletonBar key={i} width={w} height={44} />
        ))}
      </div>
    </SettingsShell>
  )
}
