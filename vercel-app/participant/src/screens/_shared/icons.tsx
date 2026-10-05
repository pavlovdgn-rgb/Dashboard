/** Плейсхолдер-иконки экранов — простые векторы, не экспорт из Figma (см. границу директивы screens: визуал иконок не здесь). */

export function SearchIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="1.5" />
      <path d="M14 14L11 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

export function PlusIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M8 3V13M3 8H13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

export function PhoneIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path
        d="M3.5 2.5H6L7 5.5L5.5 6.5C6.1 7.8 7.2 8.9 8.5 9.5L9.5 8L12.5 9V11.5C12.5 12.05 12.05 12.5 11.5 12.5C6.5 12.5 2.5 8.5 2.5 3.5C2.5 2.95 2.95 2.5 3.5 2.5Z"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function CloseIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M3 3L13 13M13 3L3 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

export function ArrowLeftIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function KeyIcon({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="8" cy="15" r="4" stroke="currentColor" strokeWidth="1.5" />
      <path d="M11 12L20 3M20 3H16M20 3V7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function AlertIcon({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5" />
      <path d="M12 7V13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="12" cy="16.5" r="1" fill="currentColor" />
    </svg>
  )
}

export function EmptyBoxIcon({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M3 8L12 4L21 8L12 12L3 8Z M3 8V16L12 20M21 8V16L12 20M12 12V20"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  )
}

export function NoMessageIcon({ size = 64 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M4 5H20V16H9L5 19.5V16H4V5Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
      <path d="M3 3L21 21" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

export function DashboardIcon({ size = 64 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="3" width="8" height="8" rx="1" stroke="currentColor" strokeWidth="1.5" />
      <rect x="13" y="3" width="8" height="5" rx="1" stroke="currentColor" strokeWidth="1.5" />
      <rect x="13" y="10" width="8" height="11" rx="1" stroke="currentColor" strokeWidth="1.5" />
      <rect x="3" y="13" width="8" height="8" rx="1" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  )
}

export function ChartIcon({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M4 20V10M12 20V4M20 20V14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  )
}

/**
 * Chat / chat — тот же округлый пузырь-диалог, что в ChatIconButton (ModuleNav) и TitleBar ChatWindow.
 * Path — точная копия из Infotech_UI (node 223:932), не рисованный вручную: прошлая stroke-based
 * версия давала нечитаемую «сломанную дугу», см. фидбек пользователя.
 */
export function ChatBubbleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path
        d="M7.99991 1.33325C7.12443 1.33325 6.25752 1.50569 5.44869 1.84072C4.63985 2.17575 3.90492 2.66682 3.28587 3.28587C2.03562 4.53612 1.33324 6.23181 1.33324 7.99992C1.32742 9.53934 1.86044 11.0323 2.83991 12.2199L1.50658 13.5533C1.41407 13.647 1.35141 13.766 1.32649 13.8954C1.30158 14.0247 1.31552 14.1585 1.36658 14.2799C1.42195 14.3999 1.51171 14.5007 1.62448 14.5695C1.73724 14.6384 1.86791 14.6721 1.99991 14.6666H7.99991C9.76802 14.6666 11.4637 13.9642 12.714 12.714C13.9642 11.4637 14.6666 9.76803 14.6666 7.99992C14.6666 6.23181 13.9642 4.53612 12.714 3.28587C11.4637 2.03563 9.76802 1.33325 7.99991 1.33325ZM7.99991 13.3333H3.60658L4.22658 12.7133C4.35074 12.5883 4.42044 12.4194 4.42044 12.2433C4.42044 12.0671 4.35074 11.8982 4.22658 11.7733C3.35363 10.9013 2.81003 9.75361 2.68837 8.52578C2.56672 7.29795 2.87454 6.06592 3.5594 5.0396C4.24425 4.01328 5.26377 3.25616 6.44425 2.89723C7.62474 2.53831 8.89315 2.59979 10.0334 3.07119C11.1736 3.5426 12.1151 4.39477 12.6975 5.48251C13.2799 6.57026 13.4672 7.82628 13.2273 9.03659C12.9875 10.2469 12.3354 11.3366 11.3823 12.1201C10.4291 12.9035 9.23375 13.3323 7.99991 13.3333Z"
        fill="currentColor"
      />
    </svg>
  )
}

/**
 * Chevron-down — переключатель чата в TitleBar ChatWindow (и шеврон «развернуть» на Minimized-плашке).
 * 16px, не 12px — финальное решение из ds/components.md («История находок по TitleBar»): уменьшение
 * размера не решало путаницу с соседним «свернуть», разнесение по разным кластерам — решило.
 */
export function ChevronDownIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

/** «Свернуть» окно чата — голая линия-минус (не боксед-знак), см. ds/components.md → ChatWindow. */
export function MinusIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <rect x="3" y="7.25" width="10" height="1.5" rx="0.75" fill="currentColor" />
    </svg>
  )
}
