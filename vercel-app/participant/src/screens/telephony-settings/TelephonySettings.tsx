import { Button } from '../../components/Button'
import { Card } from '../../components/Card'
import { Checkbox } from '../../components/Checkbox'
import { StatusBadge } from '../../components/StatusBadge'
import { TextButton } from '../../components/TextButton'
import { Toast } from '../../components/Toast'
import { SettingsShell } from '../_shared/SettingsShell'

interface Provider {
  name: string
  buttonLabel: string
  variant: 'primary' | 'secondary'
  disabled?: boolean
}

const PROVIDERS: Provider[] = [
  { name: 'Mango Office', buttonLabel: 'Подключено', variant: 'secondary', disabled: true },
  { name: 'Sipuni', buttonLabel: 'Подключить', variant: 'primary' },
  { name: 'Novofon', buttonLabel: 'Подключить', variant: 'primary' },
]

export function TelephonySettings() {
  return (
    <SettingsShell active="Телефония">
      <div style={{ position: 'absolute', top: 100, right: 'var(--space-2xl)' }}>
        <Toast status="success">Провайдер подключён</Toast>
      </div>

      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Телефония</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Подключите облачную АТС для звонков прямо из CRM
        </div>
      </div>

      <div style={{ display: 'flex', gap: 'var(--space-lg)' }}>
        {PROVIDERS.map((p) => (
          <div key={p.name} style={{ flex: 1 }}>
            <Card>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
                <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>{p.name}</span>
                <Button variant={p.variant} disabled={p.disabled}>{p.buttonLabel}</Button>
              </div>
            </Card>
          </div>
        ))}
      </div>

      <div style={{ width: 480 }}>
        <Card>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
            <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>Mango Office — подключение</span>
            <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>API-ключ: ••••••••••••3f2a</span>
            <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>Номер линии: +7 495 123-45-67</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
              <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>Статус:</span>
              <StatusBadge status="success">Активно</StatusBadge>
            </div>
            <div>
              <TextButton>Отключить</TextButton>
            </div>
          </div>
        </Card>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <Checkbox checked label="Всплывающая карточка при входящем звонке с известного номера" />
        <Checkbox checked label="Click-to-call — звонок прямо из карточки лида" />
      </div>
    </SettingsShell>
  )
}
