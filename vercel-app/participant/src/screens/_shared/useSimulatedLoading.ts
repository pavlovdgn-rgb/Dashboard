import { useEffect, useState } from 'react'

/**
 * Мок «загрузки» при заходе на экран — без бэкенда данные и так готовы синхронно, но продукт должен показывать
 * loading-состояние как реальное действие в процессе (Фаза 4 директивы wire), а не только на отдельном демо-route.
 */
export function useSimulatedLoading(ms = 600): boolean {
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    const timer = window.setTimeout(() => setLoading(false), ms)
    return () => window.clearTimeout(timer)
  }, [ms])
  return loading
}
