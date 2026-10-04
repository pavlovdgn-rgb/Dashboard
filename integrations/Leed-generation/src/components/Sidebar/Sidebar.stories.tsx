import type { Meta, StoryObj } from '@storybook/react-vite'
import { Sidebar } from './Sidebar'

/**
 * Sidebar — 80px тёмная колонка иконок; при hover/focus справа выезжает 340px флайаут со списком навигации
 * (ds/components.md → «Раскрытое состояние (hover/click)»). Наведите курсор на рельс в canvas, чтобы увидеть анимацию.
 */
const meta = {
  title: 'Components/Sidebar',
  component: Sidebar,
  tags: ['autodocs'],
  args: {
    title: 'Генератор лидов',
    items: [{ label: 'Лиды', active: true }, { label: 'Канбан', pinned: true }, { label: 'Дашборд' }, { label: 'Настройки' }],
  },
  parameters: { layout: 'fullscreen' },
  decorators: [(Story) => <div style={{ height: '100vh' }}><Story /></div>],
} satisfies Meta<typeof Sidebar>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}

/** Тот же единственный композиционный вариант — Sidebar не несёт formal-осей, кроме hover-состояния флайаута. */
export const AllVariants: Story = {
  decorators: [(Story) => <div style={{ height: '100vh' }}><Story /></div>],
  render: () => <Sidebar />,
}
