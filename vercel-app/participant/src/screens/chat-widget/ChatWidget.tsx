import { IconButton } from '../../components/IconButton'
import { Input } from '../../components/Input'
import { MessageBubble } from '../../components/MessageBubble'
import { CloseIcon } from '../_shared/icons'

export function ChatWidget() {
  return (
    <div style={{ position: 'relative', minHeight: '100vh', background: 'var(--color-bg-page)' }}>
      <span
        className="ds-desktop-label-medium"
        style={{ position: 'absolute', top: 'var(--space-lg)', left: 'var(--space-lg)', color: 'var(--color-text-secondary)' }}
      >
        Условный фон: сайт клиента (вне зоны ответственности модуля)
      </span>

      <div
        style={{
          position: 'absolute',
          right: 'var(--space-2xl)',
          bottom: 120,
          width: 360,
          height: 460,
          display: 'flex',
          flexDirection: 'column',
          background: 'var(--color-bg-surface-primary)',
          borderRadius: 'var(--radius-sm)',
          boxShadow: 'var(--shadow-lg)',
          overflow: 'hidden',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xs)', padding: 'var(--space-lg)', borderBottom: 'var(--border-width-thin) solid var(--color-border-default)', flexShrink: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
            <span className="ds-desktop-header-2-medium" style={{ flex: 1, color: 'var(--color-text-primary)' }}>Название компании</span>
            <IconButton icon={<CloseIcon />} aria-label="Закрыть" />
          </div>
          <span className="ds-desktop-breadcrumbs-regular" style={{ color: 'var(--color-text-secondary)' }}>Есть вопросы? Напишите нам</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', padding: 'var(--space-md)', flex: 1 }}>
          <MessageBubble sender="manager" meta="Онлайн-консультант" message="Здравствуйте! Чем можем помочь?" />
        </div>

        <div style={{ padding: 'var(--space-md)', borderTop: 'var(--border-width-thin) solid var(--color-border-default)', flexShrink: 0 }}>
          <Input value="Напишите сообщение..." />
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          right: 'var(--space-2xl)',
          bottom: 'var(--space-2xl)',
          width: 64,
          height: 64,
          borderRadius: 'var(--radius-full)',
          background: 'var(--color-brand-primary)',
          boxShadow: 'var(--shadow-lg)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span style={{ color: 'var(--color-text-on-button)', fontSize: 24, fontWeight: 600 }}>?</span>
        <span
          style={{
            position: 'absolute',
            top: -2,
            right: -2,
            width: 18,
            height: 18,
            borderRadius: 'var(--radius-full)',
            background: 'var(--color-system-error)',
            color: 'var(--color-text-on-button)',
            fontSize: 11,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          1
        </span>
      </div>
    </div>
  )
}
