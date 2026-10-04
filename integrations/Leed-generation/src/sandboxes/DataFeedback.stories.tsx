import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Info } from 'lucide-react'
import { Button } from '../components/Button'
import { StatusBadge } from '../components/StatusBadge'
import { Table } from '../components/Table'
import { Toast } from '../components/Toast'
import { Tooltip } from '../components/Tooltip'

const COLUMNS = [
  { key: 'name', label: 'Имя и компания', width: 'fill' as const },
  { key: 'score', label: 'Скор', width: 90 },
  { key: 'status', label: 'Статус', width: 160 },
]

const ROWS = [
  { name: 'Иванов Пётр, Ленинградский зоопарк', score: '82', status: <StatusBadge status="neutral">Новый</StatusBadge> },
  { name: 'Соколова Анна, Музей петербургского авангарда', score: '65', status: <StatusBadge status="warning">В работе</StatusBadge> },
  { name: 'Кузнецова Мария, ГМИИ им. А.С. Пушкина', score: '45', status: <StatusBadge status="error">Перезвонить</StatusBadge> },
]

/** Данные/обратная связь — Table + Toast (по действию) + Tooltip (подсказка у колонки «Скор»). */
function DataFeedbackDemo() {
  const [toastVisible, setToastVisible] = useState(false)

  return (
    <div style={{ width: 640, position: 'relative' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="ds-desktop-header-2-medium">Лиды</span>
          <Tooltip content="Скор считается по активности и полноте данных лида" position="top">
            <span style={{ display: 'inline-flex', color: 'var(--color-text-icons)', cursor: 'help' }}>
              <Info size={14} />
            </span>
          </Tooltip>
        </div>
        <Button variant="secondary" size="s" onClick={() => setToastVisible(true)}>
          Обновить
        </Button>
      </div>
      <Table columns={COLUMNS} rows={ROWS} />
      {toastVisible && (
        <div style={{ position: 'absolute', top: -8, right: 0 }}>
          <Toast status="success">Список лидов обновлён</Toast>
        </div>
      )}
    </div>
  )
}

const meta = {
  title: 'Sandboxes/Данные и обратная связь',
  parameters: { layout: 'centered' },
} satisfies Meta<typeof DataFeedbackDemo>
export default meta

type Story = StoryObj<typeof meta>

/** Table + Toast + Tooltip — нажмите «Обновить», чтобы увидеть Toast; наведите на иконку у «Лиды», чтобы увидеть Tooltip. */
export const DataAndFeedback: Story = { render: () => <DataFeedbackDemo /> }
