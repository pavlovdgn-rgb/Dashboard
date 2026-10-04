# Lead Generation — React-база

React + TypeScript + Vite приложение для продукта лидогенерации (культурные учреждения: музеи, зоопарки, выставки, театры — билетинг и контроль доступа).

## Структура

```
src/
├── components/   # UI-компоненты дизайн-системы (Button, Table, Sidebar, Toast и др.)
├── foundation/   # Базовые токены и примитивы
├── tokens/       # Дизайн-токены (цвета, отступы, типографика)
├── lib/          # Утилиты
└── sandboxes/    # Песочницы для разработки/проверки компонентов
```

Каталог компонентов задокументирован и просматривается через **Storybook**.

## Как запустить

```bash
npm install
npm run dev          # dev-сервер приложения
npm run storybook    # каталог компонентов (Storybook), порт 6006
```

Другие команды:

```bash
npm run build             # production-сборка
npm run build-storybook   # статическая сборка каталога компонентов
npm run lint               # проверка кода (oxlint)
```
