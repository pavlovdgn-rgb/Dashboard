import type { ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'
import { Tabs } from '../../components/Tabs'
import { AppShell } from './AppShell'
import { ModuleNav } from './ModuleNav'

const NAV_ITEMS = [
  { label: 'Роли и права', route: '/settings/roles' },
  { label: 'Автоназначение', route: '/settings/auto-assignment' },
  { label: 'Телефония', route: '/settings/telephony' },
  { label: 'Чат-виджет', route: '/settings/chat-widget' },
] as const
export type SettingsSection = (typeof NAV_ITEMS)[number]['label']

export interface SettingsShellProps {
  active: SettingsSection
  children: ReactNode
}

/**
 * Общая оболочка 4 settings-экранов: Sidebar + ModuleNav (без бейджа/CTA) + горизонтальный ряд Tabs
 * («Роли и права» / «Автоназначение» / «Телефония» / «Чат-виджет») + контент.
 * Обновлено по правке пользователя в Figma: вертикальный список SettingsSidebar (240px) заменён на
 * горизонтальный ряд настоящих `Tabs`-инстансов под ModuleNav — тот же паттерн, что раньше был
 * ViewToggle «Список/Канбан» на LeadsTable/LeadsKanban (см. `ds/screens/user-roles-settings.md`).
 */
export function SettingsShell({ active, children }: SettingsShellProps) {
  const navigate = useNavigate()
  return (
    <AppShell>
      <ModuleNav userName="Сергей Орлов" userInitials="СО" />
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-sm)',
          background: 'var(--color-bg-surface-primary)',
          borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
          width: '100%',
          padding: '0 var(--space-xl)',
          flexShrink: 0,
        }}
      >
        {NAV_ITEMS.map((item) => (
          <Tabs key={item.label} active={item.label === active} onClick={() => navigate(item.route)}>
            {item.label}
          </Tabs>
        ))}
      </div>
      <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)', padding: 'var(--space-xl)', flex: '1 1 0%', minWidth: 0, minHeight: 0, overflowY: 'auto' }}>
        {children}
      </div>
    </AppShell>
  )
}
