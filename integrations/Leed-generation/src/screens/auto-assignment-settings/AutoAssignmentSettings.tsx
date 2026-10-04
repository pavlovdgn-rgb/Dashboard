import { Checkbox } from '../../components/Checkbox'
import { Input } from '../../components/Input'
import { Radio } from '../../components/Radio'
import { Toggle } from '../../components/Toggle'
import { SettingsShell } from '../_shared/SettingsShell'

const PARTICIPANTS = ['Игорь Петров', 'Анна Смирнова', 'Дмитрий Волков']

export function AutoAssignmentSettings() {
  return (
    <SettingsShell active="Автоназначение">
      <div>
        <div className="ds-desktop-header-1-semibold" style={{ color: 'var(--color-text-primary)' }}>Автоназначение лидов</div>
        <div className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)', marginTop: 'var(--space-xs)' }}>
          Кто получает новый лид, если менеджер не забрал его сам
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-md)' }}>
        <Toggle on aria-label="Включить автоназначение" />
        <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>Включить автоназначение</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
          <Radio selected={false} label="Round-robin — по очереди, поровну между менеджерами" />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
          <Radio selected label="По нагрузке — тому, у кого сейчас меньше активных лидов" />
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
        <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>Лид не может оставаться без ответственного дольше</span>
        <div style={{ width: 64 }}>
          <Input value="15" showLabel={false} />
        </div>
        <span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>минут</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
        <span className="ds-desktop-main-medium" style={{ color: 'var(--color-text-primary)' }}>Участвуют в автораспределении</span>
        {PARTICIPANTS.map((name) => (
          <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
            <Checkbox checked label={<span className="ds-desktop-main-regular" style={{ color: 'var(--color-text-primary)' }}>{name}</span>} />
          </div>
        ))}
      </div>
    </SettingsShell>
  )
}
