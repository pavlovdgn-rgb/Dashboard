import { cx } from '../../lib/cx'
import styles from './NavListItem.module.css'

export interface NavListItemProps {
  active?: boolean
  pinned?: boolean
  onClick?: () => void
  children: string
}

/**
 * NavListItem — ds/components.md → "Навигация / NavListItem". State: Default|Hover|Active; Pinned: No|Yes (матрица 3×2).
 * Сверено напрямую с реальным экземпляром в Figma (191:2641-2644, Tile/Sidebar-Expanded): Active красит только текст в
 * brand/primary (не фон), Pin — User Interface/Pin, серая (color/text/icons), справа, видна только при Pinned=Yes.
 */
export function NavListItem({ active = false, pinned = false, onClick, children }: NavListItemProps) {
  return (
    <button type="button" className={cx(styles.item, active && styles.active)} onClick={onClick}>
      <span>{children}</span>
      {pinned && (
        // User Interface / Pin — тот же реальный вектор, что на рельсе Sidebar (I179:2653;139:1673)
        <svg className={styles.pin} viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path
            d="M4.45676 7.29341C5.55609 6.19404 6.86251 6.22445 8.28251 7.00316L13.5916 4.06045L13.2912 1.99451L18.0052 6.70854L15.944 6.41279L12.9965 11.7172C13.7396 13.2329 13.8057 14.4436 12.7063 15.543C12.7063 15.543 10.9312 13.7679 9.46542 12.3021L2.68457 17.3152L7.68255 10.5192C6.21672 9.05337 4.45676 7.29341 4.45676 7.29341Z"
            fill="currentColor"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
        </svg>
      )}
    </button>
  )
}
