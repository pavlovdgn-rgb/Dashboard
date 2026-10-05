import { useNavigate } from 'react-router-dom'
import { Button } from '../../components/Button'
import { CenteredMessageScreen } from '../_shared/CenteredMessageScreen'
import { AlertIcon } from '../_shared/icons'

export function ErrorState() {
  const navigate = useNavigate()
  return (
    <CenteredMessageScreen
      icon={<AlertIcon size={160} />}
      iconColor="var(--color-system-error)"
      title="Не удалось загрузить данные"
      body="Проверьте подключение к интернету или повторите попытку. Если ошибка повторяется — обратитесь к администратору."
      action={
        <Button variant="secondary" onClick={() => navigate('/leads-table')}>
          Повторить попытку
        </Button>
      }
      contentWidth={844}
    />
  )
}
