import type { Meta, StoryObj } from '@storybook/react-vite'
import { StatusBadge } from '../StatusBadge'
import { TableCell } from './TableCell'

/** Table Cell — универсальная ячейка таблицы, роль переключается свойством Type. */
const meta = {
  title: 'Components/TableCell',
  component: TableCell,
  tags: ['autodocs'],
  args: { type: 'text', children: 'Иванов Пётр, Ленинградский зоопарк' },
  argTypes: {
    type: { control: 'select', options: ['header', 'header-icon', 'text', 'status', 'checkbox', 'actions', 'toggle'] },
    disabled: { control: 'boolean' },
  },
  parameters: { layout: 'padded' },
} satisfies Meta<typeof TableCell>
export default meta

type Story = StoryObj<typeof meta>

export const Header: Story = { args: { type: 'header', children: 'Имя и компания' } }
export const Text: Story = { args: { type: 'text', children: 'Иванов Пётр, Ленинградский зоопарк' } }
export const Status: Story = { args: { type: 'status', children: <StatusBadge status="success">Активно</StatusBadge> } }

/** Все типы рядом. */
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex' }}>
      <TableCell type="header">Заголовок</TableCell>
      <TableCell type="text">Текстовая ячейка</TableCell>
      <TableCell type="status">
        <StatusBadge status="success">Активно</StatusBadge>
      </TableCell>
    </div>
  ),
}
