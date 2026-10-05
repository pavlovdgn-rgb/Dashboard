import type { ReactNode } from 'react'
import { Button } from '../../../components/Button'
import { Dropdown } from '../../../components/Dropdown'
import { Input } from '../../../components/Input'
import { TextButton } from '../../../components/TextButton'
import { CHANNEL_OPTIONS, OWNER_OPTIONS, type ChannelFilter, type OwnerFilter } from '../../_shared/useLeadFilters'
import { PlusIcon, SearchIcon } from '../../_shared/icons'

export interface LeadsFiltersBarProps {
  search?: string
  onSearchChange?: (value: string) => void
  channel?: ChannelFilter
  onChannelChange?: (value: ChannelFilter) => void
  owner?: OwnerFilter
  onOwnerChange?: (value: OwnerFilter) => void
  onReset?: () => void
  onNewLead?: () => void
  extra?: ReactNode
}

/**
 * Строка фильтров LeadsTable/LeadsKanban/Dashboard: поиск + 3 дропдауна + «Сбросить всё» + CTA «Новый лид» —
 * управляемая, читает/меняет состояние фильтров экрана-родителя (см. `useLeadFilters`). Все пропы опциональны
 * с no-op дефолтами — так статичные demo-роуты loading/empty-состояний (`LoadingState`, `EmptyLeadsTable` и т.п.,
 * реестр экранов) продолжают рендериться без правок, просто без реальной фильтрации.
 */
export function LeadsFiltersBar({
  search = '',
  onSearchChange = () => {},
  channel = 'all',
  onChannelChange = () => {},
  owner = 'all',
  onOwnerChange = () => {},
  onReset = () => {},
  onNewLead = () => {},
  extra,
}: LeadsFiltersBarProps) {
  const channelLabel = CHANNEL_OPTIONS.find((o) => o.value === channel)?.label ?? 'Все'
  const ownerLabel = OWNER_OPTIONS.find((o) => o.value === owner)?.label ?? 'Все'

  return (
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
        flexShrink: 0,
      }}
    >
      <div style={{ width: 320, flexShrink: 0 }}>
        <Input value={search} onChange={onSearchChange} placeholder="Найти лида" icon={<SearchIcon />} showIcon />
      </div>
      <Dropdown
        label={`Канал: ${channelLabel}`}
        options={CHANNEL_OPTIONS.map((o) => o.label)}
        onSelect={(label) => {
          const found = CHANNEL_OPTIONS.find((o) => o.label === label)
          if (found) onChannelChange(found.value)
        }}
      />
      <Dropdown
        label={`Менеджер: ${ownerLabel}`}
        options={OWNER_OPTIONS.map((o) => o.label)}
        onSelect={(label) => {
          const found = OWNER_OPTIONS.find((o) => o.label === label)
          if (found) onOwnerChange(found.value)
        }}
      />
      {extra ?? <Dropdown label="Период: Месяц" />}
      <TextButton onClick={onReset}>Сбросить всё</TextButton>
      <span style={{ flex: '1 1 0%' }} />
      <Button leftIcon={<PlusIcon />} onClick={onNewLead} data-track="new-lead-button">
        Новый лид
      </Button>
    </div>
  )
}
