import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from 'react'
import { Toast, type ToastStatus } from '../components/Toast'

interface ToastEntry {
  id: number
  status: ToastStatus
  message: string
}

interface ToastContextValue {
  showToast: (status: ToastStatus, message: string) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

const AUTO_DISMISS_MS = 3200

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastEntry[]>([])
  const idRef = useRef(0)

  const showToast = useCallback((status: ToastStatus, message: string) => {
    idRef.current += 1
    const id = idRef.current
    setToasts((prev) => [...prev, { id, status, message }])
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, AUTO_DISMISS_MS)
  }, [])

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div
        style={{
          position: 'fixed',
          top: 'var(--space-xl)',
          right: 'var(--space-xl)',
          zIndex: 1000,
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--space-sm)',
          alignItems: 'flex-end',
          pointerEvents: 'none',
        }}
      >
        {toasts.map((t) => (
          <Toast key={t.id} status={t.status}>
            {t.message}
          </Toast>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
