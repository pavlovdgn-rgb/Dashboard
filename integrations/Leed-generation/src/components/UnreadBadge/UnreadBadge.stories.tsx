import type { Meta, StoryObj } from '@storybook/react-vite'
import { UnreadBadge } from './UnreadBadge'

/** UnreadBadge — счётчик непрочитанных сообщений чата. Size: Sm|Md. count<=0 не рендерится (счётчику нечего показывать). */
const meta = {
  title: 'Components/UnreadBadge',
  component: UnreadBadge,
  tags: ['autodocs'],
  args: { size: 'sm', count: 3 },
  argTypes: {
    size: { control: 'inline-radio', options: ['sm', 'md'] },
    count: { control: 'number' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof UnreadBadge>
export default meta

type Story = StoryObj<typeof meta>

export const Small: Story = { args: { size: 'sm', count: 3 } }
export const Medium: Story = { args: { size: 'md', count: 3 } }
export const DoubleDigit: Story = { args: { size: 'md', count: 12 } }
export const Zero: Story = { args: { size: 'sm', count: 0 } }

/** Оба размера рядом. */
export const AllSizes: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
      <UnreadBadge size="sm" count={3} />
      <UnreadBadge size="md" count={3} />
    </div>
  ),
}
