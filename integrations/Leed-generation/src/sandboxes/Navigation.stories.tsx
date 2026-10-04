import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Breadcrumb } from '../components/Breadcrumb'
import { Pagination } from '../components/Pagination'
import { Tabs } from '../components/Tabs'

/** Навигация — Tabs + Breadcrumb + Pagination в одном контексте. */
function NavigationDemo() {
  const [tab, setTab] = useState<'list' | 'kanban'>('list')
  const [page, setPage] = useState(1)

  return (
    <div style={{ width: 560, display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <div style={{ display: 'flex', gap: 8, marginBottom: 8, fontFamily: 'var(--font-sans)', fontSize: 12, color: 'var(--color-text-secondary)' }}>
          <Breadcrumb>Настройки</Breadcrumb>
          <span>/</span>
          <Breadcrumb current>Роли и права</Breadcrumb>
        </div>
        <div style={{ display: 'flex', gap: 4, borderBottom: '1px solid var(--color-border-default)' }}>
          <Tabs active={tab === 'list'} onClick={() => setTab('list')}>Список</Tabs>
          <Tabs active={tab === 'kanban'} onClick={() => setTab('kanban')}>Канбан</Tabs>
        </div>
      </div>
      <div style={{ padding: 16, background: 'var(--color-bg-hover-subtle)', borderRadius: 'var(--radius-sm)', fontFamily: 'var(--font-sans)', fontSize: 13, color: 'var(--color-text-secondary)' }}>
        Активная вкладка: {tab === 'list' ? 'Список' : 'Канбан'}
      </div>
      <div style={{ display: 'flex', gap: 4 }}>
        <Pagination icon={<ChevronLeft size={14} />} disabled={page === 1} onClick={() => setPage((p) => Math.max(1, p - 1))} />
        {[1, 2, 3, 4].map((p) => (
          <Pagination key={p} active={page === p} onClick={() => setPage(p)}>
            {p}
          </Pagination>
        ))}
        <Pagination icon={<ChevronRight size={14} />} onClick={() => setPage((p) => Math.min(4, p + 1))} />
      </div>
    </div>
  )
}

const meta = {
  title: 'Sandboxes/Навигация',
  parameters: { layout: 'centered' },
} satisfies Meta<typeof NavigationDemo>
export default meta

type Story = StoryObj<typeof meta>

/** Breadcrumb + Tabs + Pagination — все живые, реагируют на клик. */
export const NavigationBlock: Story = { render: () => <NavigationDemo /> }
