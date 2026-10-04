import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Search } from 'lucide-react'
import { Input } from './Input'

/** Input — поле ввода, Type=Text|Textarea. State: Hover/Focus — нативные; Error/Disabled — пропы. */
const meta = {
  title: 'Components/Input',
  component: Input,
  tags: ['autodocs'],
  args: { label: 'Название поля', value: '', placeholder: 'Введите значение' },
  argTypes: {
    type: { control: 'inline-radio', options: ['text', 'textarea'] },
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
    showHint: { control: 'boolean' },
    hint: { control: 'text' },
    value: { control: 'text' },
    label: { control: 'text' },
  },
  parameters: { layout: 'centered' },
  render: (args) => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [value, setValue] = useState(args.value)
    return (
      <div style={{ width: 280 }}>
        <Input {...args} value={value} onChange={setValue} />
      </div>
    )
  },
} satisfies Meta<typeof Input>
export default meta

type Story = StoryObj<typeof meta>

export const Text: Story = {}
export const Textarea: Story = {
  args: { type: 'textarea', label: 'Комментарий', value: 'Например: обсудили условия поставки' },
}
export const WithIcon: Story = { args: { showIcon: true, icon: <Search size={16} />, value: 'Найти лида' } }
export const Error: Story = {
  args: { error: true, showHint: true, hint: 'Обязательное поле — опишите содержание разговора' },
}
export const Disabled: Story = { args: { disabled: true, value: 'Недоступно' } }

/** Type × State — все варианты рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
      <div style={{ width: 240 }}>
        <Input label="Обычное" value="Значение" onChange={() => {}} />
      </div>
      <div style={{ width: 240 }}>
        <Input label="Textarea" type="textarea" value="Комментарий на несколько строк" onChange={() => {}} />
      </div>
      <div style={{ width: 240 }}>
        <Input label="С ошибкой" value="" onChange={() => {}} error showHint hint="Обязательное поле" />
      </div>
      <div style={{ width: 240 }}>
        <Input label="Disabled" value="Недоступно" onChange={() => {}} disabled />
      </div>
    </div>
  ),
}
