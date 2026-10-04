import type { Meta, StoryObj } from '@storybook/react-vite'
import { Colors } from './Colors'

/** Вся палитра проекта — Primitive и Semantic слои, сгруппированы как в ds/foundation.md. */
const meta = {
  title: 'Foundation/Colors',
  component: Colors,
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof Colors>
export default meta

type Story = StoryObj<typeof meta>

export const AllColors: Story = {}
