import type { Meta, StoryObj } from '@storybook/react-vite'
import { Typography } from './Typography'

/** Полная шкала текстовых стилей проекта. */
const meta = {
  title: 'Foundation/Typography',
  component: Typography,
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof Typography>
export default meta

type Story = StoryObj<typeof meta>

export const AllStyles: Story = {}
