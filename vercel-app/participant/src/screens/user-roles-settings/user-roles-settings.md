# Screen: UserRolesSettings

**Источник:** `ds/screens/user-roles-settings.md`, Final Screen Node ID `154:4777`
**Роут:** `/settings/roles`

## Из базы
StatusBadge, Table

## Локальные композиции
`_shared/SettingsShell` (Sidebar + ModuleNav без бейджа/CTA + горизонтальный ряд `Tabs` — «Роли и права»/«Автоназначение»/«Телефония»/«Чат-виджет», «Роли и права» активен) — общая для всех 4 settings-экранов.

## Изменено 2026-08-27 (правка пользователя в макете)
Вертикальный список `SettingsSidebar` (240px) заменён на горизонтальный ряд из 4× компонента `Tabs`, под ModuleNav — тот же паттерн, что раньше был `ViewToggle` на LeadsTable/LeadsKanban (тот убран как дублирующий Sidebar-навигацию, см. `leads-table/leads-table.md`). См. `ds/screens/user-roles-settings.md` → «Ревизия 2026-08-27».

## Mock-контент
5 сотрудников verbatim из Figma. Роль → тон бейджа: Менеджер=neutral, Руководитель=success, Администратор=warning (решение из документации ДС).

## Не сделано
Действия со строками — статика.

## Найдено и исправлено в базе (2026-08-26)
`TableCell` не имел фона и заголовок был `12px/medium/text-secondary` вместо `14px/semibold/text-primary` — см. `ds/components.md` → Table Cell (общий фикс для всех таблиц, не специфично для этого экрана).

Также (2-й проход): не было SortIcon у Header-ячеек, не было скруглений углов и hover строки у `Table` — см. `ds/components.md` → Table Cell / Table.
