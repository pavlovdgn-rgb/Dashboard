import { useState } from 'react'
import type { Meta, StoryObj } from '@storybook/react-vite'
import { ChatWindow, type ChatWindowMessage } from './ChatWindow'
import type { ChatSummary } from '../ChatSwitcherPopover'

const SAMPLE_MESSAGES: ChatWindowMessage[] = [
  { id: 'm1', sender: 'client', meta: 'Клиент, 14:02', message: 'Здравствуйте! Подскажите про КП' },
  { id: 'm2', sender: 'manager', meta: 'Менеджер (Игорь Петров), 14:05', message: 'Да, посчитаю стоимость с доставкой' },
  { id: 'm3', sender: 'client', meta: 'Клиент, 14:06', message: 'Отлично, буду ждать расчёт' },
]

const SAMPLE_CHATS: ChatSummary[] = [
  { id: 'lead-2', initials: 'ДО', name: 'Дмитриев Олег', preview: 'Отлично, буду ждать расчёт', time: '14:06', unread: 3 },
  { id: 'lead-4', initials: 'ЕИ', name: 'Екатерина Иванова', preview: 'Хорошо, тогда до связи', time: 'вчера', unread: 0 },
  { id: 'lead-3', initials: 'СА', name: 'Соколова Анна', preview: 'А когда можно приехать на объект?', time: '2 дня назад', unread: 1 },
]

/**
 * ChatWindow — плавающее окно чата с лидом (заменяет докнутый ChatConversationPanel). State: Expanded|Minimized.
 * Компонент не навязывает позиционирование на странице — родитель решает, где разместить (drag/global state — отдельная задача).
 */
const meta = {
  title: 'Components/ChatWindow',
  component: ChatWindow,
  tags: ['autodocs'],
  args: {
    state: 'expanded',
    leadName: 'Дмитриев Олег',
    leadInitials: 'ДО',
    messages: SAMPLE_MESSAGES,
    unreadCount: 3,
    onSend: () => {},
    onMinimize: () => {},
    onExpand: () => {},
    onClose: () => {},
  },
  argTypes: {
    state: { control: 'inline-radio', options: ['expanded', 'minimized'] },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof ChatWindow>
export default meta

type Story = StoryObj<typeof meta>

export const Expanded: Story = { args: { state: 'expanded' } }
export const Minimized: Story = { args: { state: 'minimized' } }

export const ExpandedWithSwitcher: Story = {
  args: { state: 'expanded', chats: SAMPLE_CHATS },
}

export const EmptyConversation: Story = {
  args: { state: 'expanded', messages: [] },
}

/** Интерактивный пример — свернуть/развернуть переключает состояние по-настоящему. */
export const Interactive: Story = {
  render: (args) => {
    function Wrapper() {
      const [state, setState] = useState<'expanded' | 'minimized'>('expanded')
      return <ChatWindow {...args} state={state} onMinimize={() => setState('minimized')} onExpand={() => setState('expanded')} />
    }
    return <Wrapper />
  },
}
