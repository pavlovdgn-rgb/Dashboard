import type { Meta, StoryObj } from '@storybook/react-vite'
import { Avatar } from '../Avatar'
import { Header } from './Header'

/** Header — верхняя панель экрана, одиночный компонент без вариантов. */
const meta = {
  title: 'Components/Header',
  component: Header,
  tags: ['autodocs'],
  args: { title: 'Генератор лидов', userName: 'Марина Кузнецова', avatar: <Avatar size="md" initials="МК" /> },
  argTypes: {
    title: { control: 'text' },
    userName: { control: 'text' },
  },
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof Header>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}

/** Единственный вариант — компонент не несёт formal-осей. */
export const AllVariants: Story = {
  render: () => <Header title="Генератор лидов" userName="Марина Кузнецова" avatar={<Avatar size="md" initials="МК" />} />,
}
