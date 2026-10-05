import { TYPE_ROWS } from '../foundationData'
import styles from './Foundation.module.css'

/** Типографика — все Text Styles проекта, шрифт Montserrat, letter-spacing 0 везде. Цвет не входит в TextStyle (как и в Figma). */
export function Typography() {
  return (
    <div className={styles.page}>
      <div>
        <h1 className="ds-desktop-header-1-semibold">Foundation — Typography</h1>
        <p className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
          Источник: ds/foundation.md. Классы — src/tokens/typography.css. Шрифт: Montserrat (Regular/Medium/SemiBold).
        </p>
      </div>
      <div>
        {TYPE_ROWS.map((t) => (
          <div className={styles.typeRow} key={t.className}>
            <span className={styles.typeRowLabel}>{t.label}</span>
            <span className={t.className}>Пример текста Aa Яя 123</span>
          </div>
        ))}
      </div>
    </div>
  )
}
