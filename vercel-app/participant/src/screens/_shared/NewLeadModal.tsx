import { useState } from 'react'
import { Button } from '../../components/Button'
import { Dropdown } from '../../components/Dropdown'
import { IconButton } from '../../components/IconButton'
import { Input } from '../../components/Input'
import { TextButton } from '../../components/TextButton'
import { useLeads } from '../../data/LeadsContext'
import { useToast } from '../../data/ToastContext'
import { CHANNEL_LABEL, type LeadChannel } from '../../data/types'
import { CloseIcon } from './icons'

const CHANNELS: LeadChannel[] = ['form', 'call', 'chat']

export interface NewLeadModalProps {
  onClose: () => void
  onCreated?: (leadId: string) => void
}

interface FieldErrors {
  name?: string
  company?: string
  phone?: string
}

const PHONE_DIGITS_MIN = 10

function validatePhone(phone: string): boolean {
  return phone.replace(/\D/g, '').length >= PHONE_DIGITS_MIN
}

/**
 * Форма создания лида вручную — тот же структурный паттерн, что CallLogModal (overlay + scrim + карточка 480px),
 * собрана из тех же базовых компонентов ДС. Единственная форма в продукте, где реально появляется новая запись
 * в мок-слое лидов (Фаза 2/3 директивы wire — «создал → список обновился»).
 */
export function NewLeadModal({ onClose, onCreated }: NewLeadModalProps) {
  const { addLead } = useLeads()
  const { showToast } = useToast()
  const [name, setName] = useState('')
  const [company, setCompany] = useState('')
  const [phone, setPhone] = useState('')
  const [channel, setChannel] = useState<LeadChannel>('form')
  const [errors, setErrors] = useState<FieldErrors>({})
  const [saving, setSaving] = useState(false)

  const handleSubmit = () => {
    const nextErrors: FieldErrors = {}
    if (!name.trim()) nextErrors.name = 'Обязательное поле'
    if (!company.trim()) nextErrors.company = 'Обязательное поле'
    if (!phone.trim()) nextErrors.phone = 'Обязательное поле'
    else if (!validatePhone(phone)) nextErrors.phone = 'Похоже, номер неполный — проверьте формат'
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    setSaving(true)
    window.setTimeout(() => {
      const lead = addLead({ name: name.trim(), company: company.trim(), phone: phone.trim(), channel })
      setSaving(false)
      showToast('success', `Лид «${name.trim()}» добавлен`)
      onCreated?.(lead.id)
      onClose()
    }, 400)
  }

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 100,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div style={{ position: 'absolute', inset: 0, background: 'var(--color-overlay-scrim)', opacity: 'var(--opacity-scrim)' }} onClick={onClose} />

      <div
        style={{
          position: 'relative',
          width: 480,
          display: 'flex',
          flexDirection: 'column',
          background: 'var(--color-bg-surface-primary)',
          borderRadius: 'var(--radius-sm)',
          boxShadow: 'var(--shadow-lg)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', padding: 'var(--space-lg) var(--space-xl)', borderBottom: 'var(--border-width-thin) solid var(--color-border-default)' }}>
          <span className="ds-desktop-header-2-medium" style={{ flex: 1, color: 'var(--color-text-primary)' }}>
            Новый лид
          </span>
          <IconButton icon={<CloseIcon />} aria-label="Закрыть" onClick={onClose} />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
          <Input
            label="Имя"
            showLabel
            value={name}
            onChange={(v) => {
              setName(v)
              if (errors.name) setErrors((e) => ({ ...e, name: undefined }))
            }}
            placeholder="Например: Иванов Пётр"
            error={Boolean(errors.name)}
            showHint={Boolean(errors.name)}
            hint={errors.name}
          />
          <Input
            label="Компания"
            showLabel
            value={company}
            onChange={(v) => {
              setCompany(v)
              if (errors.company) setErrors((e) => ({ ...e, company: undefined }))
            }}
            placeholder="Например: Ленинградский зоопарк"
            error={Boolean(errors.company)}
            showHint={Boolean(errors.company)}
            hint={errors.company}
          />
          <Input
            label="Телефон"
            showLabel
            value={phone}
            onChange={(v) => {
              setPhone(v)
              if (errors.phone) setErrors((e) => ({ ...e, phone: undefined }))
            }}
            placeholder="+7 900 000-00-00"
            error={Boolean(errors.phone)}
            showHint={Boolean(errors.phone)}
            hint={errors.phone}
          />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
              Канал
            </span>
            <Dropdown label={CHANNEL_LABEL[channel]} options={CHANNELS.map((c) => CHANNEL_LABEL[c])} onSelect={(label) => {
              const found = CHANNELS.find((c) => CHANNEL_LABEL[c] === label)
              if (found) setChannel(found)
            }} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-sm)', padding: 'var(--space-lg) var(--space-xl)' }}>
          <TextButton onClick={onClose}>Отмена</TextButton>
          <Button onClick={handleSubmit} loading={saving}>
            Добавить лид
          </Button>
        </div>
      </div>
    </div>
  )
}
