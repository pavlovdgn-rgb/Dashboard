export interface SkeletonBarProps {
  width: number | string
  height: number
  radius?: string
}

/** Полоса-заглушка контента в loading-состояниях. */
export function SkeletonBar({ width, height, radius = 'var(--radius-sm)' }: SkeletonBarProps) {
  return <div style={{ width, height, borderRadius: radius, background: 'var(--color-bg-disabled)', flexShrink: 0 }} />
}
