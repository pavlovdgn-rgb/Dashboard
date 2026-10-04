import { useNavigate } from 'react-router-dom'
import { Button } from '../../components/Button'
import { CenteredMessageScreen } from '../_shared/CenteredMessageScreen'

export function NotFound404() {
  const navigate = useNavigate()
  return (
    <CenteredMessageScreen
      icon={<span style={{ fontSize: 56, fontWeight: 600, lineHeight: '100%', color: 'var(--color-text-primary)' }}>404</span>}
      title="Лид не найден"
      body="Возможно, лид был удалён или у вас нет доступа к нему"
      action={
        <Button variant="secondary" onClick={() => navigate('/leads-table')}>
          Вернуться к таблице лидов
        </Button>
      }
      contentWidth={393}
    />
  )
}
