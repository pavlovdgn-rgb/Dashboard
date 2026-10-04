import type { MetricCardTrend } from '../components/MetricCard'

export interface DashboardMetric {
  label: string
  value: string
  caption: string
  trend?: MetricCardTrend
}

export interface FunnelStage {
  label: string
  value: number
  tone: 'neutral' | 'negative'
}

export interface TeamRow {
  manager: string
  inProgress: string
  conversion: string
  overdue: string
  [key: string]: string
}

/**
 * Агрегаты дашборда за период — отдельный мок от рабочего списка `leads.ts`: представляют месяц реальных
 * обращений (сотни лидов), а не 7 демо-записей в таблице/канбане. Единственная величина, которую Dashboard
 * берёт из живого слоя лидов, — бейдж просрочки в ModuleNav (см. `LeadsContext.overdueCount`), она и должна
 * совпадать с тем, что реально показано на экранах «Лиды»/«Канбан».
 */
export const DASHBOARD_METRICS: DashboardMetric[] = [
  { label: 'Время первого ответа', value: '4 мин', caption: 'цель < 5 мин чат / < 30 мин звонок', trend: 'positive' },
  { label: 'Конверсия лид → сделка', value: '18%', caption: 'цель > 15% (North Star)', trend: 'positive' },
  { label: 'Лидов за период', value: '127', caption: '+12% к прошлому месяцу', trend: 'positive' },
]

export const DASHBOARD_FUNNEL: FunnelStage[] = [
  { label: 'Новый', value: 42, tone: 'neutral' },
  { label: 'В работе', value: 35, tone: 'neutral' },
  { label: 'Перезвонить', value: 18, tone: 'neutral' },
  { label: 'Квалифицирован', value: 24, tone: 'neutral' },
  { label: 'Не подходит', value: 8, tone: 'negative' },
]

export const DASHBOARD_FUNNEL_MAX = 42

export const DASHBOARD_TEAM: TeamRow[] = [
  { manager: 'Игорь Петров', inProgress: '35', conversion: '19%', overdue: '2' },
  { manager: 'Анна Смирнова', inProgress: '28', conversion: '21%', overdue: '1' },
  { manager: 'Дмитрий Волков', inProgress: '31', conversion: '15%', overdue: '0' },
]
