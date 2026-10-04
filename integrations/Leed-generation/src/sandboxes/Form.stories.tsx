import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button } from '../components/Button'
import { Dropdown } from '../components/Dropdown'
import { Input } from '../components/Input'
import { TextButton } from '../components/TextButton'

/**
 * Форма — AutoAssignmentSettings-подобная композиция: Dropdown + Input + состояние ошибки + submit/cancel.
 * Dropdown, не нативный Select — у Select направление открытия решает браузер (может уйти вверх и перекрыть
 * заголовок формы), у Dropdown открытие вниз зафиксировано в CSS, всегда предсказуемо.
 */
function AssignmentFormDemo() {
  const [mode, setMode] = useState('По нагрузке')
  const [threshold, setThreshold] = useState('15')
  const [showError, setShowError] = useState(false)

  return (
    <div style={{ width: 420, display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div>
        <span className="ds-desktop-header-2-medium">Автоназначение лидов</span>
      </div>
      <div>
        <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)', display: 'block', marginBottom: 8 }}>
          Режим распределения
        </span>
        <Dropdown label={mode} options={['Round-robin', 'По нагрузке']} onSelect={setMode} />
      </div>
      <Input
        label="Порог (минут)"
        value={threshold}
        onChange={setThreshold}
        error={showError}
        showHint={showError}
        hint={showError ? 'Введите число от 1 до 120' : undefined}
      />
      <div style={{ display: 'flex', gap: 12 }}>
        <Button variant="primary" onClick={() => setShowError(Number.isNaN(Number(threshold)) || threshold === '')}>
          Сохранить
        </Button>
        <TextButton onClick={() => { setThreshold('15'); setShowError(false) }}>Сбросить</TextButton>
      </div>
    </div>
  )
}

const meta = {
  title: 'Sandboxes/Форма',
  parameters: { layout: 'centered' },
} satisfies Meta<typeof AssignmentFormDemo>
export default meta

type Story = StoryObj<typeof meta>

/** Select + Input + submit/cancel — попробуйте очистить поле «Порог» и нажать «Сохранить», чтобы увидеть состояние ошибки. */
export const AssignmentForm: Story = { render: () => <AssignmentFormDemo /> }
