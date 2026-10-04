import type { Meta, StoryObj } from '@storybook/react-vite'
import { X } from 'lucide-react'
import { IconButton } from './IconButton'

/** Icon Button — квадратная кнопка под иконку без подписи, для тулбаров и заголовков панелей (паттерн close-icon). */
const meta = {
  title: 'Components/IconButton',
  component: IconButton,
  tags: ['autodocs'],
  args: { icon: <X size={16} />, 'aria-label': 'Закрыть' },
  argTypes: {
    disabled: { control: 'boolean' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof IconButton>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Disabled: Story = { args: { disabled: true } }

/** Normal / Disabled рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <IconButton icon={<X size={16} />} aria-label="Закрыть" />
      <IconButton icon={<X size={16} />} aria-label="Закрыть" disabled />
    </div>
  ),
}
