import type { Meta, StoryObj } from '@storybook/react-vite'
import { Tabs } from './Tabs'

/** Tabs — один инстанс = один таб (композиция ряда — на стороне потребителя). State: default|active|disabled. */
const meta = {
  title: 'Components/Tabs',
  component: Tabs,
  tags: ['autodocs'],
  args: { active: false, disabled: false, children: 'Список' },
  argTypes: {
    active: { control: 'boolean' },
    disabled: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Tabs>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}
export const Active: Story = { args: { active: true } }
export const Disabled: Story = { args: { disabled: true } }

/** Default × Active × Disabled в ряду — как на горизонтальном ряду вкладок SettingsShell. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 8 }}>
      <Tabs active>Список</Tabs>
      <Tabs>Канбан</Tabs>
      <Tabs disabled>Disabled</Tabs>
    </div>
  ),
}
