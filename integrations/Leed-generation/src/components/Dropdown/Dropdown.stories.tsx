import type { Meta, StoryObj } from '@storybook/react-vite'
import { Dropdown } from './Dropdown'

/** Dropdown — триггер, открывающий панель с опциями. State: closed|open (клик) |hover (нативно) |disabled. */
const meta = {
  title: 'Components/Dropdown',
  component: Dropdown,
  tags: ['autodocs'],
  args: { label: 'Канал: Все', options: ['Все', 'Форма', 'Звонок', 'Чат'] },
  argTypes: {
    label: { control: 'text' },
    disabled: { control: 'boolean' },
    options: { control: 'object' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Dropdown>
export default meta

type Story = StoryObj<typeof meta>

export const Closed: Story = {}
export const Assignee: Story = { args: { label: 'не назначен', options: ['не назначен', 'Игорь Петров', 'Анна Смирнова'] } }
export const Disabled: Story = { args: { disabled: true } }

/** Длинный текст триггера — обрезается многоточием (ellipsis), не разрывает layout строки фильтров. */
export const LongLabel: Story = {
  args: { label: 'Ответственный: Кузнецова Мария Александровна (в отпуске до 14 сентября)' },
}

/** Много опций — панель ограничена по высоте (240px) и скроллится, не растягивается до бесконечности. Кликните триггер, чтобы увидеть плавное появление панели (fade + сдвиг, 160ms). */
export const ManyOptions: Story = {
  args: {
    label: 'Ответственный: Все',
    options: [
      'Все', 'Игорь Петров', 'Анна Смирнова', 'Дмитрий Волков', 'Марина Кузнецова', 'Сергей Орлов',
      'Ольга Романова', 'Павел Ким', 'Наталья Егорова', 'Виктор Лебедев', 'Елена Соколова', 'Артём Быков',
    ],
  },
}

/** Пустой список опций — клик по триггеру не открывает пустую панель (нечего показывать). */
export const EmptyOptions: Story = { args: { label: 'Нет доступных значений', options: [] } }

/** Пример открытой панели и disabled рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 24 }}>
      <Dropdown label="Канал: Все" options={['Все', 'Форма', 'Звонок', 'Чат']} />
      <Dropdown label="Недоступно" disabled />
    </div>
  ),
}
