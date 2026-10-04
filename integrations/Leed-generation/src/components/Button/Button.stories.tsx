import type { Meta, StoryObj } from '@storybook/react-vite'
import { Plus } from 'lucide-react'
import { Button } from './Button'

/** Button — основная кнопка действий. Style×Size — пропы; Hover/Pressed/Focused — нативные псевдоклассы. */
const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  args: { variant: 'primary', size: 'm', children: 'Новый лид' },
  argTypes: {
    variant: { control: 'inline-radio', options: ['primary', 'secondary', 'tertiary'] },
    size: { control: 'inline-radio', options: ['m', 's'] },
    disabled: { control: 'boolean' },
    loading: { control: 'boolean' },
    children: { control: 'text' },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Button>
export default meta

type Story = StoryObj<typeof meta>

export const Primary: Story = { args: { variant: 'primary' } }
export const Secondary: Story = { args: { variant: 'secondary', children: 'Отключить' } }
export const Tertiary: Story = { args: { variant: 'tertiary', children: 'Подробнее' } }
export const SizeS: Story = { args: { size: 's' } }
export const WithIcon: Story = { args: { leftIcon: <Plus size={16} /> } }
export const Loading: Story = { args: { loading: true } }
export const Disabled: Story = { args: { disabled: true } }

/** Матрица Style × Size — все варианты рядом, сверка с Figma одним взглядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {(['primary', 'secondary', 'tertiary'] as const).map((variant) => (
        <div key={variant} style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <span style={{ width: 90, fontFamily: 'var(--font-sans)', fontSize: 12, color: 'var(--color-text-secondary)' }}>{variant}</span>
          <Button variant={variant} size="m">Подключить</Button>
          <Button variant={variant} size="s">Подключить</Button>
          <Button variant={variant} size="m" leftIcon={<Plus size={16} />}>Новый лид</Button>
          <Button variant={variant} size="m" loading>Загрузка</Button>
          <Button variant={variant} size="m" disabled>Disabled</Button>
        </div>
      ))}
    </div>
  ),
}
