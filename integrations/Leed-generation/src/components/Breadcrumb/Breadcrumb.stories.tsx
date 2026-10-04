import type { Meta, StoryObj } from '@storybook/react-vite'
import { Breadcrumb } from './Breadcrumb'

/** Breadcrumb — путь по иерархии страниц. State: default|current. */
const meta = {
  title: 'Components/Breadcrumb',
  component: Breadcrumb,
  tags: ['autodocs'],
  args: { current: false, children: 'Настройки' },
  argTypes: {
    current: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Breadcrumb>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Current: Story = { args: { current: true, children: 'Роли и права' } }

/** Полный путь — default → current. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center', fontFamily: 'var(--font-sans)', fontSize: 12, color: 'var(--color-text-secondary)' }}>
      <Breadcrumb>Настройки</Breadcrumb>
      <span>/</span>
      <Breadcrumb current>Роли и права</Breadcrumb>
    </div>
  ),
}
