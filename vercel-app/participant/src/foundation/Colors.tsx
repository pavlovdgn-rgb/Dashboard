import { PRIMITIVE_COLORS, SEMANTIC_COLORS } from '../foundationData'
import styles from './Foundation.module.css'

function groupBy<T extends { group: string }>(items: T[]): Record<string, T[]> {
  return items.reduce<Record<string, T[]>>((acc, item) => {
    ;(acc[item.group] ??= []).push(item)
    return acc
  }, {})
}

/** Palette — все Primitive- и Semantic-цвета проекта, значения читаются напрямую из src/tokens/*.css. */
export function Colors() {
  const primitiveGroups = groupBy(PRIMITIVE_COLORS)
  const semanticGroups = groupBy(SEMANTIC_COLORS)

  return (
    <div className={styles.page}>
      <div>
        <h1 className="ds-desktop-header-1-semibold">Foundation — Colors</h1>
        <p className="ds-desktop-main-regular" style={{ color: 'var(--color-text-secondary)' }}>
          Источник: ds/foundation.md. Значения читаются из src/tokens/primitives.css и semantics.css.
        </p>
      </div>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Primitive (Слой 1)</h2>
        {Object.entries(primitiveGroups).map(([group, colors]) => (
          <div key={group} style={{ marginBottom: 24 }}>
            <h3 className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)', marginBottom: 8 }}>
              {group}
            </h3>
            <div className={styles.grid}>
              {colors.map((c) => (
                <div className={styles.swatch} key={c.name}>
                  <div className={styles.swatchColor} style={{ background: `var(${c.varName})` }} />
                  <span className={styles.swatchName}>
                    {c.name}
                    <br />
                    {c.varName}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>

      <section>
        <h2 className={`ds-desktop-header-2-medium ${styles.groupTitle}`}>Semantic (Слой 2)</h2>
        {Object.entries(semanticGroups).map(([group, colors]) => (
          <div key={group} style={{ marginBottom: 24 }}>
            <h3 className="ds-desktop-label-medium" style={{ color: 'var(--color-text-secondary)', marginBottom: 8 }}>
              {group}
            </h3>
            <div className={styles.grid}>
              {colors.map((c) => (
                <div className={styles.swatch} key={c.name}>
                  <div className={styles.swatchColor} style={{ background: `var(${c.varName})` }} />
                  <span className={styles.swatchName}>
                    {c.name}
                    <br />
                    {c.varName}
                  </span>
                  <span className={styles.swatchAlias}>→ {c.aliasOf}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>
    </div>
  )
}
