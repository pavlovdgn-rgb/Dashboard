import type { Meta, StoryObj } from '@storybook/react-vite'
import { StatusBadge } from '../StatusBadge'
import { Table } from './Table'

const COLUMNS = [
  { key: 'name', label: 'Имя и компания', width: 'fill' as const },
  { key: 'score', label: 'Скор', width: 90 },
  { key: 'status', label: 'Статус', width: 160 },
]

const ROWS = [
  { name: 'Иванов Пётр, Ленинградский зоопарк', score: '82', status: <StatusBadge status="neutral">Новый</StatusBadge> },
  { name: 'Соколова Анна, Музей петербургского авангарда', score: '65', status: <StatusBadge status="warning">В работе</StatusBadge> },
  { name: 'Кузнецова Мария, ГМИИ им. А.С. Пушкина', score: '45', status: <StatusBadge status="error">Перезвонить</StatusBadge> },
]

/** Table — список записей с заголовком и повторяющимися строками, собрана из TableCell. density: compact|default; sticky-header: yes|no. */
const meta = {
  title: 'Components/Table',
  component: Table,
  tags: ['autodocs'],
  args: { columns: COLUMNS, rows: ROWS, density: 'default', stickyHeader: false },
  argTypes: {
    density: { control: 'inline-radio', options: ['compact', 'default'] },
    stickyHeader: { control: 'boolean' },
  },
  parameters: { layout: 'padded' },
} satisfies Meta<typeof Table>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Compact: Story = { args: { density: 'compact' } }

/** Длинное содержимое ячейки — колонка «Имя и компания» на FILL, текст переносится, соседние FIXED-колонки не сжимаются. */
export const LongContent: Story = {
  args: {
    rows: [
      { name: 'Государственный музей истории религии — филиал в Петропавловской крепости, отдел учёта билетов', score: '96', status: <StatusBadge status="success">Квалифицирован</StatusBadge> },
      ...ROWS,
    ],
  },
}

/** Пустая таблица — заголовок остаётся, строк нет (edge case, не отдельный empty-state внутри Table — он строится на уровне экрана). */
export const Empty: Story = { args: { rows: [] } }

/** Много строк — тело таблицы скроллится в контейнере фиксированной высоты, header зафиксирован (stickyHeader). */
export const ManyRowsScrollable: Story = {
  args: { stickyHeader: true },
  decorators: [(Story) => <div style={{ height: 240, overflowY: 'auto' }}><Story /></div>],
  render: (args) => (
    <Table
      {...args}
      rows={[
        ...ROWS,
        { name: 'Волков Сергей, «ТехноПром»', score: '78', status: <StatusBadge status="success">Квалифицирован</StatusBadge> },
        { name: 'Смирнов Игорь, «Ромашка Сервис»', score: '22', status: <StatusBadge status="neutral">Новый</StatusBadge> },
        { name: 'Романова Ольга, Русский музей', score: '58', status: <StatusBadge status="warning">В работе</StatusBadge> },
        { name: 'Ким Павел, Эрмитаж', score: '71', status: <StatusBadge status="success">Квалифицирован</StatusBadge> },
        { name: 'Егорова Наталья, Кунсткамера', score: '39', status: <StatusBadge status="error">Перезвонить</StatusBadge> },
      ]}
    />
  ),
}

/** Default × Compact рядом. */
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <Table columns={COLUMNS} rows={ROWS} density="default" />
      <Table columns={COLUMNS} rows={ROWS} density="compact" />
    </div>
  ),
}
