# Screen: Dashboard

**Источник:** `ds/screens/dashboard.md`, Final Screen Node ID `154:4362`
**Роут:** `/dashboard`

## Из базы
Sidebar, StatusBadge, Avatar, Input, Dropdown, TextButton, Button, MetricCard, FunnelBar, Table

## Локальные композиции
`_shared/AppShell`, `_shared/ModuleNav`, `leads-table/parts/LeadsFiltersBar`

## Mock-контент
4 KPI (время ответа/конверсия/просрочено/лидов за период), воронка 5 стадий (проценты посчитаны как value/max для FunnelBar.percent), таблица нагрузки команды — 3 менеджера. Значения verbatim из Figma.

## Не сделано
Обработчики фильтров/кнопки — статика.

## Найдено и исправлено в базе
`FunnelBar.module.css` → `.bar` был `span` без `display:block`, из-за чего ширина/высота в процентах браузером игнорировались и полоса рендерилась 0×0 (видно только на реальном скриншоте, не по коду). Добавлен `display:block` — однострочный фикс, не меняет API/остальной вид.

`TableCell.module.css` → `.cell` не имел фона вообще (ни у одной таблицы продукта не было белой заливки, только серый фон страницы просвечивал), а `.header` был на `12px/medium/text-secondary` вместо `14px/semibold/text-primary` (`Desktop/Main Semibold`, сверено с Figma напрямую) — оба фикса 2026-08-26, база компонента, влияет на все таблицы.

`TableCell` не рендерил SortIcon у Header (добавлен), `Table` не имел скруглений углов и hover строки (добавлены на `.headerRow`/`.row` в `Table.module.css`, точечно на крайних ячейках — `overflow:hidden` ломает `stickyHeader`, см. `ds/components.md` → Table). `FunnelBar.track` был 8px вместо 20px (сверено на мастере) — все фиксы 2026-08-26, влияют на все экраны с таблицами/воронкой.

`TextButton` был голой ссылкой без паддинга/фона/hover (`padding:0`, вес Regular) вместо полноценной 44px-кнопки (`padding: 12px 24px`, `radius/sm`, hover-заливка, вес Medium) — из-за этого расстояние до соседних Dropdown/Input визуально было меньше макета. См. `ds/components.md` → Text Button. Влияет на `LeadsFiltersBar` («Сбросить всё») и все остальные экраны с Text Button.

## Обновлено 2026-08-26 (правка пользователя в макете)
Зазор между «Воронка лидов по статусам» и первым `FunnelBar` увеличен до 24px (было 12) — см. `ds/screens/dashboard.md` → FunnelSection. Тот же зазор — между «Нагрузка команды» и таблицей (было 12, стало 24).

Таблица «Нагрузка команды» — не на всю ширину: колонки FIXED (440/320/300/296=1356px), обёрнута в `width:'fit-content'`, была ошибочно `width:'fill'` на первой колонке + растянута на 100% контейнера.
