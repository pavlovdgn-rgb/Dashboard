import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Pagination } from './Pagination'

/** Скользящее окно номеров страниц вокруг текущей — та же логика, что у любого реального пагинатора с большим числом страниц. */
function getVisiblePages(current: number, total: number, windowSize: number): number[] {
  if (total <= windowSize) return Array.from({ length: total }, (_, i) => i + 1)
  let start = Math.max(1, current - Math.floor(windowSize / 2))
  const end = Math.min(total, start + windowSize - 1)
  start = Math.max(1, end - windowSize + 1)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
}

const TOTAL_PAGES = 12
const WINDOW_SIZE = 5

/** Рабочий пагинатор — клик по числу делает страницу активной, стрелки двигают текущую страницу и, если нужно, сдвигают окно видимых номеров (появляются новые ячейки). */
function InteractivePagination() {
  const [page, setPage] = useState(1)
  const visible = getVisiblePages(page, TOTAL_PAGES, WINDOW_SIZE)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'center' }}>
      <div style={{ display: 'flex', gap: 4 }}>
        <Pagination icon={<ChevronLeft size={14} />} disabled={page === 1} onClick={() => setPage((p) => Math.max(1, p - 1))} />
        {visible.map((p) => (
          <Pagination key={p} active={p === page} onClick={() => setPage(p)}>
            {p}
          </Pagination>
        ))}
        <Pagination icon={<ChevronRight size={14} />} disabled={page === TOTAL_PAGES} onClick={() => setPage((p) => Math.min(TOTAL_PAGES, p + 1))} />
      </div>
      <span className="ds-desktop-breadcrumbs-regular" style={{ color: 'var(--color-text-secondary)' }}>
        Страница {page} из {TOTAL_PAGES}
      </span>
    </div>
  )
}

/** Pagination — постраничная навигация. State: default|active|disabled. Prev/Next — тот же чип с icon вместо номера. */
const meta = {
  title: 'Components/Pagination',
  component: Pagination,
  tags: ['autodocs'],
  args: { active: false, disabled: false, children: '2' },
  argTypes: {
    active: { control: 'boolean' },
    disabled: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Pagination>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Active: Story = { args: { active: true, children: '1' } }
export const Disabled: Story = { args: { disabled: true, children: '4' } }

/** Полный ряд пагинации — Prev / номера / Next, статичный снимок состояний (сверка с Figma одним взглядом). */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 4 }}>
      <Pagination icon={<ChevronLeft size={14} />} />
      <Pagination active>1</Pagination>
      <Pagination>2</Pagination>
      <Pagination>3</Pagination>
      <Pagination disabled>4</Pagination>
      <Pagination icon={<ChevronRight size={14} />} />
    </div>
  ),
}

/**
 * Рабочий пагинатор — 12 страниц, окно видимости 5 номеров. Кликните по числу — страница станет активной.
 * Кликните по стрелке несколько раз подряд у края окна — старые номера уйдут, появятся новые ячейки с цифрами,
 * стрелки блокируются на первой/последней странице. Именно так это работает в реальном интерфейсе.
 */
export const Interactive: Story = {
  parameters: { layout: 'padded' },
  render: () => <InteractivePagination />,
}
