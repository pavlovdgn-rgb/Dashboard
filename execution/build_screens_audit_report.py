"""Build the read-only screens audit from saved Figma evidence; no network or DS writes."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / '.tmp/screens-audit-2026-09-23'

def read(name):
    return json.loads((E / name).read_text(encoding='utf-8'))

def slug(name):
    return 'screens/' + re.sub(r'(?<!^)(?=[A-Z])', '-', name.removeprefix('Screen/')).lower()

def link(node, label=None):
    return f'[{label or node}](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id={node.replace(":", "-")})'

screens = []
for path in sorted(E.glob('scan-*.json'), key=lambda p: int(p.stem.split('-')[-1])):
    screens.extend(json.loads(path.read_text(encoding='utf-8'))['screens'])
assert len(screens) == len({s['id'] for s in screens}) == 55
foundation = read('foundation.json')['sets']
inputs = read('inputs.json')
catalog = {c['id']: c for c in inputs['catalog']['components']}
usage = []
for component in foundation:
    instances = [s for s in screens if s['usage'].get(component['id'], {}).get('count')]
    variants = {v for s in instances for v in s['usage'][component['id']]['variants']}
    actual = {slug(s['name']) for s in instances}
    expected = set(catalog.get(component['id'], {}).get('usedIn', []))
    usage.append(dict(id=component['id'], name=component['name'],
        visibleInstances=sum(s['usage'][component['id']]['visible'] for s in instances),
        allInstances=sum(s['usage'][component['id']]['count'] for s in instances),
        defined=len(component['variants']), used=len(variants),
        usedVariants=[v for v in component['variants'] if v['id'] in variants],
        unusedVariants=[v for v in component['variants'] if v['id'] not in variants],
        screens=[{'id': s['id'], 'name': s['name']} for s in instances],
        missingUsedIn=sorted(actual-expected), staleUsedIn=sorted(expected-actual)))

# State families are reviewed together: an error screen does not itself need another error state.
families = [
 ('Projects', ['ProjectsDefault', 'Projects', 'ProjectsEmpty'], 'Список проектов; форма создания',
  'Данные и пустой список; открытая форма с заполнением. ProductField Invalid/Focus/Disabled и ProductButton Loading существуют в ДС.',
  'Для списка: загрузка, ошибка, пустой результат поиска, переполнение. Для формы: сообщение ошибки обязательного поля, отправка всей формы, подтверждение создания, ошибка сохранения с сохранённым вводом.', 'P1'),
 ('Studies', ['Studies', 'StudiesEmpty'], 'Список исследований; карточки показателей; поиск',
  'Список с данными и пустой проект. SummaryMetric Loading/Empty доступны в ДС.',
  'Загрузка/ошибка всего списка, пустой результат фильтра, длинное название/переполнение; ошибка расчёта показателей.', 'P1'),
 ('Setup', ['StudySetup', 'StudySetupBlank', 'StudySetupFree', 'TaskEditor', 'TaskPicker', 'SuccessCriteria', 'CriteriaURL', 'CriteriaButton'], 'Формы исследования, задания и критериев',
  'Пустая/заполненная настройка, два режима, формы критериев, выбранная/невыбранная карточка задания. Invalid у полей и Loading у кнопок доступны в ДС.',
  'Согласованные формы с ошибками и текстом исправления, отправка, успех сохранения, ошибка сохранения без потери ввода; длинные задания и ограничение длины. Наличие варианта поля не задаёт поведение всей формы.', 'P1'),
 ('ConnectionLaunch', ['ConnectionError', 'ControlResult', 'Launch', 'LaunchActive', 'LaunchError'], 'Подключение, контрольная проверка, запуск',
  'Ошибка подключения/неполученные события, успешная контрольная попытка, готовность, активный сбор, ошибка запуска. Loading кнопки доступен в ДС.',
  'Ход повторной проверки и запуска как состояния рабочего блока; устаревшая успешная проверка после изменения URL/критерия. Не объединять ошибку запуска с ошибкой сохранения настроек.', 'P1'),
 ('Results', ['ResultsOverview', 'ResultsEmpty'], 'Сценарии, сводные показатели, обновление',
  'Ready, Selected, Loading, Error, Empty, FilteredEmpty, Overflow, FreeExploration в скрытых соседях ResultsOverview; отдельный ResultsEmpty. Таблица и карточки имеют варианты в ДС.',
  'Явное состояние устаревших результатов и поведение при поступлении новых данных во время просмотра. Свежие данные обозначены временем обновления. Для скрытых состояний нужна отдельная приёмка при показе; наличия слоя достаточно для учёта покрытия.', 'P2'),
 ('ResultsFree', ['ResultsFree'], 'Сводка свободного исследования, список страниц',
  'Сводка и страницы с данными; Loading/Empty карточек доступны в ДС. Общая ветка FreeExploration есть в ResultsOverview.',
  'Не задано применение общей Loading/Error/Empty ветки к этому отдельному экрану; у ExploredPages нет загрузки, ошибки, пустого/длинного списка. Зафиксировать переиспользование либо добавить состояния.', 'P1'),
 ('Funnel', ['Funnel'], 'Воронка/таблица шагов, показатели',
  'Данные по шагам и сводка; варианты Loading/Empty у SummaryMetric в ДС.',
  'Пустая воронка, загрузка, ошибка, длинные названия/много шагов; случай нулевой базы без вводящего в заблуждение процента.', 'P1'),
 ('Participants', ['Participants', 'ParticipantsFromHeatmap'], 'Таблица участников, поиск и фильтры',
  'Ready на двух экранах; Loading, Empty, FilteredEmpty, Error доступны в ParticipantsTable. Это покрытие в ДС, а не четыре отсутствующих состояния.',
  'Переполнение/длинные значения; поведение списка после обновления выборки на последней странице. Связать готовые варианты с экранными сценариями в спецификации.', 'P2'),
 ('ParticipantDetails', ['ParticipantDetails'], 'Карточка участника, таблица попыток',
  'Контекст выбранной попытки и данные; Loading/Empty показателей доступны в ДС.',
  'Загрузка/ошибка/отсутствие попыток и длинная таблица; удалённый или недоступный участник при переходе по сохранённой ссылке.', 'P1'),
 ('Heatmaps', ['Heatmaps', 'HeatmapsFirstClick', 'HeatmapsDynamicState'], 'Снимок, слой кликов, выборка/цели',
  'Все клики, первый клик, динамическое состояние; два режима HeatmapLegend. FirstClickTargets имеет Ready/Loading/Empty/FilteredEmpty/Error в ДС, но экземпляров в Screens нет.',
  'Для холста: загрузка/ошибка снимка, отсутствующий снимок, ноль кликов и пустая выборка, несовместимая версия/размер. Готовые состояния списка целей не покрывают холст; для них нужна явная связь с текущей композицией.', 'P1'),
 ('Replay', ['Replay', 'ReplayIncomplete', 'ReplayUnavailable'], 'Запись и управление воспроизведением',
  'Полная, неполная и недоступная запись; Paused/Playing × Complete/Gap в ReplayControls.',
  'Загрузка записи/буферизация/повторная загрузка в процессе; сохранённое положение при ошибке. Удаление записи можно покрыть ReplayUnavailable после уточнения текста причины, новый отдельный экран не обязателен.', 'P1'),
 ('Signals', ['Signals', 'SignalsByPage', 'SignalsPageDetails'], 'Списки событий и страниц, детали',
  'Данные, группировка, детализация страницы.',
  'Пусто, загрузка, ошибка, пустой результат фильтра, переполнение; недоступный источник в деталях. Кроме покрытия, у Signals неправильный компонент вкладок — отдельная находка S1.', 'P1'),
 ('Findings', ['Findings', 'FindingsEmpty', 'FindingDetails', 'FindingEditor', 'FindingSaved'], 'Список, карточка, форма находки',
  'Данные, пустой список, открытая карточка/редактор, подтверждение сохранения; варианты Invalid и Loading контролов в ДС.',
  'Загрузка/ошибка списка, переполнение, удалённая находка или источник; валидация обязательного наблюдения, процесс/ошибка сохранения; конфликт изменения двумя коллегами — зависит от D08. У FindingsEmpty также S1.', 'P1'),
 ('Report', ['Report', 'ReportGenerating', 'ReportReady', 'ReportError'], 'Выбор состава и формирование PDF',
  'Настройка, процесс, успех и ошибка формирования; Off/On/Mixed и Disabled чекбоксов существуют в ДС, на экране показан On.',
  'Не определён результат снятия всех разделов: Disabled у формирования и пояснение либо разрешённый пустой отчёт по продуктовому решению. Недоступность одной из выбранных карт/записей при генерации.', 'P1'),
 ('ParticipantFlow', ['ParticipantIntro', 'TaskBriefing', 'ParticipantSession', 'ParticipantFinish', 'ParticipantIntroMobile', 'TaskBriefingMobile', 'ParticipantSessionMobile', 'ParticipantFinishMobile'], 'Доступ участника, инструкции, отправка результатов',
  'Основной путь desktop/mobile; успешное завершение. Ошибки ссылки/прототипа/передачи представлены отдельной семьёй ParticipantErrors.',
  'Процесс отправки результата/загрузка прототипа; адаптация существующих ошибочных состояний на mobile явно не описана. Валидация формы магазина относится к чужому тестируемому интерфейсу, не к продуктовой ДС.', 'P2'),
 ('ParticipantErrors', ['UnavailableLink', 'PrototypeUnavailable', 'ParticipantTransferError'], 'Ошибки доступа участника и передачи',
  'Недоступная ссылка, недоступный прототип, ошибка передачи результата с повтором.',
  'Состояние повтора в процессе доступно только как вариант кнопки в ДС; связь с оболочкой участника и mobile должна быть описана. Отдельные платежи/регистрация не применимы.', 'P2'),
 ('Access', ['Login'], 'Доступ коллеги',
  'Начало входа; текст обращения к коллеге при отсутствии доступа.',
  'Способ входа, запрещённый/заблокированный доступ и истечение сессии не подтверждены: IA04/D08 оставлены открытыми. Не считать отсутствие PasswordReset/Signup/оплаты дефектом до решения.', 'Decision'),
]
family_for = {name: f for f in families for name in f[1]}
assert set(family_for) == {s['name'].removeprefix('Screen/') for s in screens}

stats = dict(screens=len(screens), nodes=sum(s['nodeCount'] for s in screens),
    localSets=len(foundation), variants=sum(u['defined'] for u in usage),
    usedVariants=sum(u['used'] for u in usage),
    unusedSets=[u['name'] for u in usage if not u['allInstances']],
    rawPaints=sum(len(s['colors']) for s in screens),
    visibleRawPaints=sum(c['visible'] for s in screens for c in s['colors']),
    rawEffects=sum(e['count'] for s in screens for e in s['effects']),
    visibleRawEffects=sum(e['visible'] for s in screens for e in s['effects']))
machine = dict(date='2026-09-23', mode='Audit only', stats=stats, usage=usage,
    families=[dict(key=f[0], screens=f[1], blocks=f[2], present=f[3], missing=f[4], priority=f[5]) for f in families],
    screenInventory=[dict(id=s['id'], name=s['name'], nodeCount=s['nodeCount'], family=family_for[s['name'].removeprefix('Screen/')][0], blocks=s['blocks']) for s in screens])
(E/'report-data.json').write_text(json.dumps(machine, ensure_ascii=False, indent=2), encoding='utf-8')

out = []
def emit(s=''):
    out.append(s)

emit('# Аудит экранов · 23 сентября 2026')
emit('\nРежим: **Audit only** по `directives/directive_screens_audit.md`. В Figma и каталоге изменений не сделано. Проверено 55 экранов / 17 524 вложенных узла; учтены скрытые состояния. Сопоставлено 22 локальных набора / 168 вариантов, 81 локальная Variable и Effect Styles. Прочитан 71 локальный файл: каталог, foundation, scan-status и все файлы ds/screens. Исходные 204 позиции Elastic — справочный каталог ds_scan, а не 204 локальных набора Dashboard.')
emit('\nОсновной подтверждённый визуальный пропуск: **две группы вкладок всё ещё собраны из одинаковых Secondary-кнопок**. Ещё обнаружены 3 расхождения реестра использования и пробелы в сценариях загрузки/ошибок/сохранения. Неиспользуемые варианты, скрытые технические слои и предположения о дублях не суммируются с этими дефектами.')
emit('\n## Границы и принятые решения')
emit('- Обход ограничен '+link('175:613','Screens на Final Screens')+'; исторические вайрфреймы и доски сравнения не считаются текущими экранами. '+link('82:15','Foundation')+' и локальные наборы на странице UI Kit прочитаны отдельно.\n- Утверждённые Secondary A без контура, действия на цветных DataCoverage, оливковый playback и прозрачные вкладки сохраняются. Общее решение по Tertiary не переоткрывалось.\n- Девять областей NOVA — намеренно чужая дизайн-система; Manrope, фиолетовые цвета, фото и собственные компоненты не являются detached-дубликатами продукта. Жёлто-красная тепловая карта — принятое исключение.\n- Структура проверена на всех 55 экранах. Скриншоты использованы выборочно для спорных мест; это не покадровая визуальная приёмка всех скрытых вариантов. Figma-макеты не доказывают работу клавиатуры, запросов и маршрутов в приложении.\n- `P1` — желательно закрыть до передачи сценария в разработку; `P2` — консистентность/документация; `P3` — технический долг. Это приоритет аудита, не новый продуктовый scope.')

emit('\n## 1. Отвязанные элементы вместо экземпляров')
emit('Подтверждённых имитаций не найдено. Проверка native FRAME/GROUP/RECTANGLE использовала ≥2 признака: размер ±10 px, цвет ±5 RGB и анатомию (типы детей/количество текстов). Получено 43 кандидата, все отклонены после проверки назначения. Это не доказательство отсутствия detach в истории файла; API показывает текущую структуру.')
emit('\n- '+link('175:2787','ScenarioAnalysis')+' совпал с ResearchTableRow по размеру/цвету, но это подсказка из двух вертикальных текстов, а не ячейки.\n- Actions/InsightTabs/SignalsFindingsTabs — композиции из связанных экземпляров, не имитации строки таблицы.\n- TaskOne/TaskTwo, TestControls и FindingSavedNotice совпали с FirstClickTargets по общему каркасу «два текста + блок», но имеют другое назначение.\n- Полный список: `screens-audit-2026-09-23/native-candidates.json`. Автозамена по одной геометрии дала бы ошибочные результаты.')

emit('\n## 2. Цвета и эффекты без Variables')
emit('В видимых fills/strokes/градиентных остановках непривязанных цветов не обнаружено. Найдено **4 скрытые чёрные обводки** и **84 вхождения одного белого эффекта**, из них **8 видимых**. Все относятся к библиотечному Resize Handle поля; это не чёрная подложка Play/Pause и не ошибка пагинации.')
emit('\n**C1 · P3 · высокая уверенность в наличии, низкая в автоматической замене.** Четыре скрытые strokes #000000 находятся под поиском '+link('210:12295')+' и '+link('210:20553')+'. Подходящего по смыслу и цвету (±5 RGB) локального продуктового токена для чёрного bevel нет. Не назначать text/primary по приблизительному сходству.')
emit('\n**C2 · P3 · высокая уверенность.** Белый DROP_SHADOW rgba(255,255,255,.5), radius=0, offset=(.66,.66) создаёт фаску ручки resize. Виден в textarea '+link('207:6644','Projects / описание')+' и '+link('210:19710')+', '+link('210:19726')+', '+link('210:19773')+' в FindingEditor. `background/surface` и `text/inverse` совпадают только по RGB, но не по альфе/назначению; `shadow/card` имеет совсем другие геометрию и цвет. Безопасный готовый токен не найден. Если нормализовать — отдельный семантический токен фаски с сохранением .5 alpha и визуальной проверкой; массовый bind не рекомендован.')
emit('\nИтого: 2 группы технического долга, не 88 визуальных ошибок. Точные вложенные Node ID сохранены в scan-*.json и effectAudit.json. Стиль shadow/card связан с shadow/color; ошибок его привязки не найдено.')

emit('\n## 3. Подозрения на дубли компонентов')
emit('Однозначных кандидатов на объединение не подтверждено. Шесть пар совпали по грубой анатомии первого варианта:')
emit('\n| Пары | Почему не объединяем автоматически |\n|---|---|\n| ProductButton / ProductNavItem; ProductButton / ProductTab; ProductTab / ProductNavItem | Общая библиотечная оболочка из instance, но действие, навигация и вкладка имеют разную семантику и selected-состояния. |\n| TaskOutcome / RecordingCoverage | Одинаковая форма icon + text, но результат задания и полнота записи — независимые признаки. |\n| TaskOutcome / ProductCheckbox; RecordingCoverage / ProductCheckbox | Статус против управляемого ввода. Совпадение анатомии не означает общий компонент. |')
emit('\nДополнительно сопоставлены SummaryMetric/SuccessMetric и ScenarioTable/ParticipantsTable: карточка показателя против ячейки и разные предметные таблицы. Оснований автоматически удалять или объединять нет.')

emit('\n## 4. Неиспользуемые компоненты и реестр usedIn')
emit('В пределах Screens не используются '+link('86:370','DataCoverage')+', '+link('132:634','FirstClickTargetRow')+' и '+link('135:778','FirstClickTargets')+'. Их usedIn уже пуст; это **unused**, не stale. Наличие в UI Kit полезно для предусмотренных состояний. DataCoverage только что утверждён пользователем — удаление не предлагается. Проверка не утверждает отсутствие использования на других страницах файла.')
emit('\n| ID | Расхождение | Предлагаемая точечная правка |\n|---|---|---|\n| D1 · P2 | ProductTab: 8 видимых экземпляров в SignalsByPage, SignalsPageDetails, Findings, FindingDetails, но usedIn пуст. В ds/components.md:1382 написано «не используется», ниже :1444 уже описано применение. | Обновить запись usedIn в ds/index.json и актуальную сводку ds/components.md; позднюю историю сохранить. |\n| D2 · P2 | ProductCheckbox: 7 экземпляров в Report, usedIn пуст; текстовый раздел :1444 применение знает. | Добавить screens/report в реестр. |\n| D3 · P2 | ProductField: screens/launch-active записан в usedIn, экземпляра на экране нет. | Удалить только устаревшую ссылку из реестра и сводки. |')
emit('\nУверенность высокая: сопоставлены mainComponent, включая вложенные экземпляры, и все 55 экранов. До/после для этих трёх правок не требует визуального изменения макетов. Сейчас каталог оставлен без изменений.')

emit('\n## 5. Матрица вариантов и консистентность состояний')
emit('В Screens используются **62 из 168 вариантов** (включая скрытые состояния); 106 не размещены. Отсутствие Hover/Focus/Pressed на статическом экране само по себе не дефект. Они доступны в ДС; удалять их не нужно.')
emit('\n**S1 · P1 · подтверждено визуально и структурно.** В '+link('210:13333','Signals / InsightTabs')+' экземпляры `210:13334`, `210:13341`, а в '+link('210:18724','FindingsEmpty / Actions')+' — `210:18725`, `210:18732` ссылаются на ProductButton Secondary Default. В обеих парах нет selected-вкладки. У соседних экранов стоят прозрачные ProductTab с нижним индикатором. Это не detach, а неправильное применение существующего компонента.')
emit('\nПредлагаемое исправление S1: заменить только 4 этих экземпляра на ProductTab `Selected=True/False, State=Default, Size=Small`, сохранить подписи; в Signals выбрать «Сигналы», в FindingsEmpty — «Находки · 0». Ширина 180 px, прозрачная подложка и индикатор — как на '+link('210:17407','SignalsByPage')+' и '+link('210:18322','Findings')+'. Проверка после замены: обе вкладки на одной высоте, ровно одна выбрана, selected сохраняется для пустого состояния. Сам стиль утверждённых кнопок не менять.')
emit('\n| Набор | Определено / использовано | Видимых экземпляров | На экранах, включая скрытые |\n|---|---:|---:|---|')
for u in usage:
    emit(f'| {link(u["id"], u["name"])} | {u["defined"]} / {u["used"]} | {u["visibleInstances"]} | '+', '.join(s['name'].removeprefix('Screen/') for s in u['screens'])+' |')
emit('\nПолные имена и IDs использованных/неиспользованных вариантов — в `screens-audit-2026-09-23/report-data.json`. Значимые пробелы применения: у ProductField на экранах только Default; у ParticipantsTable только Ready, остальные 4 состояния доступны в ДС; у ReplayControls на экранах Paused, Playing доступен в ДС; у ProductCheckbox размещён только On/Default. Это входы в проверку 6, а не требование нарисовать все 106 вариантов на отдельных экранах.')

emit('\n## 6. Покрытие состояний — бриф следующей итерации')
emit('Таблица объединяет связанные экраны в 17 семейств. Различаются: «показано на экране», «доступно в ДС» и «не задано». Варианты компонента засчитаны в покрытие соответствующего блока, но не заменяют состояние всей формы/холста. Ошибочная страница не обязана иметь собственную ошибочную страницу. Общие Header/NavMenu/статические подписи не требуют empty/loading/deleted.')
emit('\n| Семейство / тип блока | Уже предусмотрено | Пробел или решение следующей итерации | Приоритет |\n|---|---|---|---|')
for f in families:
    emit('| '+f[0]+' — '+f[2]+' | '+f[3]+' | '+f[4]+' | '+f[5]+' |')
emit('\nПорядок проработки: (1) формы создания/редактирования — ошибки, сохранение и восстановление; (2) списки и аналитические холсты — загрузка/ошибка/пустая выборка; (3) свежесть данных и недоступный объект; (4) повторные операции и mobile-ошибки. Для каждого состояния сохранить текущий контекст выборки и полезный ввод, дать конкретное действие восстановления. Это отдельный бриф для final_screens, не автоматическая генерация в режиме аудита.')
emit('\nОткрытые решения доступа: `ia/open-questions.md`, IA04/D08. Signup, PasswordReset, SessionExpired и требования оплаты намеренно не объявлены обязательными. Конфликт правки двумя коллегами требует решения о совместной работе, а не случайно выбранного варианта UI.')

emit('\n## Дополнительная геометрическая проверка')
emit('Автоматический обход отметил 15 вертикальных выходов и 0 горизонтальных. После проверки содержимого ни один не подтверждён как видимый текстовый артефакт:')
emit('\n- Девять `SummaryMetric/Detail` в Funnel, ParticipantDetails и ResultsFree выходят на 4–8 px, но characters пусты. Скриншот Funnel подтверждает целую карточку. P3: скрывать пустой Detail либо обеспечивать HUG при заполнении, иначе добавленный позже текст может выйти за край. Не называть текущую ситуацию обрезанным текстом.\n- Четыре handle ползунка Replay выходят вверх на 8 px намеренно. Круги не следует обрезать или растягивать ради нулевого overflow.\n- `175:2642` выходит ниже Main `175:776` на 60 px; Main имеет VERTICAL scrolling, вертикальная прокрутка предусмотрена спецификацией. Статический экспорт обрезает нижнюю часть viewport — это ожидаемо; работу прокрутки в интерактивном просмотре этот аудит не проверял.\n- `210:15000` Demo click layer в динамической карте на 24 px выше по размеру, чем доступная внутренняя область из-за offset. Сами пять hotspots помещаются в снимок (нижний край локально 363 + 24 < 432), визуальный выход не подтверждён. P3: привести техническую рамку overlay к внутренней области при следующей работе с холстом, не менять позиции кликов вслепую.')

emit('\n## Полный реестр 55 проверенных экранов')
emit('Для каждого экрана ниже указаны его рабочие секции; состояния этих секций описаны в соответствующем семействе выше. Вложенные формы в overlays учтены в семьях Projects/Setup/Findings. Имена композиций и контрольные суммы прочитанных файлов сохранены в inputs.json.')
emit('\n| Экран | Узлов | Семейство | Секции Main / корня |\n|---|---:|---|---|')
for s in screens:
    name=s['name'].removeprefix('Screen/')
    blocks='; '.join(dict.fromkeys(b['name'] for b in s['blocks']))
    emit(f'| {link(s["id"],name)} | {s["nodeCount"]} | {family_for[name][0]} | {blocks} |')

emit('\n## Что выполнено и что не изменено')
emit('Все шесть проверок завершены. Исправлений в Figma: **0**. Изменений в ds/components.md, ds/index.json, ds/screens: **0**. Ничего не помечено как «осознанно пропущено» без решения пользователя. Сохранены доказательства и воспроизводимый сборщик `execution/screens_audit_readonly.py`, отчёт строится `execution/build_screens_audit_report.py`.')
emit('\nКонкретные решения для следующего шага: **S1** — 4 вкладки на двух экранах; **D1/D2/D3** — синхронизация трёх записей использования; по **C1/C2** рекомендовано не менять встроенный декор без отдельного токена. По каждой группе можно выбрать «чинить», «пропустить» или «не решать сейчас». Покрытие состояний из раздела 6 — отдельная итерация final_screens после выбора объёма.')
emit('\nОснование режима: директива говорит «По умолчанию только чтение» и «Каждый автофикс — через явный апрув в чате». Текущий запрос был без `--fix`, поэтому отчёт не переходит в правки автоматически.')

target=ROOT/'.tmp/screens_audit_2026-09-23.md'
if target.exists():
    raise SystemExit('Report already exists; choose a new run filename to preserve history.')
target.write_text('\n'.join(out)+'\n', encoding='utf-8')
print(json.dumps({'report':str(target),'stats':stats,'familyCount':len(families),'catalogMismatches':[u['name'] for u in usage if u['missingUsedIn'] or u['staleUsedIn']]}, ensure_ascii=False))
