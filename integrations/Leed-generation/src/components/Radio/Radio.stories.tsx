import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Radio } from './Radio'

/** Radio — радиокнопка для единичного выбора. Selected=No|Yes; State: Normal|Hover|Disabled — нативные. */
const meta = {
  title: 'Components/Radio',
  component: Radio,
  tags: ['autodocs'],
  args: { selected: true, label: 'Исходящий' },
  argTypes: {
    selected: { control: 'boolean' },
    disabled: { control: 'boolean' },
    label: { control: 'text' },
  },
  parameters: { layout: 'centered' },
  render: (args) => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [selected, setSelected] = useState(args.selected)
    return <Radio {...args} selected={selected} onChange={() => setSelected(true)} />
  },
} satisfies Meta<typeof Radio>
export default meta

type Story = StoryObj<typeof meta>

export const Selected: Story = { args: { selected: true } }
export const Unselected: Story = { args: { selected: false } }
export const Disabled: Story = { args: { selected: false, disabled: true } }

/** Пара Radio в группе — Selected × Disabled. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 24 }}>
      <Radio selected={true} onChange={() => {}} label="Входящий" name="direction" />
      <Radio selected={false} onChange={() => {}} label="Исходящий" name="direction" />
      <Radio selected={false} onChange={() => {}} label="Disabled" disabled />
    </div>
  ),
}
