import type { ReactNode } from 'react'

export interface EmptyStateProps {
  icon: ReactNode
  title: string
  body: string
  action?: ReactNode
}

/** Центрированный empty-state блок, переиспользуется во всех empty-состояниях таблиц/списков. */
export function EmptyState({ icon, title, body, action }: EmptyStateProps) {
  return (
    <div style={{ display: 'flex', flex: '1 1 0%', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 'var(--space-lg)', width: 480 }}>
        <div style={{ color: 'var(--color-text-icons)', display: 'flex' }}>{icon}</div>
        <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)', textAlign: 'center' }}>{title}</span>
        <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', textAlign: 'center' }}>{body}</span>
        {action}
      </div>
    </div>
  )
}
