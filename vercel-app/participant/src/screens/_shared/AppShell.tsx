import type { ReactNode } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Sidebar } from '../../components/Sidebar'
import { NAV_ITEMS } from './nav'

export interface AppShellProps {
  children: ReactNode
}

/**
 * Общий каркас продуктовых экранов: Sidebar (80px, флайаут навигации) на всю высоту экрана + контентная колонка.
 * Корень — FIXED 100vh (не minHeight): Sidebar должен оставаться на весь экран, как в макете Figma, даже когда
 * контент длиннее вьюпорта — тогда скроллится сама контентная колонка, а не вся страница.
 *
 * Навигация — здесь, в одном месте: пункты флайаута и их active-состояние считаются из текущего route
 * (`NAV_ITEMS`), клик — `navigate()`. Экраны больше не передают `sidebarItems` вручную (раньше был статичный
 * дефолт с «Лиды» активным всегда, независимо от реального экрана).
 */
export function AppShell({ children }: AppShellProps) {
  const location = useLocation()
  const navigate = useNavigate()

  const items = NAV_ITEMS.map((item) => ({ label: item.label, pinned: item.pinned, active: item.matches(location.pathname) }))

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', background: 'var(--color-bg-page)' }}>
      <Sidebar
        items={items}
        onSelect={(label) => {
          const target = NAV_ITEMS.find((item) => item.label === label)
          if (target) navigate(target.route)
        }}
      />
      <div style={{ display: 'flex', flexDirection: 'column', flex: '1 1 0%', minWidth: 0, minHeight: 0, overflowY: 'auto' }}>{children}</div>
    </div>
  )
}
