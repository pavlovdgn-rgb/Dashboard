import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Select } from './Select'

/** Select — специализация Input под паттерн выбора. State: default|hover|focus|error|disabled. */
const meta = {
  title: 'Components/Select',
  component: Select,
  tags: ['autodocs'],
  args: { value: 'Форма', options: ['Все', 'Форма', 'Звонок', 'Чат'] },
  argTypes: {
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    options: { control: 'object' },
  },
  parameters: { layout: 'centered' },
  render: (args) => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [value, setValue] = useState(args.value)
    return (
      <div style={{ width: 200 }}>
        <Select {...args} value={value} onChange={setValue} />
      </div>
    )
  },
} satisfies Meta<typeof Select>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Error: Story = { args: { error: true } }
export const Disabled: Story = { args: { disabled: true } }

/** Длинный текст опции — нативный select переносит обрезку на уровне ОС/браузера, компонент не ломает layout. */
export const LongOptionText: Story = {
  args: {
    value: 'Перезвонить · Просрочен на 1 день, требует срочного внимания менеджера',
    options: ['Перезвонить · Просрочен на 1 день, требует срочного внимания менеджера', 'Новый', 'В работе'],
  },
}

/** Много опций — 12 значений, список открывается стандартным нативным поведением браузера. */
export const ManyOptions: Story = {
  args: {
    value: 'Игорь Петров',
    options: [
      'Игорь Петров', 'Анна Смирнова', 'Дмитрий Волков', 'Марина Кузнецова', 'Сергей Орлов', 'Ольга Романова',
      'Павел Ким', 'Наталья Егорова', 'Виктор Лебедев', 'Елена Соколова', 'Артём Быков', 'Юлия Фёдорова',
    ],
  },
}

/** Default × Error × Disabled — все состояния рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <div style={{ width: 180 }}>
        <Select value="Форма" onChange={() => {}} options={['Все', 'Форма', 'Звонок', 'Чат']} />
      </div>
      <div style={{ width: 180 }}>
        <Select value="Ошибка" onChange={() => {}} options={['Ошибка']} error />
      </div>
      <div style={{ width: 180 }}>
        <Select value="Недоступно" onChange={() => {}} options={['Недоступно']} disabled />
      </div>
    </div>
  ),
}
