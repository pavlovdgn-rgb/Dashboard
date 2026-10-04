import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { Toggle } from './Toggle'

/** Toggle — переключатель вкл/выкл. Position=Off|On; State: Normal|Hover|Disabled — нативные. */
const meta = {
  title: 'Components/Toggle',
  component: Toggle,
  tags: ['autodocs'],
  args: { on: true, 'aria-label': 'Включить автоназначение' },
  argTypes: {
    on: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
  parameters: { layout: 'centered' },
  render: (args) => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    const [on, setOn] = useState(args.on)
    return <Toggle {...args} on={on} onChange={setOn} />
  },
} satisfies Meta<typeof Toggle>
export default meta

type Story = StoryObj<typeof meta>

export const On: Story = { args: { on: true } }
export const Off: Story = { args: { on: false } }
export const Disabled: Story = { args: { on: true, disabled: true } }

/** On × Off × Disabled — все состояния рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
      <Toggle on={true} onChange={() => {}} aria-label="On" />
      <Toggle on={false} onChange={() => {}} aria-label="Off" />
      <Toggle on={true} onChange={() => {}} aria-label="Disabled on" disabled />
      <Toggle on={false} onChange={() => {}} aria-label="Disabled off" disabled />
    </div>
  ),
}
