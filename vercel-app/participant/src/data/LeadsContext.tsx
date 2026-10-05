import {taskAction} from '../ux-lab/task'
import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'
import { createInitialLeads } from './leads'
import type { ChatMessage, Lead, LeadChannel, LeadStatus, TimelineEntry } from './types'

export interface NewLeadInput {
  name: string
  company: string
  phone: string
  channel: LeadChannel
}

interface LeadsContextValue {
  leads: Lead[]
  overdueCount: number
  unreadChatsCount: number
  getLead: (id: string) => Lead | undefined
  addLead: (input: NewLeadInput) => Lead
  updateStatus: (id: string, status: LeadStatus) => void
  assignOwner: (id: string, owner: string) => void
  addTimelineEntry: (id: string, entry: Omit<TimelineEntry, 'id' | 'at'>) => void
  addChatMessage: (id: string, message: Omit<ChatMessage, 'id' | 'at'>) => void
}

const LeadsContext = createContext<LeadsContextValue | null>(null)

let uid = 0
function nextId(prefix: string): string {
  uid += 1
  return `${prefix}-${Date.now()}-${uid}`
}

export function LeadsProvider({ children }: { children: ReactNode }) {
  const [leads, setLeads] = useState<Lead[]>(() => createInitialLeads())

  const getLead = useCallback((id: string) => leads.find((l) => l.id === id), [leads])

  const addLead = useCallback((input: NewLeadInput): Lead => {
    const now = Date.now()
    const lead: Lead = {
      id: nextId('lead'),
      channel: input.channel,
      name: input.name,
      company: input.company,
      phone: input.phone,
      email: null,
      source: input.channel === 'form' ? 'Форма, добавлено вручную' : input.channel === 'chat' ? 'Чат, добавлено вручную' : 'Звонок, добавлено вручную',
      score: 50,
      status: 'new',
      owner: null,
      overdue: false,
      createdAt: now,
      lastContactAt: now,
      timeline: [{ id: nextId('tl'), type: 'form', title: 'Лид создан вручную', quote: 'Добавлен менеджером через форму «Новый лид»', at: now }],
      messages: [],
    }
    setLeads((prev) => [lead, ...prev])
    taskAction('lead_created')
    return lead
  }, [])

  const updateStatus = useCallback((id: string, status: LeadStatus) => {
    // overdue относится только к «висящему» статусу callback — любой явный перевод статуса (в т.ч. drag&drop
    // по канбану) резолвит его, не только смена на callback: иначе, например, «Подходит» на просроченном лиде
    // оставлял бы overdue=true на новом статусе Квалифицирован, и бейдж показывал бы неверный «висящий» вид.
    setLeads((prev) => prev.map((l) => (l.id === id ? { ...l, status, overdue: false } : l)))
  }, [])

  const assignOwner = useCallback((id: string, owner: string) => {
    setLeads((prev) => prev.map((l) => (l.id === id ? { ...l, owner } : l)))
  }, [])

  const addTimelineEntry = useCallback((id: string, entry: Omit<TimelineEntry, 'id' | 'at'>) => {
    const now = Date.now()
    setLeads((prev) =>
      prev.map((l) =>
        l.id === id
          ? { ...l, lastContactAt: now, overdue: false, timeline: [{ ...entry, id: nextId('tl'), at: now }, ...l.timeline] }
          : l,
      ),
    )
  }, [])

  const addChatMessage = useCallback((id: string, message: Omit<ChatMessage, 'id' | 'at'>) => {
    if(!message.message.trim()||!leads.some(lead=>lead.id===id))return
    const now = Date.now()
    setLeads((prev) =>
      prev.map((l) => (l.id === id ? { ...l, lastContactAt: now, messages: [...l.messages, { ...message, id: nextId('msg'), at: now }] } : l)),
    )
    if(message.sender==='manager')taskAction('chat_message_sent')
  }, [leads])

  const overdueCount = useMemo(() => leads.filter((l) => l.overdue).length, [leads])

  // Чат «непрочитан», если последнее сообщение в переписке — от клиента: значит менеджер ещё не ответил.
  // Тот же смысл, что «не отвечённых сообщений» из UnreadBadge на ChatIconButton (ds/components.md).
  const unreadChatsCount = useMemo(
    () => leads.filter((l) => l.messages.length > 0 && l.messages[l.messages.length - 1].sender === 'client').length,
    [leads],
  )

  const value = useMemo<LeadsContextValue>(
    () => ({ leads, overdueCount, unreadChatsCount, getLead, addLead, updateStatus, assignOwner, addTimelineEntry, addChatMessage }),
    [leads, overdueCount, unreadChatsCount, getLead, addLead, updateStatus, assignOwner, addTimelineEntry, addChatMessage],
  )

  return <LeadsContext.Provider value={value}>{children}</LeadsContext.Provider>
}

export function useLeads(): LeadsContextValue {
  const ctx = useContext(LeadsContext)
  if (!ctx) throw new Error('useLeads must be used within LeadsProvider')
  return ctx
}
