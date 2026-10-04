import type { Meta, StoryObj } from '@storybook/react-vite'
import { MetricCard } from './MetricCard'

/** MetricCard — карточка одной ключевой метрики дашборда. Trend: Neutral|Positive|Negative — красит только Value, Caption всегда secondary. */
const meta = {
  title: 'Components/MetricCard',
  component: MetricCard,
  tags: ['autodocs'],
  args: { label: 'Время первого ответа', value: '4 мин', caption: 'цель < 5 мин чат / < 30 мин звонок', trend: 'positive' },
  argTypes: {
    trend: { control: 'inline-radio', options: ['neutral', 'positive', 'negative'] },
    label: { control: 'text' },
    value: { control: 'text' },
    caption: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof MetricCard>
export default meta

type Story = StoryObj<typeof meta>

export const Positive: Story = { args: { trend: 'positive' } }
export const Negative: Story = { args: { label: 'Просроченные лиды', value: '3', caption: 'требуют внимания', trend: 'negative' } }
export const Neutral: Story = { args: { label: 'Лидов за период', value: '127', caption: 'всего за месяц', trend: 'neutral' } }

/** Все три тренда рядом — как в KeyMetricsRow на Dashboard. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 16 }}>
      <MetricCard label="Время первого ответа" value="4 мин" caption="цель < 5 мин" trend="positive" />
      <MetricCard label="Просроченные лиды" value="3" caption="требуют внимания" trend="negative" />
      <MetricCard label="Лидов за период" value="127" caption="всего за месяц" trend="neutral" />
    </div>
  ),
}
