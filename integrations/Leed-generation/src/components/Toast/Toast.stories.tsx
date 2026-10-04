import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button } from '../Button'
import { Toast } from './Toast'

/** Toast — всплывающее уведомление о результате действия. Status: success|error|warning|info. */
const meta = {
  title: 'Components/Toast',
  component: Toast,
  tags: ['autodocs'],
  args: { status: 'success', children: 'Провайдер подключён' },
  argTypes: {
    status: { control: 'inline-radio', options: ['success', 'error', 'warning', 'info'] },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Toast>
export default meta

type Story = StoryObj<typeof meta>

export const Success: Story = { args: { status: 'success', children: 'Провайдер подключён' } }
export const Error: Story = { args: { status: 'error', children: 'Не удалось сохранить' } }
export const Warning: Story = { args: { status: 'warning', children: 'Проверьте данные' } }
export const Info: Story = { args: { status: 'info', children: 'Изменения сохранены автоматически' } }

/** Все 4 статуса рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'flex-start' }}>
      <Toast status="success">Провайдер подключён</Toast>
      <Toast status="error">Не удалось сохранить</Toast>
      <Toast status="warning">Проверьте данные</Toast>
      <Toast status="info">Изменения сохранены автоматически</Toast>
    </div>
  ),
}

/** Длинное сообщение — переносится по словам, не растягивает toast бесконечно (max-width 360px). */
export const LongMessage: Story = {
  args: {
    status: 'error',
    children: 'Не удалось сохранить звонок: сервер телефонии не ответил за 30 секунд, проверьте подключение и попробуйте ещё раз чуть позже',
  },
}

/** Несколько уведомлений сразу — стек, как при пачке событий подряд. */
export const Stacked: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, alignItems: 'flex-start' }}>
      <Toast status="success">Лид «Иванов Пётр» назначен на Игоря Петрова</Toast>
      <Toast status="success">Лид «Соколова Анна» переведён в «В работе»</Toast>
      <Toast status="warning">3 лида без ответа больше суток</Toast>
    </div>
  ),
}

/** Микро-анимация появления (slide-down + fade, ~220ms) — нажмите «Показать», чтобы увидеть live. */
export const AppearanceDemo: Story = {
  parameters: { layout: 'padded' },
  render: () => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [key, setKey] = useState(0)
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [visible, setVisible] = useState(true)
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, alignItems: 'flex-start' }}>
        <Button
          variant="secondary"
          size="s"
          onClick={() => {
            setVisible(false)
            setTimeout(() => {
              setKey((k) => k + 1)
              setVisible(true)
            }, 50)
          }}
        >
          Показать снова
        </Button>
        <div style={{ minHeight: 44 }}>{visible && <Toast key={key} status="success">Провайдер подключён</Toast>}</div>
      </div>
    )
  },
}
