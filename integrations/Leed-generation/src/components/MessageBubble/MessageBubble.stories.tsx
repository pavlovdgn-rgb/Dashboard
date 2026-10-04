import type { Meta, StoryObj } from '@storybook/react-vite'
import { MessageBubble } from './MessageBubble'

/** MessageBubble — одно сообщение в переписке. Sender: Client(слева)|Manager(справа) — красит фон и выравнивание. */
const meta = {
  title: 'Components/MessageBubble',
  component: MessageBubble,
  tags: ['autodocs'],
  args: { sender: 'client', meta: 'Клиент, 14:02', message: 'Здравствуйте! Подскажите про интеграцию' },
  argTypes: {
    sender: { control: 'inline-radio', options: ['client', 'manager'] },
    meta: { control: 'text' },
    message: { control: 'text' },
  },
  parameters: { layout: 'padded' },
} satisfies Meta<typeof MessageBubble>
export default meta

type Story = StoryObj<typeof meta>

export const Client: Story = {}
export const Manager: Story = { args: { sender: 'manager', meta: 'Менеджер (Игорь Петров), 14:05', message: 'Добрый день! Да, есть такая возможность, посчитаю точную стоимость' } }

/** Диалог целиком — Client → Manager → Client, как в MessageHistory на ChatPanel. */
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <MessageBubble sender="client" meta="Клиент, 14:02" message="Здравствуйте! Подскажите про интеграцию" />
      <MessageBubble sender="manager" meta="Менеджер (Игорь Петров), 14:05" message="Добрый день! Да, есть такая возможность" />
      <MessageBubble sender="client" meta="Клиент, 14:06" message="Отлично, буду ждать расчёт" />
    </div>
  ),
}
