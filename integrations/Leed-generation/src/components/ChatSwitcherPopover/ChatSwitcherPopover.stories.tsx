import type { Meta, StoryObj } from '@storybook/react-vite'
import { ChatSwitcherPopover, type ChatSummary } from './ChatSwitcherPopover'

const SAMPLE_CHATS: ChatSummary[] = [
  { id: 'lead-2', initials: 'ДО', name: 'Дмитриев Олег', preview: 'Отлично, буду ждать расчёт', time: '14:06', unread: 3 },
  { id: 'lead-4', initials: 'ЕИ', name: 'Екатерина Иванова', preview: 'Хорошо, тогда до связи', time: 'вчера', unread: 0 },
  { id: 'lead-3', initials: 'СА', name: 'Соколова Анна', preview: 'А когда можно приехать на объект?', time: '2 дня назад', unread: 1 },
  { id: 'lead-5', initials: 'МК', name: 'Мария Кузнецова', preview: 'Спасибо, всё понятно', time: '3 дня назад', unread: 0 },
]

/** ChatSwitcherPopover — список активных переписок для быстрого переключения. Два входа: ChatIconButton в ModuleNav, TitleBar ChatWindow. */
const meta = {
  title: 'Components/ChatSwitcherPopover',
  component: ChatSwitcherPopover,
  tags: ['autodocs'],
  args: { chats: SAMPLE_CHATS, onSelect: () => {} },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof ChatSwitcherPopover>
export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const AllRead: Story = {
  args: { chats: SAMPLE_CHATS.map((c) => ({ ...c, unread: 0 })) },
}
