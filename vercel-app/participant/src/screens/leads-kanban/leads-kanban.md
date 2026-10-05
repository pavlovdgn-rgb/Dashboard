# Screen: LeadsKanban

**Источник:** `ds/screens/leads-kanban.md`, Final Screen Node ID `154:6604`
**Роут:** `/leads-kanban`

## Из базы
Sidebar, StatusBadge, Avatar, Tabs, Input, Dropdown, TextButton, Button, KanbanCard

## Локальные композиции
`_shared/AppShell`, `_shared/ModuleNav`, `leads-table/parts/LeadsFiltersBar` (переиспользована один в один — тот же состав фильтров)

## Убрано 2026-08-27 (правка пользователя в макете)
`_shared/ViewToggle` — дублировал навигацию Лиды/Канбан в Sidebar-флайауте, см. `ds/screens/leads-kanban.md` → «Ревизия 2026-08-27».

## Mock-контент
5 колонок статуса (Новый/В работе/Перезвонить/Квалифицирован/Не подходит), 5 карточек + 1 пустая колонка — verbatim из Figma.

## Не сделано
Drag-and-drop, обработчики карточек/фильтров — статика (граница директивы).
