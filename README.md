# UX-Lab · React base

Vite + React + TypeScript. Компонентная база из `ds/` и Figma: исходная Elastic UI Amsterdam и продуктовые компоненты UX-Lab.

## Запуск

```sh
npm install
npm run dev
```

Откройте адрес из терминала (обычно `http://localhost:5173/`). Каталог содержит компоненты с переключателями состояний, матрицы вариантов, палитру и шкалу текста. Текстовые и логические свойства находятся в раскрывающемся блоке «Текст и дополнительные свойства». Каждый элемент связан с исходным узлом Figma.

```sh
npm run check
npm run lint
npm run build
npm run preview
```

## Использование

```tsx
import { ProductButton, ScenarioTable, ParticipantsTable } from './components';

<ProductButton Kind="Primary" onClick={save}>Сохранить</ProductButton>
<ScenarioTable State="OverviewUnselected" onChange={selectScenario} />
<ParticipantsTable State="Ready" onOpenRecording={openRecording} />
```

Имена Figma, включая пробелы, пунктуацию и повторяющиеся имена, сохранены в реестре. Допустимые имена TypeScript и точное соответствие исходным ID перечислены в `ds/react-name-map.json`. Свойства вариантов сохраняют исходный регистр (`State`, `Selected`, `Kind`); текстовые свойства Figma с `#` передаются через spread.

Таблицы принимают собственные `rows`. Типы записей: `ScenarioRecord` в `_shared/ScenarioResults.tsx`, `ParticipantRecord` в `_shared/ParticipantsTableExample.tsx`. Без `rows` показаны демонстрационные данные. Навигационные действия передаются через callbacks; маршрутизация и загрузка данных относятся к сборке экранов.

Для подключения к другому корневому приложению сохраните порядок импортов токенов из `src/main.tsx`, загрузку шрифтов и провайдер `EuiProvider` с Amsterdam и `elasticTheme`. Продуктовые фасады самостоятельно подключают `ProductTheme`.

## Источники и синхронизация

- `ds/index.json`, `ds/components.md`, `ds/foundation.md`, `ds/CONTRACT.md` — исходный контракт.
- `src/tokens/manifest.json` — имена, ID, режимы и значения токенов.
- `src/tokens/primitives.css` → `semantics.css` → `typography.css` — токены и стили текста.
- `src/components/catalog.json` — 204 позиции Elastic и 23 позиции UX-Lab, 3 811 сочетаний вариантов.
- `src/components/_shared/` — адаптация исходной React-библиотеки и продуктовые композиции.
- `execution/generate_react_catalog.py` — воспроизводимая генерация фасадов из выгрузок Figma. Перед синхронизацией нужны актуальные выгрузки в `.tmp/react-base/`; не запускайте генератор на старом снимке после изменения макетов.

EUI закреплена на `106.7.0`, тема Amsterdam. 57 элементов исходного каталога помечены Deprecated; каталог сохраняет эти пометки и не заменяет библиотеку новой версией. Лицензия EUI — Elastic License 2.0 / SSPL, сведения поставляются с зависимостью.

## Проверки

При работающем `npm run dev` на порту 5173:

```sh
node execution/check_react_showcase.mjs
node execution/check_react_interactions.mjs
node execution/check_react_adapter_behaviors.mjs
node execution/check_react_completion.mjs
node execution/check_react_tokens.mjs
```

Проверки браузера используют установленный Google Chrome через Playwright. Подробные результаты находятся в `.tmp/react-base/`; постоянный итог — `ds/react-base-report.md`.

## Границы базы

Это страница компонентов, не приложение с подключённой аналитикой. По указанию пользователя подключены оригинальные иконки Elastic UI и логотип из макета UX-Lab. Данные и обработчики демонстрационные; реальные запись сессий, API и переходы между экранами не входят в React Base. Каталог Storybook описан ниже.

Исходная Elastic-тема имеет Light/Dark; продуктовые компоненты сохраняют утверждённую светлую тему. Каталог целиком загружает EUI и все фасады, поэтому production build предупреждает о большом JS-файле; разделение загрузки выполняется при сборке приложения.

Каталог запускается без React StrictMode: старый EuiObserver в закреплённой EUI 106 не восстанавливает наблюдение после пробного unmount/remount. Это влияет на измеряемые компоненты, в том числе высоту accordion. При подключении к приложению со StrictMode требуется отдельно решить совместимость EUI; проверка раскрытия включена в `check_react_completion.mjs`.

## Storybook

Рабочая песочница приложения: [UX-Lab — все проекты](http://localhost:5173/?screen=results-overview#/projects). Связанные разделы, локальное хранение демонстрационных данных и границы реализации описаны в [отчёте wire](ds/wire-report.md). Проверки полного прохода: `node execution/check_workspace.mjs` и `node execution/check_workspace_edges.mjs` при запущенных Vite и Storybook.

```sh
npm run storybook -- --ci --no-open
```

Адрес: http://localhost:6006/. Foundation содержит Primitive/Semantic токены, 29 текстовых стилей и исходные иконки. В Components — 227 компонентов с autodocs, контролами, копированием кода и 3 811 вариантами. Sandboxes объединяет компоненты в форму, модальное окно, навигацию и таблицу с уведомлением.

```sh
python execution/generate_storybook_catalog.py
node execution/check_storybook.mjs --all
npm run build-storybook
```

Генератор обновляет истории из `src/components/catalog.json`; повторный `storybook init` не нужен. Проверка требует запущенный сервер на порту 6006 и установленный Chrome. Статическая сборка появляется в `storybook-static/`. Происхождение иконок: `ds/icon-origin.md`; результат работ: `ds/storybook-report.md`.

