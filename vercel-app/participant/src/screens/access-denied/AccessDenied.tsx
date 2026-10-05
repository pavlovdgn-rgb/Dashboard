import { useNavigate } from 'react-router-dom'
import { TextButton } from '../../components/TextButton'
import { CenteredMessageScreen } from '../_shared/CenteredMessageScreen'
import { KeyIcon } from '../_shared/icons'

export function AccessDenied() {
  const navigate = useNavigate()
  return (
    <CenteredMessageScreen
      icon={<KeyIcon size={160} />}
      title="Доступ ограничен"
      body="Раздел «Настройки» доступен только администраторам. Ваша роль: Менеджер."
      action={<TextButton onClick={() => navigate('/leads-table')}>Вернуться к лидам</TextButton>}
    />
  )
}
