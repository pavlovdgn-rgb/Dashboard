import { useMemo, useState } from 'react'
import { MANAGERS } from '../../data/leads'
import { CHANNEL_LABEL, type Lead, type LeadChannel } from '../../data/types'

export type ChannelFilter = 'all' | LeadChannel
export type OwnerFilter = 'all' | 'unassigned' | string

export const CHANNEL_OPTIONS: { value: ChannelFilter; label: string }[] = [
  { value: 'all', label: 'Все' },
  { value: 'form', label: CHANNEL_LABEL.form },
  { value: 'call', label: CHANNEL_LABEL.call },
  { value: 'chat', label: CHANNEL_LABEL.chat },
]

export const OWNER_OPTIONS: { value: OwnerFilter; label: string }[] = [
  { value: 'all', label: 'Все' },
  ...MANAGERS.map((m) => ({ value: m, label: m })),
  { value: 'unassigned', label: 'Не назначен' },
]

/** Общая логика фильтрации LeadsTable/LeadsKanban: поиск по имени/компании + канал + ответственный, читают из единого мок-слоя лидов. */
export function useLeadFilters(leads: Lead[]) {
  const [search, setSearch] = useState('')
  const [channel, setChannel] = useState<ChannelFilter>('all')
  const [owner, setOwner] = useState<OwnerFilter>('all')

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase()
    return leads.filter((lead) => {
      if (query) {
        const haystack = `${lead.name} ${lead.company}`.toLowerCase()
        if (!haystack.includes(query)) return false
      }
      if (channel !== 'all' && lead.channel !== channel) return false
      if (owner === 'unassigned' && lead.owner !== null) return false
      if (owner !== 'all' && owner !== 'unassigned' && lead.owner !== owner) return false
      return true
    })
  }, [leads, search, channel, owner])

  const isFiltered = search.trim() !== '' || channel !== 'all' || owner !== 'all'

  const reset = () => {
    setSearch('')
    setChannel('all')
    setOwner('all')
  }

  return { search, setSearch, channel, setChannel, owner, setOwner, filtered, isFiltered, reset }
}
