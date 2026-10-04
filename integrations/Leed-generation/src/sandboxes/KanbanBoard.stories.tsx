import { useState, type CSSProperties, type DragEvent } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { KanbanCard, type KanbanCardProps } from '../components/KanbanCard'

interface Lead extends KanbanCardProps {
  id: string
}

type ColumnId = 'new' | 'in-progress' | 'callback' | 'qualified' | 'not-fit'

const COLUMN_LABELS: Record<ColumnId, string> = {
  new: 'Новый',
  'in-progress': 'В работе',
  callback: 'Перезвонить',
  qualified: 'Квалифицирован',
  'not-fit': 'Не подходит',
}

const COLUMN_ORDER: ColumnId[] = ['new', 'in-progress', 'callback', 'qualified', 'not-fit']

const INITIAL_LEADS: Record<ColumnId, Lead[]> = {
  new: [
    { id: 'l1', channel: 'Форма', nameCompany: 'Иванов Пётр, Ленинградский зоопарк', score: 82, timeText: '12 мин назад', managerName: 'Игорь Петров', managerInitials: 'ИП' },
    { id: 'l2', channel: 'Чат', nameCompany: 'Дмитриев Олег, Петропавловская крепость', score: 91, timeText: '40 мин назад' },
  ],
  'in-progress': [
    { id: 'l3', channel: 'Звонок', nameCompany: 'Соколова Анна, Музей петербургского авангарда', score: 65, timeText: '3 часа назад', managerName: 'Игорь Петров', managerInitials: 'ИП' },
  ],
  callback: [
    { id: 'l4', channel: 'Форма', nameCompany: 'Кузнецова Мария, ГМИИ им. А.С. Пушкина', score: 45, timeText: '1 день назад — Просрочен', managerName: 'Игорь Петров', managerInitials: 'ИП', overdue: true },
  ],
  qualified: [],
  'not-fit': [],
}

const COLUMN_STYLE: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
  width: 340,
  flexShrink: 0,
  padding: '8px 0',
  borderRadius: 'var(--radius-sm)',
  background: 'var(--color-bg-page)',
  minHeight: 120,
}

/**
 * Канбан-доска — реальные `KanbanCard` в 5 колонках LeadsKanban, с перетаскиванием между колонками
 * (нативный HTML5 Drag and Drop, без сторонней библиотеки). Захватите карточку за любое место и перетащите
 * в другую колонку — статус лида (и визуально, и в состоянии этой истории) обновится.
 */
function KanbanBoardDemo() {
  const [columns, setColumns] = useState(INITIAL_LEADS)
  const [draggedFrom, setDraggedFrom] = useState<ColumnId | null>(null)
  const [draggedId, setDraggedId] = useState<string | null>(null)
  const [dragOverColumn, setDragOverColumn] = useState<ColumnId | null>(null)

  function handleDragStart(columnId: ColumnId, leadId: string) {
    setDraggedFrom(columnId)
    setDraggedId(leadId)
  }

  function handleDragOver(e: DragEvent<HTMLDivElement>, columnId: ColumnId) {
    e.preventDefault()
    setDragOverColumn(columnId)
  }

  function handleDrop(targetColumn: ColumnId) {
    if (!draggedFrom || !draggedId || draggedFrom === targetColumn) {
      setDraggedFrom(null)
      setDraggedId(null)
      setDragOverColumn(null)
      return
    }
    setColumns((prev) => {
      const lead = prev[draggedFrom].find((l) => l.id === draggedId)
      if (!lead) return prev
      return {
        ...prev,
        [draggedFrom]: prev[draggedFrom].filter((l) => l.id !== draggedId),
        [targetColumn]: [...prev[targetColumn], lead],
      }
    })
    setDraggedFrom(null)
    setDraggedId(null)
    setDragOverColumn(null)
  }

  return (
    <div style={{ display: 'flex', gap: 16, padding: 16, alignItems: 'flex-start' }}>
      {COLUMN_ORDER.map((columnId) => (
        <div
          key={columnId}
          style={{
            ...COLUMN_STYLE,
            outline: dragOverColumn === columnId && draggedFrom !== columnId ? '2px dashed var(--color-brand-primary)' : 'none',
            outlineOffset: -2,
          }}
          onDragOver={(e) => handleDragOver(e, columnId)}
          onDragLeave={() => setDragOverColumn((c) => (c === columnId ? null : c))}
          onDrop={() => handleDrop(columnId)}
        >
          <span className="ds-desktop-main-semibold" style={{ padding: '4px 4px 8px' }}>
            {COLUMN_LABELS[columnId]} ({columns[columnId].length})
          </span>
          {columns[columnId].length === 0 && (
            <div style={{ padding: '24px 8px', textAlign: 'center' }} className="ds-desktop-main-regular">
              <span style={{ color: 'var(--color-text-secondary)' }}>Нет лидов в этом статусе</span>
            </div>
          )}
          {columns[columnId].map((lead) => (
            <div
              key={lead.id}
              draggable
              onDragStart={() => handleDragStart(columnId, lead.id)}
              onDragEnd={() => {
                setDraggedFrom(null)
                setDraggedId(null)
                setDragOverColumn(null)
              }}
              style={{
                cursor: 'grab',
                opacity: draggedId === lead.id ? 0.4 : 1,
                width: '100%',
              }}
            >
              <KanbanCard {...lead} />
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

const meta = {
  title: 'Sandboxes/Канбан-доска',
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof KanbanBoardDemo>
export default meta

type Story = StoryObj<typeof meta>

/** Захватите карточку и перетащите в другую колонку — реальный drag and drop, состояние обновляется живьём. */
export const DragAndDrop: Story = { render: () => <KanbanBoardDemo /> }
