import { Link } from 'react-router-dom'
import { TextButton } from '../components/TextButton'
import { screens } from './registry'
import styles from './ScreensIndex.module.css'

export function ScreensIndex() {
  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={`ds-desktop-header-1-medium ${styles.title}`}>Генератор лидов — экраны</h1>
        <p className={`ds-desktop-main-regular ${styles.subtitle}`}>
          Статичные экраны, собранные из дизайн-системы. Логика и данные — отдельный шаг.
        </p>
      </div>

      <div className={styles.grid}>
        {screens.map((screen) => (
          <Link key={screen.id} to={screen.route} className={styles.tile}>
            <span className={`ds-desktop-main-semibold ${styles.tileName}`}>{screen.name}</span>
            <span className={`ds-desktop-label-medium ${styles.tileDescription}`}>{screen.description}</span>
            <span className={`ds-desktop-label-medium ${styles.tileRoute}`}>{screen.route}</span>
          </Link>
        ))}
      </div>

      <div className={styles.footer}>
        <Link to="/showcase" style={{ textDecoration: 'none' }}>
          <TextButton>Открыть DS-витрину (Showcase)</TextButton>
        </Link>
      </div>
    </div>
  )
}
