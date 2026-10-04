import type { Meta, StoryObj } from '@storybook/react-vite'
import { TimelineItem } from './TimelineItem'

/** TimelineItem — одна запись в хронологической ленте взаимодействий с лидом. Type: Call|Form|Chat — красит IconBadge (accent-круг без глифа). */
const meta = {
  title: 'Components/TimelineItem',
  component: TimelineItem,
  tags: ['autodocs'],
  args: { type: 'call', title: 'Звонок исходящий', meta: '1 день назад — Игорь Петров', quote: 'Просила перезвонить после обеда' },
  argTypes: {
    type: { control: 'inline-radio', options: ['call', 'form', 'chat'] },
    title: { control: 'text' },
    meta: { control: 'text' },
    quote: { control: 'text' },
  },
  parameters: { layout: 'padded' },
} satisfies Meta<typeof TimelineItem>
export default meta

type Story = StoryObj<typeof meta>

export const Call: Story = {}
export const Form: Story = { args: { type: 'form', title: 'Заявка с сайта', meta: '3 дня назад', quote: 'Интересует установка 50 билетных систем с последующим обучением персонала' } }
export const Chat: Story = { args: { type: 'chat', title: 'Обращение через чат-виджет сайта', meta: 'Сегодня, 14:02', quote: 'Спрашивают об интеграции системы контроля доступа с билетной кассой' } }

/** Call × Form × Chat — как в ActivityTimeline на LeadCard. */
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <TimelineItem type="call" title="Звонок исходящий" meta="1 день назад — Игорь Петров" quote="Просила перезвонить после обеда" />
      <TimelineItem type="form" title="Заявка с сайта" meta="3 дня назад" quote="Интересует установка 50 билетных систем" />
      <TimelineItem type="chat" title="Обращение через чат-виджет сайта" meta="Сегодня, 14:02" quote="Спрашивают об интеграции системы контроля доступа" />
    </div>
  ),
}
