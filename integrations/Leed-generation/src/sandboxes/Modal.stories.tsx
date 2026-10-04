import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button } from '../components/Button'
import { IconButton } from '../components/IconButton'
import { Input } from '../components/Input'
import { Radio } from '../components/Radio'
import { StatusBadge } from '../components/StatusBadge'

function CloseIcon() {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M4 4L12 12M12 4L4 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

/** Модальное окно — реальная композиция CallLogModal: заголовок с close, Radio-направление, Input, StatusBadge, Secondary+Primary в футере. */
function CallLogModalDemo() {
  const [direction, setDirection] = useState<'in' | 'out'>('out')
  const [comment, setComment] = useState('')

  return (
    <div style={{ width: 480, background: 'var(--color-bg-surface-primary)', borderRadius: 'var(--radius-sm)', boxShadow: 'var(--shadow-lg)' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottom: '1px solid var(--color-border-default)' }}>
        <span className="ds-desktop-header-2-medium">Записать звонок</span>
        <IconButton icon={<CloseIcon />} aria-label="Закрыть" />
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, padding: 16 }}>
        <div>
          <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)', display: 'block', marginBottom: 8 }}>
            Направление
          </span>
          <div style={{ display: 'flex', gap: 24 }}>
            <Radio selected={direction === 'in'} onChange={() => setDirection('in')} label="Входящий" name="direction" />
            <Radio selected={direction === 'out'} onChange={() => setDirection('out')} label="Исходящий" name="direction" />
          </div>
        </div>
        <Input label="Комментарий" type="textarea" value={comment} onChange={setComment} placeholder="Например: обсудили условия поставки, попросил прислать КП" />
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
            Статус звонка:
          </span>
          <StatusBadge status="success">Успешно</StatusBadge>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12, padding: 16, borderTop: '1px solid var(--color-border-default)' }}>
        <Button variant="secondary">Отмена</Button>
        <Button variant="primary">Сохранить</Button>
      </div>
    </div>
  )
}

const meta = {
  title: 'Sandboxes/Модальное окно',
  parameters: { layout: 'centered' },
} satisfies Meta<typeof CallLogModalDemo>
export default meta

type Story = StoryObj<typeof meta>

/** Реальные компоненты базы, собранные вместе — как CallLogModal в продукте. */
export const CallLogModal: Story = { render: () => <CallLogModalDemo /> }
