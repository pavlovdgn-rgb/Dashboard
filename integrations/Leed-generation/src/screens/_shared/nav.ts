export interface NavConfigItem {
  label: string
  route: string
  pinned?: boolean
  matches: (pathname: string) => boolean
}

/**
 * Единая карта «пункт флайаута Sidebar → маршрут реестра + когда он активен».
 * Overlay-экраны (LeadCard/ChatPanel поверх канбана, CallLogModal/IncomingCallPopup поверх таблицы) подсвечивают
 * пункт того экрана, что лежит под overlay — так пользователь не теряет ориентацию, на каком разделе он находится.
 */
export const NAV_ITEMS: NavConfigItem[] = [
  {
    label: 'Лиды',
    route: '/leads-table',
    matches: (p) => p.startsWith('/leads-table') || p === '/call-log-modal' || p === '/incoming-call-popup' || p === '/not-found',
  },
  {
    label: 'Канбан',
    route: '/leads-kanban',
    pinned: true,
    matches: (p) => p.startsWith('/leads-kanban') || p === '/lead-card' || p === '/chat-panel',
  },
  {
    label: 'Дашборд',
    route: '/dashboard',
    matches: (p) => p.startsWith('/dashboard'),
  },
  {
    label: 'Настройки',
    route: '/settings/roles',
    matches: (p) => p.startsWith('/settings') || p === '/access-denied',
  },
]
