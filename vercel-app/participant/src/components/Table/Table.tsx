import type { ReactNode } from 'react'
import { cx } from '../../lib/cx'
import { TableCell, type TableCellType } from '../TableCell'
import styles from './Table.module.css'

export type TableDensity = 'compact' | 'default'

export interface TableColumn {
  key: string
  label: string
  width?: number | 'fill'
  /** Тип ячейки в HEADER-строке — по умолчанию 'header' (лейбл + сортировочный шеврон). Колонке с чекбоксами
   *  сортировка не имеет смысла — задать 'checkbox' (та же ячейка без шеврона, 1:1 с Figma: LeadsTableSection
   *  несёт header row = Type=Checkbox + 6× Type=Header, не 7× Type=Header, см. ds/components.md → TableCell). */
  headerType?: TableCellType
}

export interface TableProps {
  columns: TableColumn[]
  rows: Record<string, ReactNode>[]
  density?: TableDensity
  stickyHeader?: boolean
  /** Опционально — делает строки кликабельными (например, открыть карточку записи). Не влияет на потребителей, которые это не передают. */
  onRowClick?: (rowIndex: number) => void
  /** Опционально — метка для трекера юзер-тестов (data-track), чтобы клик по строке был различим в аналитике. */
  rowDataTrack?: string
}

/** Table — ds/components.md → "Данные / Table". density: compact|default; sticky-header: yes|no. Собрана из TableCell — см. находку в каталоге про зашитый demo-контент готового Figma-компонента. */
export function Table({ columns, rows, density = 'default', stickyHeader = false, onRowClick, rowDataTrack }: TableProps) {
  return (
    <div className={cx(styles.table, density === 'compact' && styles.compact)}>
      <div className={cx(styles.headerRow, stickyHeader && styles.sticky)}>
        {columns.map((col) => (
          <TableCell key={col.key} type={col.headerType ?? 'header'} width={col.width}>
            {col.label}
          </TableCell>
        ))}
      </div>
      {rows.map((row, i) => (
        <div
          className={styles.row}
          key={i}
          onClick={onRowClick ? () => onRowClick(i) : undefined}
          style={onRowClick ? { cursor: 'pointer' } : undefined}
          data-track={onRowClick ? rowDataTrack : undefined}
        >
          {columns.map((col) => (
            <TableCell key={col.key} width={col.width}>
              {row[col.key]}
            </TableCell>
          ))}
        </div>
      ))}
    </div>
  )
}
