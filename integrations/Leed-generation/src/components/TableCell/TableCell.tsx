import type { ReactNode, CSSProperties } from 'react'
import { cx } from '../../lib/cx'
import styles from './TableCell.module.css'

export type TableCellType = 'header' | 'header-icon' | 'text' | 'status' | 'checkbox' | 'actions' | 'toggle'

export interface TableCellProps {
  type?: TableCellType
  children?: ReactNode
  disabled?: boolean
  width?: number | 'fill'
}

/** Сортировочная стрелка — «Arrows / down arrow small», тот же вектор, что шеврон Dropdown/Select. Показывается на каждой Header-ячейке, сверено в Figma (SortIcon рядом с лейблом на всех Header-инстансах). */
function SortIcon() {
  return (
    <svg className={styles.sortIcon} viewBox="0 0 12 12" fill="none" aria-hidden="true">
      <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

/** Table Cell — ds/components.md → "Данные / Table Cell". Type переключает роль ячейки; Table собирается напрямую из этих ячеек, не из Table-компонента с зашитым demo-контентом. */
export function TableCell({ type = 'text', children, disabled = false, width }: TableCellProps) {
  const style: CSSProperties = width === 'fill' ? { flex: 1 } : width ? { width, flexShrink: 0 } : {}
  const isHeader = type === 'header' || type === 'header-icon'
  return (
    <div className={cx(styles.cell, isHeader && styles.header, disabled && styles.disabled)} style={style}>
      {isHeader ? (
        <span className={styles.headerContent}>
          {children}
          <SortIcon />
        </span>
      ) : (
        children
      )}
    </div>
  )
}
