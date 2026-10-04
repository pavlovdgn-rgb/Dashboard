import type { Meta, StoryObj } from '@storybook/react-vite'
import { Button } from '../Button'
import { Tooltip } from './Tooltip'

/** Tooltip — короткая контекстная подсказка по hover/focus триггера. Position: top|bottom. */
const meta = {
  title: 'Components/Tooltip',
  component: Tooltip,
  tags: ['autodocs'],
  args: { content: 'Подсказка', position: 'top', children: <Button variant="secondary" size="s">Наведи курсор</Button> },
  argTypes: {
    content: { control: 'text' },
    position: { control: 'inline-radio', options: ['top', 'bottom'] },
  },
  parameters: { layout: 'centered' },
} satisfies Meta<typeof Tooltip>
export default meta

type Story = StoryObj<typeof meta>

export const Top: Story = { args: { position: 'top' } }
export const Bottom: Story = { args: { position: 'bottom' } }

/** Top × Bottom рядом. */
export const AllVariants: Story = {
  parameters: { layout: 'padded' },
  render: () => (
    <div style={{ display: 'flex', gap: 48, padding: 32 }}>
      <Tooltip content="Подсказка сверху" position="top">
        <Button variant="secondary" size="s">top</Button>
      </Tooltip>
      <Tooltip content="Подсказка снизу" position="bottom">
        <Button variant="secondary" size="s">bottom</Button>
      </Tooltip>
    </div>
  ),
}
