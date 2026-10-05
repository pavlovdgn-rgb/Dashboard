import { Input } from '../../components/Input'
import { TextButton } from '../../components/TextButton'
import { SettingsShell } from '../_shared/SettingsShell'

export function ChatWidgetSettings() {
  return (
    <SettingsShell active="Чат-виджет">
      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Чат-виджет</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Встройте виджет на сайт одной строкой кода
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>Код для встраивания</span>
        <div style={{ padding: 'var(--space-md)', borderRadius: 'var(--radius-sm)', background: 'var(--color-bg-surface-secondary)' }}>
          <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-on-dark)' }}>
            {'<script src="https://widget.leadgen.app/embed.js" data-id="a1f9c3"></script>'}
          </span>
        </div>
        <div>
          <TextButton>Скопировать</TextButton>
        </div>
      </div>

      <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', maxWidth: 700 }}>
        Виджет появится в правом нижнем углу вашего сайта после установки скрипта — так, как показано на экране ChatWidget.
      </span>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>Приветственное сообщение</span>
        <div style={{ width: 420 }}>
          <Input type="textarea" showLabel={false} value="Здравствуйте! Чем можем помочь?" />
        </div>
      </div>
    </SettingsShell>
  )
}
