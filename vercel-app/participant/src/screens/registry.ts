import type { ComponentType } from 'react'
import { LeadsTable } from './leads-table/LeadsTable'
import { LeadsKanban } from './leads-kanban/LeadsKanban'
import { Dashboard } from './dashboard/Dashboard'
import { LeadCard } from './lead-card/LeadCard'
import { ChatPanel } from './chat-panel/ChatPanel'
import { ChatWidget } from './chat-widget/ChatWidget'
import { CallLogModal } from './call-log-modal/CallLogModal'
import { IncomingCallPopup } from './incoming-call-popup/IncomingCallPopup'
import { UserRolesSettings } from './user-roles-settings/UserRolesSettings'
import { AutoAssignmentSettings } from './auto-assignment-settings/AutoAssignmentSettings'
import { TelephonySettings } from './telephony-settings/TelephonySettings'
import { ChatWidgetSettings } from './chat-widget-settings/ChatWidgetSettings'
import { AccessDenied } from './access-denied/AccessDenied'
import { ErrorState } from './error-state/ErrorState'
import { NotFound404 } from './not-found-404/NotFound404'
import { EmptyLeadsTable } from './empty-leads-table/EmptyLeadsTable'
import { LoadingState } from './loading-state/LoadingState'
import { EmptyLeadsKanban } from './empty-leads-kanban/EmptyLeadsKanban'
import { EmptyDashboard } from './empty-dashboard/EmptyDashboard'
import { LoadingDashboard } from './loading-dashboard/LoadingDashboard'
import { EmptyUserRolesSettings } from './empty-user-roles-settings/EmptyUserRolesSettings'
import { LoadingUserRolesSettings } from './loading-user-roles-settings/LoadingUserRolesSettings'

export interface ScreenEntry {
  id: string
  name: string
  description: string
  route: string
  component: ComponentType
}

export const screens: ScreenEntry[] = [
  {
    id: 'leads-table',
    name: 'Таблица лидов',
    description: 'Основной рабочий экран менеджера: список лидов, фильтры, скор, статус, ответственный',
    route: '/leads-table',
    component: LeadsTable,
  },
  {
    id: 'leads-kanban',
    name: 'Канбан лидов',
    description: 'Альтернативный вид таблицы лидов — 5 колонок по статусу воронки',
    route: '/leads-kanban',
    component: LeadsKanban,
  },
  {
    id: 'dashboard',
    name: 'Дашборд руководителя',
    description: 'KPI, воронка лидов по статусам, нагрузка команды',
    route: '/dashboard',
    component: Dashboard,
  },
  {
    id: 'lead-card',
    name: 'Карточка лида',
    description: 'Slide-over поверх канбана: контакты, скор, статус, ответственный, история взаимодействий',
    route: '/lead-card',
    component: LeadCard,
  },
  {
    id: 'chat-panel',
    name: 'Плавающее окно чата',
    description: 'Переписка с клиентом — свободно перемещаемое окно поверх канбана, не блокирует остальной интерфейс',
    route: '/chat-panel',
    component: ChatPanel,
  },
  {
    id: 'chat-widget',
    name: 'Чат-виджет сайта',
    description: 'Виджет для посетителя сайта клиента — свёрнутый лаунчер и раскрытая панель',
    route: '/chat-widget',
    component: ChatWidget,
  },
  {
    id: 'call-log-modal',
    name: 'Записать звонок',
    description: 'Модальное окно ручной фиксации звонка вне телефонии',
    route: '/call-log-modal',
    component: CallLogModal,
  },
  {
    id: 'incoming-call-popup',
    name: 'Входящий звонок',
    description: 'Toast-уведомление о звонке с известного номера поверх таблицы лидов',
    route: '/incoming-call-popup',
    component: IncomingCallPopup,
  },
  {
    id: 'user-roles-settings',
    name: 'Роли и права',
    description: 'Настройки: список сотрудников и их роли доступа',
    route: '/settings/roles',
    component: UserRolesSettings,
  },
  {
    id: 'auto-assignment-settings',
    name: 'Автоназначение',
    description: 'Настройки автоматического распределения лидов между менеджерами',
    route: '/settings/auto-assignment',
    component: AutoAssignmentSettings,
  },
  {
    id: 'telephony-settings',
    name: 'Телефония',
    description: 'Подключение облачной АТС — провайдеры, статус линии, функции',
    route: '/settings/telephony',
    component: TelephonySettings,
  },
  {
    id: 'chat-widget-settings',
    name: 'Настройки чат-виджета',
    description: 'Код встраивания виджета и приветственное сообщение',
    route: '/settings/chat-widget',
    component: ChatWidgetSettings,
  },
  {
    id: 'access-denied',
    name: 'Доступ ограничен',
    description: 'Отказ в доступе к разделу «Настройки» для роли Менеджер',
    route: '/access-denied',
    component: AccessDenied,
  },
  {
    id: 'error-state',
    name: 'Ошибка загрузки',
    description: 'Сбой загрузки данных — повторить попытку',
    route: '/error',
    component: ErrorState,
  },
  {
    id: 'not-found-404',
    name: '404 — лид не найден',
    description: 'Лид удалён или недоступен',
    route: '/not-found',
    component: NotFound404,
  },
  {
    id: 'empty-leads-table',
    name: 'Таблица лидов — пусто',
    description: 'Empty-состояние таблицы лидов',
    route: '/leads-table/empty',
    component: EmptyLeadsTable,
  },
  {
    id: 'loading-state',
    name: 'Таблица лидов — загрузка',
    description: 'Loading-состояние таблицы лидов (skeleton)',
    route: '/leads-table/loading',
    component: LoadingState,
  },
  {
    id: 'empty-leads-kanban',
    name: 'Канбан — пусто',
    description: 'Empty-состояние канбан-доски лидов',
    route: '/leads-kanban/empty',
    component: EmptyLeadsKanban,
  },
  {
    id: 'empty-dashboard',
    name: 'Дашборд — нет данных',
    description: 'Empty-состояние дашборда за выбранный период',
    route: '/dashboard/empty',
    component: EmptyDashboard,
  },
  {
    id: 'loading-dashboard',
    name: 'Дашборд — загрузка',
    description: 'Loading-состояние дашборда (skeleton KPI/воронка/таблица)',
    route: '/dashboard/loading',
    component: LoadingDashboard,
  },
  {
    id: 'empty-user-roles-settings',
    name: 'Роли и права — пусто',
    description: 'Empty-состояние списка сотрудников',
    route: '/settings/roles/empty',
    component: EmptyUserRolesSettings,
  },
  {
    id: 'loading-user-roles-settings',
    name: 'Роли и права — загрузка',
    description: 'Loading-состояние списка сотрудников (skeleton)',
    route: '/settings/roles/loading',
    component: LoadingUserRolesSettings,
  },
]
