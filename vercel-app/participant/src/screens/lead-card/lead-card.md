# Screen: LeadCard

**Источник:** `ds/screens/lead-card.md`, Final Screen Node ID `154:4747`
**Роут:** `/lead-card`

## Из базы
IconButton, StatusBadge, TextButton, Dropdown, Button, TimelineItem

## Локальные композиции
Бэкдроп — реальный экран `leads-kanban/LeadsKanban` (переиспользован как компонент, как в Figma — «LeadsKanban Backdrop (clone)», без затемнения, см. `ds/CONTRACT.md` про slide-over без scrim). Панель — `position:fixed` 480px справа поверх бэкдропа.

## Mock-контент
Лид Екатерина Иванова verbatim из Figma: контакты, скор 45, статус «Перезвонить · Просрочен на 1 день», 3 записи истории.

## Не сделано
Закрытие панели, quick-status кнопки, звонок/чат — без обработчиков (статика).
