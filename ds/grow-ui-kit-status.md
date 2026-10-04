# UI Kit extension — выполнено

Elastic UI (Copy) подключена к Dashboard. Импорт основных компонентов, существующих Text Styles и Variables подтверждён. Служебная .Button Group / Button не опубликована; вместо неё использован основной Button той же версии.

[Открыть UI Kit — extended](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=82-45) · [Foundation](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=82-15).

- **HeatmapLegend** — 2 варианта, аудит ✓, [Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=83-730).
- **ReplayControls** — 4 варианта, аудит ✓, [Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=84-713).
- **DataCoverage** — 3 варианта, аудит ✓, [Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=86-370).

Проверены тип ComponentSet, девять вариантов, Text Styles и их типографические Variables, привязки цветов, положительных отступов и четырёх радиусов. Макеты просмотрены визуально. Воспроизводимые скрипты: execution/grow_ui_kit.py и execution/finalize_grow_ui_kit.py. Новые Text Styles не создавались.

Это компоненты для макетов, не работающий сборщик событий или проигрыватель. D02 (единица первого клика) остаётся открытым. Полная интерактивная матрица и сборка финальных экранов — отдельные задачи.

Обновление ReplayControls от 22 сентября: [шкала по референсу, управление и границы изменений](replay-reference-update.md).


## Component variants — завершено

Добавлены ProductButton (18), ProductNavItem (8), ProductTab (8). Вместе с HeatmapLegend (2), ReplayControls (4), DataCoverage (3): **6 наборов, 43 варианта**. Все привязки и снимки проверены. [Матрицы в Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=125-308). [Разбор каталога](component-variants-audit.md).

Скрипты: build_interaction_variants.py, audit_interaction_variants.py, finalize_component_variants.py. Ранние генераторы описывают прежний пакет; перед повторной записью читать текущий канвас.
