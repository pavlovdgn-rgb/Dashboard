import { Button } from '../../components/Button'
import { Dropdown } from '../../components/Dropdown'
import { MetricCard, type MetricCardTrend } from '../../components/MetricCard'
import { TextButton } from '../../components/TextButton'
import { AppShell } from '../_shared/AppShell'
import { EmptyState } from '../_shared/EmptyState'
import { ModuleNav } from '../_shared/ModuleNav'
import { DashboardIcon, PlusIcon } from '../_shared/icons'

interface Metric {
  label: string
  value: string
  caption: string
  trend?: MetricCardTrend
}

const METRICS: Metric[] = [
  { label: 'Время первого ответа', value: '4 мин', caption: 'цель < 5 мин чат / < 30 мин звонок', trend: 'positive' },
  { label: 'Конверсия лид → сделка', value: '18%', caption: 'цель > 15% (North Star)', trend: 'positive' },
  { label: 'Просроченные лиды', value: '3', caption: 'требуют внимания', trend: 'negative' },
  { label: 'Лидов за период', value: '127', caption: '+12% к прошлому месяцу', trend: 'positive' },
]

export function EmptyDashboard() {
  return (
    <AppShell>
      <ModuleNav badge={{ label: '0 просрочено', status: 'success' }} unreadCount={0} />
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-md)',
          padding: 'var(--space-lg) var(--space-xl)',
          background: 'var(--color-bg-surface-primary)',
          borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
          width: '100%',
          flexWrap: 'wrap',
        }}
      >
        <Dropdown label="Канал: Все" />
        <Dropdown label="Менеджер: Все" />
        <Dropdown label="Статус: Все" />
        <Dropdown label="Период: Сегодня" />
        <TextButton>Сбросить всё</TextButton>
        <span style={{ flex: '1 1 0%' }} />
        <Button leftIcon={<PlusIcon />}>Новый лид</Button>
      </div>

      <div style={{ display: 'flex', gap: 'var(--space-lg)', padding: 'var(--space-xl)', flexWrap: 'wrap' }}>
        {METRICS.map((metric) => (
          <div key={metric.label} style={{ flex: '1 1 200px', minWidth: 200 }}>
            <MetricCard label={metric.label} value={metric.value} caption={metric.caption} trend={metric.trend} />
          </div>
        ))}
      </div>

      <EmptyState
        icon={<DashboardIcon />}
        title="Данных за этот период нет"
        body="Попробуйте выбрать другой период или сбросить фильтры"
        action={<TextButton>Сбросить фильтры</TextButton>}
      />
    </AppShell>
  )
}
