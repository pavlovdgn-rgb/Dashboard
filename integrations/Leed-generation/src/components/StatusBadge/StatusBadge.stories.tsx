import type { Meta, StoryObj } from '@storybook/react-vite'
import { StatusBadge } from './StatusBadge'

/** Status Badge — цветовая индикация состояния записи. Status: Success|Error|Warning|Neutral. Neutral рендерится синим, не серым (см. ds/components.md). */
const meta = {
  title: 'Components/StatusBadge',
  component: StatusBadge,
  tags: ['autodocs'],
  args: { status: 'neutral', children: 'Новый' },
  argTypes: {
    status: { control: 'inline-radio', options: ['success', 'error', 'warning', 'neutral'] },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof StatusBadge>
export default meta

type Story = StoryObj<typeof meta>

export const Success: Story = { args: { status: 'success', children: 'Квалифицирован' } }
export const ErrorStatus: Story = { args: { status: 'error', children: 'Перезвонить · Просрочен на 1 день' } }
export const Warning: Story = { args: { status: 'warning', children: 'В работе' } }
export const Neutral: Story = { args: { status: 'neutral', children: 'Новый' } }

/** Все 4 статуса рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 12 }}>
      <StatusBadge status="success">Квалифицирован</StatusBadge>
      <StatusBadge status="error">Перезвонить</StatusBadge>
      <StatusBadge status="warning">В работе</StatusBadge>
      <StatusBadge status="neutral">Новый</StatusBadge>
    </div>
  ),
}
