# Screen: CallLogModal

**Источник:** `ds/screens/call-log-modal.md`, Final Screen Node ID `154:4918`
**Роут:** `/call-log-modal`

## Из базы
IconButton, Radio, Dropdown, Input (textarea), TextButton, Button

## Локальные композиции
Центрированная модалка + затемнение через токены `--color-overlay-scrim`/`--opacity-scrim` (единственный экран проекта с настоящим scrim — блокирующая модалка, в отличие от slide-over панелей LeadCard/ChatPanel).

## Mock-контент
Направление «Исходящий», результат «Перезвонить позже», комментарий verbatim из Figma.

## Не сделано
Закрытие, выбор радио/дропдауна, сохранение — без обработчиков. Вариант с ошибкой валидации (`CallLogModal — Error`) не собран отдельно — не запрошен явно.
