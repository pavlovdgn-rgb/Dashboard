import type { Meta, StoryObj } from '@storybook/react-vite'
import { ChatWindowProvider } from '../../data/ChatWindowContext'
import { LeadsProvider } from '../../data/LeadsContext'
import { GlobalChatWindow } from './GlobalChatWindow'
import { ModuleNav } from './ModuleNav'

/**
 * ModuleNav — продуктовая шапка экрана (см. ds/components.md → "Header" [замещён этим] и "ChatIconButton").
 * Живёт в screens/_shared (переиспользуется всеми экранами, не отдельный `components/*`-атом), но
 * заведён здесь как полноценная Storybook-история — иначе кнопка чата/бейдж непрочитанных, ключевая часть
 * недавнего редизайна чата, нигде не видна в каталоге компонентов (найдено пользователем 2026-08-29:
 * «в сторибуке в хедере нет кнопки чата, а в фигме есть»).
 *
 * ModuleNav сам читает useLeads()/useChatWindow() (не прокидывается пропами — см. его же docblock), поэтому
 * история обёрнута в реальные провайдеры + смонтирован GlobalChatWindow — клик по кнопке чата здесь
 * по-настоящему открывает ChatSwitcherPopover с живыми mock-данными, а выбор чата показывает настоящее
 * плавающее окно (та же связка, что в реальном приложении, см. App.tsx).
 */
const meta = {
  title: 'Components/ModuleNav',
  component: ModuleNav,
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <LeadsProvider>
        <ChatWindowProvider>
          <Story />
          <GlobalChatWindow />
        </ChatWindowProvider>
      </LeadsProvider>
    ),
  ],
  args: {
    title: 'Генератор лидов',
    userName: 'Марина Кузнецова',
    userInitials: 'МК',
  },
  parameters: { layout: 'fullscreen' },
} satisfies Meta<typeof ModuleNav>
export default meta

type Story = StoryObj<typeof meta>

/** Как на «Лиды»/«Канбан»/«Дашборд» — статус-бейдж слева + кнопка чата с непрочитанными справа. */
export const Default: Story = {
  args: { badge: { label: '3 просрочено', status: 'warning' } },
}

/** Явный override — 0 непрочитанных, независимо от реальных mock-данных (см. unreadCount в ModuleNavProps). */
export const NoUnread: Story = {
  args: { badge: { label: '0 просрочено', status: 'success' }, unreadCount: 0 },
}

/** Settings-экраны и подобные — без статус-бейджа, кнопка чата всё равно на месте (глобальная, не зависит от экрана). */
export const WithoutStatusBadge: Story = {
  args: { userName: 'Сергей Орлов', userInitials: 'СО' },
}
