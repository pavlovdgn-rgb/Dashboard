const MINUTE = 60_000
const HOUR = 60 * MINUTE
const DAY = 24 * HOUR

/** Человекочитаемое «N назад» для меток последнего контакта/таймлайна — считается от реального now(), не хранится строкой. */
export function formatRelativeTime(at: number, now: number = Date.now()): string {
  const diff = Math.max(0, now - at)
  if (diff < MINUTE) return 'только что'
  if (diff < HOUR) {
    const m = Math.round(diff / MINUTE)
    return `${m} мин назад`
  }
  if (diff < DAY) {
    const h = Math.round(diff / HOUR)
    return `${h} ${pluralHours(h)} назад`
  }
  const d = Math.round(diff / DAY)
  return `${d} ${pluralDays(d)} назад`
}

function pluralHours(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return 'час'
  if ([2, 3, 4].includes(mod10) && ![12, 13, 14].includes(mod100)) return 'часа'
  return 'часов'
}

function pluralDays(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return 'день'
  if ([2, 3, 4].includes(mod10) && ![12, 13, 14].includes(mod100)) return 'дня'
  return 'дней'
}

export function minutesAgo(n: number): number {
  return Date.now() - n * MINUTE
}
export function hoursAgo(n: number): number {
  return Date.now() - n * HOUR
}
export function daysAgo(n: number): number {
  return Date.now() - n * DAY
}
