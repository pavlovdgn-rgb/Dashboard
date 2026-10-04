import type { Meta, StoryObj } from '@storybook/react-vite'
import { KanbanCard } from './KanbanCard'

/** KanbanCard — карточка одного лида в колонке канбан-доски. Overdue: No|Yes — красит border и TimeText. */
const meta = {
  title: 'Components/KanbanCard',
  component: KanbanCard,
  tags: ['autodocs'],
  args: {
    channel: 'Форма',
    nameCompany: 'Иванов Пётр, Ленинградский зоопарк',
    score: 82,
    timeText: '12 мин назад',
    managerName: 'Игорь Петров',
    managerInitials: 'ИП',
    overdue: false,
  },
  argTypes: {
    channel: { control: 'text' },
    nameCompany: { control: 'text' },
    score: { control: 'number' },
    timeText: { control: 'text' },
    managerName: { control: 'text' },
    overdue: { control: 'boolean' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof KanbanCard>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Unassigned: Story = {
  args: { channel: 'Чат', nameCompany: 'Дмитриев Олег, Петропавловская крепость', score: 91, timeText: '40 мин назад', managerName: undefined, managerInitials: undefined },
}
export const Overdue: Story = {
  args: { channel: 'Форма', nameCompany: 'Кузнецова Мария, ГМИИ им. А.С. Пушкина', score: 45, timeText: '1 день назад — Просрочен', overdue: true },
}

/** Overdue No|Yes рядом — как в колонке LeadsKanban. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <KanbanCard channel="Форма" nameCompany="Иванов Пётр, Ленинградский зоопарк" score={82} timeText="12 мин назад" managerName="Игорь Петров" managerInitials="ИП" />
      <KanbanCard channel="Чат" nameCompany="Дмитриев Олег, Петропавловская крепость" score={91} timeText="40 мин назад" />
      <KanbanCard channel="Форма" nameCompany="Кузнецова Мария, ГМИИ им. А.С. Пушкина" score={45} timeText="1 день назад — Просрочен" managerName="Игорь Петров" managerInitials="ИП" overdue />
    </div>
  ),
}
