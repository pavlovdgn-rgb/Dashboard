# Screen: LeadsTable

**Источник:** `ds/screens/leads-table.md`, Final Screen Node ID `154:4466` (Lead-generation_2.0, «Flow», Screens/2)
**Роут:** `/leads-table`

## Из базы
Sidebar, StatusBadge, Avatar, Tabs, Input, Dropdown, TextButton, Button, Checkbox, Table (+TableCell внутри)

## Локальные композиции
- `_shared/AppShell` — Sidebar + контентная колонка (переиспользуется другими экранами)
- `_shared/ModuleNav` — заголовок + бейдж + пользователь, 84px (переиспользуется)
- `parts/LeadsFiltersBar` — поиск + 3 дропдауна + «Сбросить всё» + CTA «Новый лид» (переиспользуется empty/loading-вариантами)

## Убрано 2026-08-27 (правка пользователя в макете)
`_shared/ViewToggle` (переключатель Список/Канбан) удалён — дублировал уже существующую навигацию Лиды/Канбан в Sidebar-флайауте. Компонент полностью выпилен из кода (был только здесь, в `leads-kanban` и трёх empty/loading-вариантах). См. `ds/screens/leads-table.md` → «Ревизия 2026-08-27».

## Mock-контент
5 строк лидов, значения — verbatim из Figma (см. `ds/screens/leads-table.md`).

## Не сделано (по границе директивы)
Сортировка колонок, чекбоксы, дропдауны, поиск, кнопка «Новый лид» — без обработчиков, статика.

## Найдено и исправлено в базе (2026-08-26)
`TableCell` не имел фона (белая заливка отсутствовала на всех таблицах) и заголовок был `12px/medium/text-secondary` вместо `14px/semibold/text-primary` (`Desktop/Main Semibold`) — см. `ds/components.md` → Table Cell.

Также (2-й проход): не было SortIcon у Header-ячеек, не было скруглений углов и hover строки у `Table` — см. `ds/components.md` → Table Cell / Table.

`TextButton` («Сбросить всё» в `LeadsFiltersBar`) был без паддинга (голая ссылка) вместо 44px-кнопки с `padding: 12px 24px` — визуально расстояние до соседнего Dropdown было меньше макета. См. `ds/components.md` → Text Button.
