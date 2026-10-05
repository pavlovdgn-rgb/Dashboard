import { HEADER_HEIGHT } from './LeadCardPanel'

/** Ширина рельса Sidebar — см. components/Sidebar/Sidebar.module.css. Затемнение не должно накрывать
 *  рельс (см. ниже), поэтому дублируем значение здесь с явной ссылкой на источник, а не импортируем
 *  CSS-модуль ради одного числа. */
const SIDEBAR_WIDTH = 80

/**
 * Затемняющая подложка под правой выезжающей панелью (LeadCardPanel) — раньше была полностью прозрачной
 * (по дизайну slide-over панели не затемняли фон вообще, см. историю в `ds/CONTRACT.md`), 2026-08-29
 * пользователь это пересмотрел: «затени весь контент под правым окном кроме сайдбара и хедера». Затемняется
 * только зона контента (от правого края Sidebar и от нижнего края ModuleNav) — сам рельс и шапка остаются
 * на полной яркости, тот же паттерн, что `ContentScrim` в Figma-макетах (координаты/токены 1:1: `--color-
 * overlay-scrim` + `--opacity-scrim` — те же переменные, что уже использует scrim модалок NewLeadModal/
 * CallLogModalContent, см. `ds/foundation.md` → Paint Style «scrim»).
 *
 * Пока панель открыта, всё остальное (таблица/канбан-доска под ней, включая drag-and-drop карточек) должно
 * быть недоступно для клика/движения — взаимодействовать можно только с самой панелью, отсюда и имя
 * компонента (клик-блокер, не просто визуальный scrim). Модалки со своим скримом (NewLeadModal/
 * CallLogModalContent, z-index 100) уже блокируют клики сами по себе и в этом компоненте не нуждаются.
 * Плавающее окно чата (ChatWindow) этим блокером НЕ накрывается — оно не докнутая панель, не блокирует
 * остальной интерфейс под собой (см. ds/components.md → ChatWindow) и рендерится поверх затемнения, может
 * быть открыто одновременно с LeadCardPanel.
 */
export function InteractionBlocker() {
  return (
    <div
      style={{
        position: 'fixed',
        top: HEADER_HEIGHT,
        left: SIDEBAR_WIDTH,
        right: 0,
        bottom: 0,
        zIndex: 39,
        background: 'var(--color-overlay-scrim)',
        opacity: 'var(--opacity-scrim)',
        cursor: 'default',
      }}
    />
  )
}
