import type { Meta, StoryObj } from '@storybook/react-vite'
import { FunnelBar } from './FunnelBar'

/** FunnelBar — одна строка горизонтальной воронки. Tone: Neutral|Negative — красит заливку Bar. */
const meta = {
  title: 'Components/FunnelBar',
  component: FunnelBar,
  tags: ['autodocs'],
  args: { label: 'Новый', value: 42, percent: 100, tone: 'neutral' },
  argTypes: {
    tone: { control: 'inline-radio', options: ['neutral', 'negative'] },
    label: { control: 'text' },
    value: { control: 'number' },
    percent: { control: { type: 'range', min: 0, max: 100 } },
  },
  parameters: { layout: 'padded' },
} satisfies Meta<typeof FunnelBar>
export default meta

type Story = StoryObj<typeof meta>

export const Neutral: Story = {}
export const Negative: Story = { args: { label: 'Не подходит', value: 8, percent: 19, tone: 'negative' } }

/** Полная воронка — как в FunnelSection на Dashboard. */
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, width: 480 }}>
      <FunnelBar label="Новый" value={42} percent={100} />
      <FunnelBar label="В работе" value={35} percent={83} />
      <FunnelBar label="Перезвонить" value={18} percent={43} />
      <FunnelBar label="Квалифицирован" value={24} percent={57} />
      <FunnelBar label="Не подходит" value={8} percent={19} tone="negative" />
    </div>
  ),
}
