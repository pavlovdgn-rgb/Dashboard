import { useState } from 'react'
import { Button } from '../../components/Button'
import { Dropdown } from '../../components/Dropdown'
import { IconButton } from '../../components/IconButton'
import { Input } from '../../components/Input'
import { Radio } from '../../components/Radio'
import { TextButton } from '../../components/TextButton'
import { useLeads } from '../../data/LeadsContext'
import { useToast } from '../../data/ToastContext'
import type { Lead } from '../../data/types'
import { CloseIcon } from './icons'

const RESULT_OPTIONS = ['Договорились о встрече', 'Перезвонить позже', 'Не дозвонились', 'Клиент отказался']

export interface CallLogModalContentProps {
  lead: Lead
  onClose: () => void
  onSaved?: () => void
  initialDirection?: 'in' | 'out'
}

/**
 * Общая форма «Записать звонок» — используется и как отдельный route-экран (`screens/call-log-modal`, реестр),
 * и как overlay поверх LeadCard/ChatPanel по кнопке «Записать звонок» (ActionsRow), привязанная к конкретному лиду.
 * Комментарий — обязательное поле; пустой ввод показывает Type=Textarea/State=Error (документированный вариант
 * ds/components.md → Input, найден аудитом `screens_audit` как ни разу не применённый на живом экране — теперь применён).
 */
export function CallLogModalContent({ lead, onClose, onSaved, initialDirection = 'out' }: CallLogModalContentProps) {
  const { addTimelineEntry } = useLeads()
  const { showToast } = useToast()
  const [direction, setDirection] = useState<'in' | 'out'>(initialDirection)
  const [result, setResult] = useState(RESULT_OPTIONS[1])
  const [comment, setComment] = useState('')
  const [commentError, setCommentError] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleSubmit = () => {
    if (!comment.trim()) {
      setCommentError(true)
      return
    }
    setSaving(true)
    window.setTimeout(() => {
      addTimelineEntry(lead.id, {
        type: 'call',
        title: direction === 'in' ? 'Звонок входящий (ручной лог)' : 'Звонок исходящий (ручной лог)',
        quote: comment.trim(),
      })
      setSaving(false)
      showToast('success', 'Звонок записан')
      onSaved?.()
      onClose()
    }, 400)
  }

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
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
            Записать звонок
          </span>
          <IconButton icon={<CloseIcon />} aria-label="Закрыть" onClick={onClose} />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)', padding: 'var(--space-lg) var(--space-xl)', borderBottom: 'var(--border-width-thin) solid var(--color-border-default)' }}>
          <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>
            {lead.name}, {lead.company}
          </span>
          <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
            {lead.phone}
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', padding: 'var(--space-xl)' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
              Направление
            </span>
            <div style={{ display: 'flex', gap: 'var(--space-xl)' }}>
              <Radio selected={direction === 'in'} onChange={() => setDirection('in')} label="Входящий" />
              <Radio selected={direction === 'out'} onChange={() => setDirection('out')} label="Исходящий" />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
              Результат
            </span>
            <Dropdown label={result} options={RESULT_OPTIONS} onSelect={setResult} />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
              Комментарий
            </span>
            <Input
              type="textarea"
              showLabel={false}
              value={comment}
              onChange={(v) => {
                setComment(v)
                if (commentError && v.trim()) setCommentError(false)
              }}
              placeholder="Например: обсудили условия поставки, попросил прислать КП"
              error={commentError}
              showHint={commentError}
              hint="Обязательное поле — опишите содержание разговора"
            />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-sm)', padding: 'var(--space-lg) var(--space-xl)' }}>
          <TextButton onClick={onClose}>Отмена</TextButton>
          <Button onClick={handleSubmit} loading={saving}>
            Сохранить
          </Button>
        </div>
      </div>
    </div>
  )
}
