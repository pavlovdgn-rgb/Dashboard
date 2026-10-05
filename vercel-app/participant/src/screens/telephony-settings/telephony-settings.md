# Screen: TelephonySettings

**Источник:** `ds/screens/telephony-settings.md`, Final Screen Node ID `154:4954`
**Роут:** `/settings/telephony`

## Из базы
Card, Button, StatusBadge, TextButton, Checkbox, Toast

## Локальные композиции
`_shared/SettingsShell` («Телефония» активен). ProviderCard/ConnectionForm собраны на реальном `Card` — в отличие от Figma (где Card-инстанс не принимал произвольных детей), в React-коде это ограничение не действует, см. комментарий в `Card.tsx`.

## Mock-контент
Mango Office подключён (Secondary/Disabled «Подключено»), Sipuni/Novofon — Primary «Подключить»; форма подключения Mango Office со статусом «Активно»; 2 чекбокса функций; Toast «Провайдер подключён» — verbatim из Figma.

## Не сделано
Подключение/отключение провайдера, чекбоксы — без обработчиков.
