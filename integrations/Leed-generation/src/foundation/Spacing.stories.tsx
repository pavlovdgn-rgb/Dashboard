import type { Meta, StoryObj } from '@storybook/react-vite'
import { Spacing } from './Spacing'

/** Отступы, радиусы, толщина обводки и тени. */
const meta = {
  title: 'Foundation/Spacing & Radius & Shadows',
  component: Spacing,
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof Spacing>
export default meta

type Story = StoryObj<typeof meta>

export const AllTokens: Story = {}
