import type { ReactNode } from 'react'
import { AppShell } from './AppShell'
import { ModuleNav } from './ModuleNav'

export interface CenteredMessageScreenProps {
  icon: ReactNode
  iconColor?: string
  title: string
  body: string
  action?: ReactNode
  contentWidth?: number
}

/** Общий каркас AccessDenied/ErrorState/NotFound404: Sidebar + ModuleNav (без бейджа) + центрированный блок-сообщение. */
export function CenteredMessageScreen({ icon, iconColor = 'var(--color-text-icons)', title, body, action, contentWidth = 558 }: CenteredMessageScreenProps) {
  return (
    <AppShell>
      <ModuleNav userName="Игорь Петров" userInitials="ИП" />
      <div style={{ display: 'flex', flex: '1 1 0%', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 'var(--space-lg)', width: contentWidth }}>
          <div style={{ width: 160, height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center', color: iconColor }}>
            {icon}
          </div>
          <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>{title}</span>
          <span className="ds-desktop-regular-16" style={{ color: 'var(--color-text-secondary)', textAlign: 'center', width: '100%' }}>{body}</span>
          {action}
        </div>
      </div>
    </AppShell>
  )
}
