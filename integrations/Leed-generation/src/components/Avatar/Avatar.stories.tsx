import type { Meta, StoryObj } from '@storybook/react-vite'
import { Avatar } from './Avatar'

/** Avatar — круг с инициалами пользователя. Size: Sm(24)|Md(32). */
const meta = {
  title: 'Components/Avatar',
  component: Avatar,
  tags: ['autodocs'],
  args: { size: 'md', initials: 'МК' },
  argTypes: {
    size: { control: 'inline-radio', options: ['sm', 'md'] },
    initials: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Avatar>
export default meta

type Story = StoryObj<typeof meta>

export const Small: Story = { args: { size: 'sm' } }
export const Medium: Story = { args: { size: 'md' } }

/** Sm × Md рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
      <Avatar size="sm" initials="ИП" />
      <Avatar size="md" initials="МК" />
    </div>
  ),
}
