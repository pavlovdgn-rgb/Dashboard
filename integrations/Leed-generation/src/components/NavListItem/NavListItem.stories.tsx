import type { Meta, StoryObj } from '@storybook/react-vite'
import { NavListItem } from './NavListItem'

/** NavListItem — пункт списка в раскрытом Sidebar-флайауте. State: Default|Hover|Active; Pinned: No|Yes (матрица 3×2). Active красит только текст (brand/primary), не фон. */
const meta = {
  title: 'Components/NavListItem',
  component: NavListItem,
  tags: ['autodocs'],
  args: { active: false, pinned: false, children: 'Лиды' },
  argTypes: {
    active: { control: 'boolean' },
    pinned: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
  decorators: [(Story) => <div style={{ width: 308, background: 'var(--color-bg-surface-primary)', padding: 8 }}><Story /></div>],
} satisfies Meta<typeof NavListItem>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Active: Story = { args: { active: true } }
export const Pinned: Story = { args: { pinned: true, children: 'Канбан' } }
export const ActivePinned: Story = { args: { active: true, pinned: true } }

/** Полный список — как в реальном флайауте Sidebar (Лиды/Канбан/Дашборд/Настройки). */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ width: 308, background: 'var(--color-bg-surface-primary)', padding: 8 }}>
      <NavListItem active>Лиды</NavListItem>
      <NavListItem pinned>Канбан</NavListItem>
      <NavListItem>Дашборд</NavListItem>
      <NavListItem>Настройки</NavListItem>
    </div>
  ),
}
