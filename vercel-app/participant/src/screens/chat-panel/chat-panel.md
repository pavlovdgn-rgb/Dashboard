# Screen: ChatPanel

**Источник:** `ds/screens/chat-panel.md` (не `chat-panel-v2.md` — та версия архивирована 2026-08-25, отклонена пользователем), Final Screen Node ID `154:4893`
**Роут:** `/chat-panel`

## Из базы
IconButton, MessageBubble, Input, Button, StatusBadge, TextButton, Dropdown, TimelineItem

## Локальные композиции
Бэкдроп — `leads-kanban/LeadsKanban` (полная яркость, без затемнения — правило проекта для slide-over). Две панели рядом справа: ChatPanelPanel (585px) + SlideOverPanel лида (480px), обе `position:fixed`.

## Mock-контент
Лид Дмитриев Олег verbatim из Figma: 3 сообщения чата, скор 91/статус «Новый», 1 запись истории (Type=Chat).

## Не сделано
Закрытие панелей, отправка сообщения, quick-status — без обработчиков.
