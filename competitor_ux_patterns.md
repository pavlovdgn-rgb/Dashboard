# UX-паттерны конкурентов

Дата: 18 сентября 2026 года. Контекст: внутренний сервис для дизайнеров и PM; два коллеги, 2–5 одновременных участников, 20 участников исследования. Главный приоритет — тепловые карты; весь объём первой версии сохраняется.

Основания: [бриф](brief.md), [быстрый анализ](competitive_analysis.md), [полученный глубокий отчёт](deep_research_results.md.md) и точечная проверка первоисточников. UX оценён по документации, без самостоятельного тестирования кабинетов. Возможности конкурентов учитываются независимо от тарифа; ограничения указаны отдельно. Наш продукт находится на стадии плана.

## 1. Рыночный стандарт: общие ожидания

На уровне задач у рассмотренных продуктов повторяются подключение источника данных, выбор контекста анализа и переход к деталям поведения. Это сходство процессов, а не доказательство одинаковых экранов или наличия исследования с заданиями у всех пяти. Источники описывают возможности, но не заменяют наблюдение за пользователями.

| Повторяющийся паттерн | Где подтверждён | Ожидание для нашего интерфейса |
| --- | --- | --- |
| Подключить код и убедиться в поступлении данных | Maze, Clarity; сбор через код также у остальных [M1](https://help.maze.co/articles/2471284614-website-test-run-usability-tests-on-your-live-websites) [C4](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup) [U2](https://www.uxtweak.com/session-recording-tool/) [P2](https://posthog.com/docs/session-replay) [S4](https://docs.contentsquare.com/en/web/personal-data-handling/) | Статусы «подключено», «нет данных», «ошибка» перед запуском |
| Перейти от общей картины к конкретной сессии | Maze, Clarity, Contentsquare, PostHog [M2](https://help.maze.co/articles/4467546573-understanding-your-live-website-test-results) [C2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/funnels) [S2](https://support.contentsquare.com/hc/en-us/articles/37271710955793-How-to-create-Heatmaps-and-Zonings) [P4](https://posthog.com/docs/product-analytics/funnels) | Из карты или воронки доступны относящиеся к ней участники |
| Ограничить данные контекстом | Фильтры сессий UXtweak, устройства Clarity, сегменты Contentsquare [U2](https://www.uxtweak.com/session-recording-tool/) [C1](https://learn.microsoft.com/en-us/clarity/heatmaps/heatmaps-overview) [S2](https://support.contentsquare.com/hc/en-us/articles/37271710955793-How-to-create-Heatmaps-and-Zonings) | Видно, по какому заданию, устройству и участникам построена карта |
| Проигрыватель с навигацией по поведению | UXtweak, Contentsquare, PostHog [U2](https://www.uxtweak.com/session-recording-tool/) [S3](https://support.contentsquare.com/hc/en-us/articles/37271802041745-Insights-and-Session-Replay) [P2](https://posthog.com/docs/session-replay) | Переход к значимому моменту без просмотра всей сессии |

Конструктор заданий, PDF и одинаковая обработка полей ввода **не являются подтверждённым общим стандартом всех пяти продуктов**.

## 2. Точки расхождения

| Одна задача | Разные подходы | Следствие для нашего проекта |
| --- | --- | --- |
| Определить успех | Maze — пути сайта; PostHog/Clarity — события воронки [M1](https://help.maze.co/articles/2471284614-website-test-run-usability-tests-on-your-live-websites) [P4](https://posthog.com/docs/product-analytics/funnels) [C2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/funnels) | Разделить понятный текст задания и проверяемый критерий; автоматический перевод текста в событие не обещать |
| Получить запись | Maze Clips — экран; UXtweak — также DOM-реконструкция [M1](https://help.maze.co/articles/2471284614-website-test-run-usability-tests-on-your-live-websites) [U2](https://www.uxtweak.com/session-recording-tool/) | Проверять требуемый результат воспроизведения, не выбирать формат только по названию «запись» |
| Открыть карту | Maze — из экрана/пути; Contentsquare — анализ страницы/зоны; PostHog — Toolbar или in-app [M2](https://help.maze.co/articles/4467546573-understanding-your-live-website-test-results) [S2](https://support.contentsquare.com/hc/en-us/articles/37271710955793-How-to-create-Heatmaps-and-Zonings) [P1](https://posthog.com/docs/toolbar/heatmaps) | Сделать карту основной областью результатов исследования |
| Сопоставить состояния | У Maze есть ограничение первого снимка; PostHog предлагает карту поверх снимка replay [M2](https://help.maze.co/articles/4467546573-understanding-your-live-website-test-results) [P1](https://posthog.com/docs/toolbar/heatmaps) | Проверить модалки и разные состояния одного URL до фиксации решения |
| Показать ввод | Clarity скрывает input; PostHog настраивает маскирование; Contentsquare имеет специальный режим [C3](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-masking) [P3](https://posthog.com/docs/session-replay/privacy) [S4](https://docs.contentsquare.com/en/web/personal-data-handling/) | Требование брифа сохраняется, но не заявляется уникальным |
| Завершить анализ отчётом | PDF у UXtweak; в рассмотренной документации Maze — CSV и изображения [U3](https://www.uxtweak.com/pricing/) [M2](https://help.maze.co/articles/4467546573-understanding-your-live-website-test-results) | Согласовать структуру PDF как отдельный результат исследования |

## 3. Рекомендации для проектирования

Ниже — предложения для реализации согласованного объёма, а не новые подтверждённые требования.

| Что перенять | У кого и почему | Как применить и проверить |
| --- | --- | --- |
| Проверка установки | Maze / Clarity: понятная готовность источника [M1](https://help.maze.co/articles/2471284614-website-test-run-usability-tests-on-your-live-websites) [C4](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup) | Пробная сессия перед отправкой ссылки; коллега понимает причину отсутствия данных |
| Результаты вокруг задания | Maze: связь исхода и поведения [M2](https://help.maze.co/articles/4467546573-understanding-your-live-website-test-results) | Исследование → задание → карта/воронка → участник; проверить поиск проваленного задания |
| От шага к сессии | Clarity / PostHog: метрика связана с деталями [C2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/funnels) [P4](https://posthog.com/docs/product-analytics/funnels) | Нажатие на отказ открывает нужных участников и момент записи |
| Сохранение фильтров | Contentsquare: переход в replay с тем же контекстом [S2](https://support.contentsquare.com/hc/en-us/articles/37271710955793-How-to-create-Heatmaps-and-Zonings) | При переходе с карты и обратно сохраняются задание, устройство и выборка |
| Поиск и пропуск неактивности | UXtweak: меньше ручного просмотра [U2](https://www.uxtweak.com/session-recording-tool/) | Быстро найти повторный клик; паузу можно пропустить, её длительность остаётся видимой |
| Контекст перед проблемой | Contentsquare Insights [S3](https://support.contentsquare.com/hc/en-us/articles/37271802041745-Insights-and-Session-Replay) | Открывать запись немного раньше события, чтобы видеть предшествующее действие |

**Предложение по компоновке:** страница исследования с разделами «Настройка», «Участники», «Результаты», «Отчёт». В «Результатах» карта занимает основное место, рядом доступны воронка и список участников; выбор задания и устройства общий. Это наш вариант для проверки, а не скопированный рыночный стандарт.

**Прозрачность метрик:** показывать одновременно число и долю, например «8 из 20 — 40%», а также знаменатель и пропущенные данные. Не скрывать карты только из-за n=20 и не обещать статистическую значимость по одному размеру выборки; метод зависит от вопроса, набора участников и требуемой точности. [N1](https://www.nngroup.com/articles/quantitative-studies-how-many-users/)

**Первый клик:** перед проектированием определить начало отсчёта — страница, задание или сессия. **События успеха:** проверить кнопку без смены URL, несколько допустимых путей и повторную попытку. **Полнота сбора:** показывать статус данных каждого участника, не обещая технически недостижимые гарантии записи при разрыве соединения.
