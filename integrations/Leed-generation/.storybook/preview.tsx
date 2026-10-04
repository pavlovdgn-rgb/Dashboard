import type { Preview } from '@storybook/react-vite'
import '../src/index.css'

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },

    a11y: {
      // 'todo' - show a11y violations in the test UI only
      // 'error' - fail CI on a11y violations
      // 'off' - skip a11y checks entirely
      test: 'todo',
    },

    backgrounds: {
      default: 'page',
      values: [
        { name: 'page', value: '#F4F5F7' },
        { name: 'surface', value: '#FFFFFF' },
        { name: 'dark', value: '#253858' },
      ],
    },
  },
}

export default preview
