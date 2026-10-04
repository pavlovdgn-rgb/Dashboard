import type { Meta, StoryObj } from '@storybook/react-vite'
import { ArrowRight } from 'lucide-react'
import { TextButton } from './TextButton'

/** Text Button — кнопка-ссылка без фона, для второстепенных действий. State: Normal|Hover|Pressed|Disabled — нативные. */
const meta = {
  title: 'Components/TextButton',
  component: TextButton,
  tags: ['autodocs'],
  args: { children: 'Сбросить всё' },
  argTypes: {
    disabled: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof TextButton>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const WithIcon: Story = { args: { children: 'Открыть карточку лида', rightIcon: <ArrowRight size={14} /> } }
export const Disabled: Story = { args: { disabled: true } }

/** Все состояния рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <TextButton>Сбросить всё</TextButton>
      <TextButton rightIcon={<ArrowRight size={14} />}>Открыть карточку лида</TextButton>
      <TextButton disabled>Disabled</TextButton>
    </div>
  ),
}
