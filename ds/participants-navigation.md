# Участники и боковая навигация

Компоненты созданы и проверены в Dashboard. Это макеты Figma; клики, фильтры, сортировка и загрузка данных не являются реализованным приложением. Исходная Elastic UI не изменялась.

| Компонент | Вариантов | Состояния |
| --- | ---: | --- |
| [TaskOutcome](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=152-948) | 3 | Status=Achieved; Status=NotAchieved; Status=NotAssessed |
| [RecordingCoverage](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=152-964) | 3 | Status=Complete; Status=Partial; Status=Unavailable |
| [AttemptAction](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=152-996) | 3 | Mode=Single; Mode=Multiple; Mode=Unavailable |
| [ParticipantRow](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=153-692) | 3 | State=Default; State=Hover; State=Focus |
| [ParticipantsTable](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=153-1605) | 5 | State=Ready; State=Loading; State=Empty; State=FilteredEmpty; State=Error |
| [NavMenu](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=153-2777) | 10 | Active=Projects; Active=Studies; Active=Setup; Active=Launch; Active=Overview; Active=Heatmap; Active=Funnel; Active=Participants; Active=Signals; Active=PDF |

## Таблица участников

Строки чередуют белый background/surface (#FFFFFF) и светло-серый background/canvas (#F7F7F2): серые 2-я, 4-я и далее чётные видимые строки. Фон назначается на уровне композиции таблицы, не меняет смысл статусов. После сортировки и фильтрации чередование считается заново по видимому порядку. Скрипт: execution/apply_participant_zebra_rows.py.

[Готовый пример](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=153-702). Поиск по ID, фильтры исхода и полноты данных, четыре демонстрационные строки, пагинация. Одна строка описывает выбранную попытку участника. При выборе другой попытки приложение должно одновременно менять исход, время, сигналы, полноту и целевую запись. Эти взаимодействия описаны, но не подключены к данным.

Исход задания и полнота данных — независимые вложенные компоненты. Полные данные не гарантируют достижения цели, неполные не означают неуспех. У недоступной записи показано пояснение вместо кнопки открытия. Фильтр по меткам, настройка колонок и отдельная выгрузка не добавлены. Сортировку необходимо подключить на экране; ложного признака уже отсортированных данных в примере нет.

«Выбрать попытку» использует ProductButton/Secondary, иконку layers слева и arrowDown справа; обе иконки — instances Elastic UI. Меню списка попыток и прототип взаимодействия не входят в текущую отрисовку.

## NavMenu

[Пример с активными участниками](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=153-2369). Размер 320×1080. Active переключает 10 разделов. Projects показывает рабочее пространство; Studies добавляет проект; разделы исследования показывают всю структуру. Заголовки проекта и исследования редактируются через свойства. Пункты собраны из ProductNavItem и библиотечных иконок. Наведение и фокус доступны в свойствах вложенного ProductNavItem. Нижний блок прижат вниз через растягиваемый Auto Layout; готовность исследования — демонстрационный статус, не реальное состояние сервера. Номер версии приложения не выдуман и не добавлен.

## Последние визуальные решения

- ScenarioRow: серые фоны счётчиков сохранены при Selected=False; при Selected=True число графитовое без фона.
- ProductButton/Secondary: фон background/sidebar, Hover — border/subtle, Pressed — accent/soft. Белый фон и контур убраны; рамка Focus сохранена. Tertiary в спокойном состоянии прозрачен.
- Ширина внутреннего контрола ProductButton растягивается вместе с instance, иконки не обрезаются.
- Новых цветов нет: используются утверждённые Variables. Источники, размеры, шрифты и палитра сохранены.

## Проверка и воспроизведение

Геометрия видимых дочерних элементов, привязки цветов и текстовые стили проверены у всех 27 новых вариантов. Ошибок нет. Визуально проверены все пять состояний таблицы, меню участников и кнопка выбора попытки. Состояния макета не являются интерактивным прототипом.

Исполнение: build_participants_navigation.py (стадии outcome, coverage, action, row, table, nav; после каждой — combine), затем polish_participants_navigation.py и add_attempt_button_icons.py. Последние два скрипта используют ID из текущего файла; перед применением к заново созданной библиотеке ID нужно обновить по квитанциям. Для визуальных правок сценариев — refine_secondary_buttons.py. Проверка — audit_participants_navigation.py.

Учтённое ограничение MCP: импортированный, но не вставленный source-компонент может не находиться по временному ID в следующем вызове. Search field импортируется по стабильному key в том же вызове, где создаётся instance.

## Уточнение отступов, шевронов и подложек

NavMenu: внутренние боковые отступы всех строк — 12 px (Dimensions/md), расстояние до иконки — 8 px. Вложенный контрол занимает оставшуюся ширину; минимальная ширина снята через null. Текст #626E32 на фоне #ECEEDC: 4,6973:1, соответствует минимуму 4,5:1 для обычного текста. Проверены все 10 вариантов, переполнений нет.

Во всех 10 кнопках фильтров ParticipantsTable текстовый треугольник заменён на instance arrowDown. В UI Kit не осталось текстовых треугольников раскрытия. «Выбрать попытку» содержит layers + arrowDown.

[Три предложения подложек Secondary](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=164-1681): A — плотный серый; B — серый с контуром (рекомендация); C — оливковый с контуром. Сравнение на белой, светлой и активной оливковой поверхности. Варианты представлены как локальные overrides связанных instances; ни один не применён к мастерам.

Воспроизводимые правки: fix_nav_menu_padding.py, replace_dropdown_text_arrows.py, propose_secondary_surfaces.py. Учтённое ограничение API: minWidth=0 недопустим, для снятия минимума используется null.
