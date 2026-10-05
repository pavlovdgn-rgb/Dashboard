import { BORDER_WIDTH_TOKENS, RADIUS_TOKENS, SHADOW_TOKENS, SPACING_TOKENS } from '../foundationData'
import styles from './Foundation.module.css'

/** Отступы, радиусы, толщина обводки, тени — примитивы шкалы, не цвета. */
export function Spacing() {
  return (
    <div className={styles.page}>
      <div>
        <h1 className="ds-desktop-header-1-semibold">Foundation — Spacing, Radius, Shadows</h1>
        <p className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
          Источник: ds/foundation.md. Значения — src/tokens/primitives.css.
        </p>
      </div>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Spacing</h2>
        {SPACING_TOKENS.map((t) => (
          <div className={styles.scaleRow} key={t.name}>
            <span className={styles.scaleLabel}>{t.name}</span>
            <span className={styles.scaleValue}>{t.px}px</span>
            <div className={styles.spacingBox} style={{ width: `var(${t.varName})` }} />
          </div>
        ))}
      </section>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Radius</h2>
        <div style={{ display: 'flex', gap: 24 }}>
          {RADIUS_TOKENS.map((t) => (
            <div className={styles.swatch} key={t.name}>
              <div className={styles.radiusBox} style={{ borderRadius: `var(${t.varName})` }} />
              <span className={styles.swatchName}>
                {t.name} — {t.px}px
              </span>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Border Width</h2>
        {BORDER_WIDTH_TOKENS.map((t) => (
          <div className={styles.scaleRow} key={t.name}>
            <span className={styles.scaleLabel}>{t.name}</span>
            <span className={styles.scaleValue}>{t.px}px</span>
            <div style={{ width: 200, borderBottom: `var(${t.varName}) solid var(--color-text-primary)` }} />
          </div>
        ))}
      </section>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Shadows (Effect Styles)</h2>
        <div style={{ display: 'flex', gap: 32, padding: '16px 0' }}>
          {SHADOW_TOKENS.map((t) => (
            <div className={styles.swatch} key={t.name}>
              <div className={styles.shadowBox} style={{ boxShadow: `var(${t.varName})` }} />
              <span className={styles.swatchName}>{t.name}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
