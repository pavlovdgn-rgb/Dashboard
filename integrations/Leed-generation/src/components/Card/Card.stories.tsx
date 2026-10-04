import type { Meta, StoryObj } from '@storybook/react-vite'
import { Card } from './Card'

/** Card — контейнер с отступом для группировки контента. Padding: compact|default; Border: yes|no. */
const meta = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'],
  args: { padding: 'default', border: true, children: 'Card content' },
  argTypes: {
    padding: { control: 'inline-radio', options: ['compact', 'default'] },
    border: { control: 'boolean' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Card>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: (
      <>
        <span className="ds-desktop-main-medium">Ленинградский зоопарк</span>
        <span className="ds-desktop-main-regular">Скор 82 · Форма · 12 мин назад</span>
      </>
    ),
  },
}
export const Compact: Story = { args: { padding: 'compact', border: false } }
export const NoBorder: Story = { args: { border: false } }

/** Padding × Border — все варианты рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <Card padding="default" border>
        <span className="ds-desktop-main-medium">Default + Border</span>
      </Card>
      <Card padding="default" border={false}>
        <span className="ds-desktop-main-medium">Default, no border</span>
      </Card>
      <Card padding="compact" border>
        <span className="ds-desktop-main-medium">Compact + Border</span>
      </Card>
    </div>
  ),
}
