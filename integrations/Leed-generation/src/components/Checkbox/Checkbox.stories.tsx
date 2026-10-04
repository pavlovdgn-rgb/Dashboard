import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Checkbox } from './Checkbox'

/** Checkbox — чекбокс для мультивыбора. Checked=No|Yes; State: Normal|Hover|Disabled — нативные. */
const meta = {
  title: 'Components/Checkbox',
  component: Checkbox,
  tags: ['autodocs'],
  args: { checked: true, label: 'Игорь Петров' },
  argTypes: {
    checked: { control: 'boolean' },
    disabled: { control: 'boolean' },
    label: { control: 'text' },
  },
  parameters: { layout: 'centered' },
  render: (args) => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [checked, setChecked] = useState(args.checked)
    return <Checkbox {...args} checked={checked} onChange={setChecked} />
  },
} satisfies Meta<typeof Checkbox>
export default meta

type Story = StoryObj<typeof meta>

export const Checked: Story = { args: { checked: true } }
export const Unchecked: Story = { args: { checked: false } }
export const Disabled: Story = { args: { checked: false, disabled: true } }

/** Checked × Disabled — все варианты рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 24 }}>
      <Checkbox checked={true} onChange={() => {}} label="Checked" />
      <Checkbox checked={false} onChange={() => {}} label="Unchecked" />
      <Checkbox checked={false} onChange={() => {}} label="Disabled" disabled />
    </div>
  ),
}
