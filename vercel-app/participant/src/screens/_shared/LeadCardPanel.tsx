import { useState } from 'react'
import { Button } from '../../components/Button'
import { Dropdown } from '../../components/Dropdown'
import { StatusBadge } from '../../components/StatusBadge'
import { TextButton } from '../../components/TextButton'
import { TimelineItem } from '../../components/TimelineItem'
import { useLeads } from '../../data/LeadsContext'
import { MANAGERS } from '../../data/leads'
import { useToast } from '../../data/ToastContext'
import { formatRelativeTime } from '../../data/format'
import { STATUS_LABEL, STATUS_TONE, type Lead, type LeadStatus } from '../../data/types'
import { CallLogModalContent } from './CallLogModalContent'
import { CloseIcon } from './icons'
import styles from './LeadCardPanel.module.css'

const STATUS_ACTIONS: { label: string; status: LeadStatus }[] = [
  { label: 'Подходит', status: 'qualified' },
  { label: 'Не подходит', status: 'rejected' },
  { label: 'Перезвонить', status: 'callback' },
]

/** Высота ModuleNav — 48px паддинга + 44px самый высокий дочерний элемент (ChatIconButton) + 1px нижний
 * бордер = 93 (не 92 — бордер добавляет высоту поверх content+padding даже при box-sizing:border-box,
 * когда height задан не явно, а auto, как здесь; проверено getBoundingClientRect(), см. находку
 * 2026-08-29 — при 92 панель перекрывала последний пиксель бордера-разделителя хедера). Панель начинается
 * под хедером, не перекрывает его. См. ds/screens/lead-card.md → находку про панель-под-хедером. */
export const HEADER_HEIGHT = 93
const PANEL_WIDTH = 480

export interface LeadCardPanelProps {
  lead: Lead
  onClose: () => void
  /** «Написать в чат» в ActionsRow — вызывает глобальный `useChatWindow().openChat(lead.id)` (см. ChatWindowContext),
   *  панель сама никуда не навигирует и не знает о чате ничего, кроме этого колбэка. */
  onWriteChat: () => void
}

/**
 * Slide-over карточка лида — вынесена из `LeadCard` (route-экран) в переиспользуемую панель, чтобы
 * LeadsTable/LeadsKanban могли открывать её поверх СЕБЯ (локальный state, без navigate) и оставаться
 * на своём route: раньше клик по строке/карточке всегда уводил на `/lead-card` с зашитым бэкдропом
 * LeadsKanban — на странице «Лиды» это подменяло активный пункт меню на «Канбан» и визуально телепортировало
 * пользователя. По той же причине «Написать в чат» больше не делает `navigate('/chat-panel')` сам — это
 * тоже уводило со страницы «Лиды» на канбан-бэкдроп чата. Чат теперь отдельное глобальное плавающее окно
 * (ChatWindow/GlobalChatWindow), не докнутая панель поверх этого же слота — может быть открыто одновременно
 * с самой карточкой лида, см. `onWriteChat`.
 */
export function LeadCardPanel({ lead, onClose, onWriteChat }: LeadCardPanelProps) {
  const { updateStatus, assignOwner } = useLeads()
  const { showToast } = useToast()
  const [callLogOpen, setCallLogOpen] = useState(false)

  return (
    <>
      {/* Крестик закрытия — снаружи панели, слева от её границы (не внутри Header) — так у пользователя
          короче путь курсора до закрытия: панель докнута справа экрана, крестик у правого края раньше
          оказывался у самого края браузера. Абсолютно спозиционирован относительно того же fixed-контекста,
          что и сама панель (см. HEADER_HEIGHT ниже — экран под панелью). Стоит в зоне, которую теперь
          закрывает InteractionBlocker-затемнение — color/text/on-dark (не text-icons), иначе теряется на
          тёмном фоне, см. ds/CONTRACT.md → «Крестик закрытия SlideOverPanel посветлел». Едет вместе с
          панелью при появлении (slideInCloseButton, см. LeadCardPanel.module.css) — крестик и панель это
          два разных fixed-элемента, синхронизированы по расстоянию, не по времени/спрингу. */}
      <button
        type="button"
        aria-label="Закрыть"
        onClick={onClose}
        className={styles.closeButton}
        style={{
          position: 'fixed',
          top: HEADER_HEIGHT + 8,
          right: PANEL_WIDTH + 8,
          width: 28,
          height: 28,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: 'none',
          borderRadius: 'var(--radius-sm)',
          background: 'transparent',
          color: 'var(--color-text-on-dark)',
          cursor: 'pointer',
          zIndex: 41,
        }}
      >
        <CloseIcon />
      </button>

      <div
        className={styles.panel}
        style={{
          position: 'fixed',
          // Начинается под ModuleNav (HEADER_HEIGHT), не с самого верха экрана — иначе панель полностью
          // перекрывает хедер (заголовок, статус, иконку чата с бейджем непрочитанных, аватар) всё время,
          // пока открыта.
          top: HEADER_HEIGHT,
          right: 0,
          width: PANEL_WIDTH,
          height: `calc(100vh - ${HEADER_HEIGHT}px)`,
          background: 'var(--color-bg-surface-primary)',
          boxShadow: 'var(--shadow-panel)',
          display: 'flex',
          flexDirection: 'column',
          overflowY: 'auto',
          zIndex: 40,
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-xs)',
            padding: 'var(--space-lg) var(--space-xl)',
            borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
            flexShrink: 0,
          }}
        >
          <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
            {lead.name}, «{lead.company}»
          </span>
          <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
            Источник: {lead.source}
          </span>
        </div>

        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-sm)',
            padding: 'var(--space-lg) var(--space-xl)',
            borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
            flexShrink: 0,
          }}
        >
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>
            Телефон: {lead.phone}
          </span>
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>
            Email: {lead.email ?? 'не указан'}
          </span>
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>
            Источник: {lead.source}
          </span>
        </div>

        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-md)',
            padding: 'var(--space-lg) var(--space-xl)',
            borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
            flexShrink: 0,
          }}
        >
          <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
            Скор: {lead.score}
          </span>
          <div>
            <StatusBadge status={lead.overdue ? 'error' : STATUS_TONE[lead.status]}>
              {lead.overdue ? `${STATUS_LABEL[lead.status]} · Просрочен на 1 день` : STATUS_LABEL[lead.status]}
            </StatusBadge>
          </div>
          {/* flexWrap — 3 кнопки почти впритык умещаются в 480px панели минус паддинги (найдено 2026-08-29,
              пользователь: «почему кнопка не помещается в 2 строки», TextButton заодно получил white-space:nowrap
              как у Button, но этого мало — при чуть более широком шрифте/масштабе строка всё равно не влезает;
              перенос ЦЕЛОЙ кнопки на новую строку, а не текста внутри неё). */}
          <div style={{ display: 'flex', gap: 'var(--space-sm)', flexWrap: 'wrap' }}>
            {STATUS_ACTIONS.map((action) => (
              <TextButton
                key={action.label}
                onClick={() => {
                  updateStatus(lead.id, action.status)
                  showToast('success', `Статус обновлён: ${action.label}`)
                }}
              >
                {action.label}
              </TextButton>
            ))}
          </div>
        </div>

        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-sm)',
            padding: 'var(--space-lg) var(--space-xl)',
            borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
            flexShrink: 0,
          }}
        >
          <span className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)' }}>
            Ответственный
          </span>
          <Dropdown
            label={lead.owner ?? 'не назначен'}
            options={MANAGERS}
            onSelect={(owner) => {
              assignOwner(lead.id, owner)
              showToast('success', `Ответственный назначен: ${owner}`)
            }}
          />
        </div>

        <div
          style={{
            display: 'flex',
            gap: 'var(--space-sm)',
            flexWrap: 'wrap',
            padding: 'var(--space-lg) var(--space-xl)',
            borderBottom: 'var(--border-width-thin) solid var(--color-border-default)',
            flexShrink: 0,
          }}
        >
          <Button variant="secondary" onClick={() => showToast('info', `Звонок инициирован: ${lead.phone}`)}>
            Позвонить
          </Button>
          <Button variant="secondary" onClick={() => setCallLogOpen(true)}>
            Записать звонок
          </Button>
          <Button variant="secondary" onClick={onWriteChat}>
            Написать в чат
          </Button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)', padding: 'var(--space-lg) var(--space-xl)', flex: 1 }}>
          <span className="ds-desktop-header-2-medium" style={{ color: 'var(--color-text-primary)' }}>
            История взаимодействий
          </span>
          {lead.timeline.map((entry) => (
            <TimelineItem
              key={entry.id}
              type={entry.type}
              title={entry.title}
              meta={entry.type === 'call' ? `${formatRelativeTime(entry.at)} — ${lead.owner ?? 'не назначен'}` : formatRelativeTime(entry.at)}
              quote={entry.quote}
            />
          ))}
        </div>
      </div>

      {callLogOpen && <CallLogModalContent lead={lead} onClose={() => setCallLogOpen(false)} />}
    </>
  )
}
