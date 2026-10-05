import type { ReactNode } from 'react'
import styles from './Header.module.css'

export interface HeaderProps {
  title: string
  userName: string
  avatar?: ReactNode
}

/** Header — ds/components.md → "Навигация / Header". Одиночный компонент, без вариантов: заголовок страницы + блок пользователя. */
export function Header({ title, userName, avatar }: HeaderProps) {
  return (
    <div className={styles.header}>
      <span className={styles.title}>{title}</span>
      <div className={styles.userInfo}>
        {avatar}
        <span className={styles.userName}>{userName}</span>
        <svg className={styles.chevron} viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  )
}
