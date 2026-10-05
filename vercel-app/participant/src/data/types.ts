export type LeadChannel = 'form' | 'call' | 'chat'
export type LeadStatus = 'new' | 'in_progress' | 'callback' | 'qualified' | 'rejected'
export type MessageSender = 'client' | 'manager'

export interface TimelineEntry {
  id: string
  type: 'call' | 'form' | 'chat'
  title: string
  quote: string
  at: number
}

export interface ChatMessage {
  id: string
  sender: MessageSender
  authorLabel: string
  message: string
  at: number
}

export interface Lead {
  id: string
  channel: LeadChannel
  name: string
  company: string
  phone: string
  email: string | null
  source: string
  score: number
  status: LeadStatus
  owner: string | null
  overdue: boolean
  createdAt: number
  lastContactAt: number
  timeline: TimelineEntry[]
  messages: ChatMessage[]
}

export const CHANNEL_LABEL: Record<LeadChannel, string> = {
  form: 'Форма',
  call: 'Звонок',
  chat: 'Чат',
}

export const STATUS_LABEL: Record<LeadStatus, string> = {
  new: 'Новый',
  in_progress: 'В работе',
  callback: 'Перезвонить',
  qualified: 'Квалифицирован',
  rejected: 'Не подходит',
}

export const STATUS_TONE: Record<LeadStatus, 'success' | 'error' | 'warning' | 'neutral'> = {
  new: 'neutral',
  in_progress: 'warning',
  callback: 'error',
  qualified: 'success',
  rejected: 'error',
}
