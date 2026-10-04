"""Read the scanned catalog and prepare the directive's approval artifact."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DRAFT = r'''# Расширение UI-кита — черновик на согласование

Статус: описания подготовлены; апрув не получен; Figma в рамках этой директивы не изменялась. Новые компоненты в основной каталог не записаны.

## Решение по объёму

Предлагаются три составных компонента для UX-исследований: HeatmapLegend, ReplayControls, DataCoverage. Это оболочки из существующих элементов, а не новые базовые кнопки, таблицы или поля. После согласования проверить ближайшие компоненты в исходном Figma: если они уже решают задачу целиком, переиспользовать их вместо создания дубля.

В каталоге есть Data Grid и Table Cell, Tabs, Tooltip, Popover и Selectable List, Select field, Toast, Breadcrumbs, Pagination. Базовые восемь примеров из директивы заново не создаются. Tabs, Tooltip, Select field, Selectable List и часть кнопок помечены Deprecated: не подменять их самовольно новой версией Borealis. Результаты проверки каталога и все 204 имени — в grow_ui_kit_catalog_check.md рядом с этим файлом.

## Файл и Foundation: обязательная зависимость перед отрисовкой

Целевой файл — Dashboard, `1LeVoicxDT7Sl8TpMPs4hr`, в котором находятся wireframes. Источник — Elastic UI (Copy), `SNBSKtwsO81j3BdjRGFpAw`. Это два разных файла, в отличие от предпосылки директивы. В последней проверке Dashboard до цветовой примерки не было локальных Text Styles или размерных Variables; затем добавлены только 20 цветовых Variables. Наличие Section Foundation в Dashboard не подтверждено.

После апрува сначала проверить актуальное состояние и доступность импорта исходных компонентов, размерных Variables и существующих Text Styles в Dashboard. Использовать опубликованные стили через импорт, сохраняя их происхождение и привязки. Новые Text Styles в grow_ui_kit не создавать. При невозможности импорта или отсутствии требуемых токенов отдельно закрыть Foundation, не рисовать неподвязанные заменители. Не создавать новый Figma-файл и не переписывать исходную Elastic UI.

UI Kit — extended разместить рядом с Foundation после подтверждения/подготовки этой основы. Использовать существующую секцию при повторном прогоне. Каталог остаётся снимком Elastic UI до появления реально созданных дополнений; у дополнений указывать файл Dashboard и реальные Node ID.

## Общие правила трёх компонентов

- Автолейаут; настоящие ComponentSet/Component и вложенные instances. Латинские имена слоёв и свойств, русский пользовательский текст.
- Сохранить шкалы Elastic UI: Size/X-Small, Small, Medium, Base, Large, X-Large; радиусы Radius/Small и Radius/Medium. Это существующие названия, не вводить параллельную space-* шкалу ради шаблона директивы. Значения 4/8/12/16/24/32 и 4/6 приведены только для сверки, в Figma применяются bindings.
- Цвета поверхностей, текста и статусов — смысловые Variables из product-palette.json. Никаких raw HEX на слоях.
- Типографика — существующие Text Styles из foundation.md; основные подписи через Body Copy/Regular и Medium, вспомогательные через Fine Print/Regular. У исходных стилей есть Deprecated-маркер: сохранять provenance, не выдавать их за новую версию библиотеки. Проверить Variable bindings и кириллицу до использования.
- Лейбл плитки брать из имеющегося стиля подписи, без создания отсутствующего Label/xs.
- Две-три визуальные разновидности на компонент. Полная матрица hover/focus/disabled/loading — отдельное расширение; не выдавать эти состояния за выполненные сейчас.
- Связь с UI-прототипом не означает реализацию работающего сбора данных, проигрывателя или расчёта карты.

### HeatmapLegend

**Назначение:** объяснять единицу и интенсивность тепловой карты на экранах Heatmaps, HeatmapsFirstClick и в отчёте.

**Проверка дублей:** Color Palette Display (`15884:173623`) показывает палитру, но каталог не подтверждает подписи единицы анализа и базы выборки; Color Palette Picker — выбор палитры, другая задача. Сначала проверить возможность вложить существующее отображение шкалы. Не создавать второй picker.

**Анатомия:** ModeLabel; IntensityScale; ScaleLabels; SampleBase; DefinitionNote. Видны режим, «Меньше — больше кликов», число представленных кликов/участников и область применения шкалы. Первый клик имеет отдельную подпись единицы отсчёта.

**Варианты:** `Mode=AllClicks | FirstClick` — 2 варианта.

**Состояния:** заполненные данные в обоих вариантах. Нет данных — композиция существующего Empty Prompt на уровне экрана; не показывать фиктивный ноль. В первом клике незакрытое определение D02 явно отмечается «Единица отсчёта: требуется определить».

**Отступы:** Size/Small между подписями, Size/Medium между группами; контейнер Size/Base; радиус Radius/Small при наличии фона.

**Привязки:** поверхность background/surface, граница border/subtle, текст text/primary и text/secondary. Шкала интенсивности требует отдельных semantic-токенов heatmap/intensity/* в Foundation: не подменять её цветами success/error или оливковым выделением строки. Готовые числовые пороги и алгоритм плотности не утверждаются этим компонентом. До появления согласованной и проверенной шкалы компонент нельзя объявить законченным.

**Типографика:** Body Copy/Medium для режима, Fine Print/Regular для базы и концов шкалы; через существующие Text Styles и их Variables.

### ReplayControls

**Назначение:** управлять просмотром восстановленной сессии и показывать разрыв записи на Replay/ReplayIncomplete.

**Проверка дублей:** Timeline (`26861:286195`) — вертикальная лента с иконкой/контентом, не transport плеера; Slider/Track и части Slider есть в каталоге. Проверить их переиспользование для шкалы; использовать существующие кнопки/иконки, не делать новые атомы.

**Анатомия:** TimeTrack; EventMarkers; GapRange; PlaybackAction; PositionLabel; SpeedControl; FitAction. Демо: «02:18 / 04:32», «Скорость: 1×», «Вписать»; для разрыва «Нет данных: 01:40–02:05». Воспроизведение/пауза меняют существующую иконку и подпись вложенной кнопки.

**Варианты:** `Coverage=Complete | Gap` — 2 варианта. Не добавлять декартово произведение со скоростью и playback-состояниями.

**Состояния:** оба варианта показываются на паузе. Для Gap действия в потерянном интервале неизвестны; нельзя изображать непрерывную достоверную запись. Недоступная запись — существующий Empty Prompt с действием повторить/вернуться, вне этого component set.

**Отступы:** Size/Small внутри управления; Size/Base между группами и по краям; Radius/Small. Геометрия временного интервала зависит от длительности данных, а не от spacing-токенов; это не произвольный межэлементный отступ.

**Привязки:** background/surface, background/subtle; border/control; text/primary, text/secondary; action/primary и text/inverse; accent/strong для позиции; status/warning/background и status/warning/text для разрыва с текстовой подписью. Недостаток отдельного цвета дорожки решается в Foundation до построения, не hardcode.

**Типографика:** Body Copy/Medium для действий и позиции, Fine Print/Regular для временных меток и разрыва; существующие Text Styles.

**Границы:** камера, голос, автоматический пропуск пауз, новая настройка скорости или клавиатурные shortcuts не добавляются к брифу этой директивой. Доступность управления с клавиатуры документируется при реализации, но не выдаётся за проверенную в статическом макете.

### DataCoverage

**Назначение:** одинаково обозначать полноту данных в списке участников, деталях участника и записи; отделять качество записи от успеха задания.

**Проверка дублей:** Callout (`32350:392160`), Stat (`14638:71133`), .Status и Progress уже есть. Новый блок — повторяемая композиция статуса и пояснения, а не новая версия Badge или Callout; если нужное сочетание реализуется готовым instance без новой структуры, оставить его документированным паттерном и не создавать дубль.

**Анатомия:** StatusIcon; StatusLabel; DetailText; OptionalAction. Свойства DetailText (TEXT), ShowAction (BOOLEAN), ActionLabel (TEXT). Для агрегата передавать «2 из 20» текстом, без нового варианта и без вычисления статистики в компоненте.

**Варианты:** `Coverage=Complete | Partial | Unavailable` — 3 варианта.

**Состояния:** «Данные полные» — зелёный смысловой статус; «Данные неполные» — предупреждение с причиной; «Запись недоступна» — нейтральное состояние с известной причиной. Временная ошибка загрузки не доказывает потерю исходных данных. Неполная запись не означает неуспешное задание.

**Отступы:** Size/Small между иконкой/подписью, Size/X-Small между текстовыми строками, Size/Medium по краям; Radius/Small.

**Привязки:** background/surface и border/subtle; text/primary, text/secondary; status/success/background и status/success/text; status/warning/background и status/warning/text. Для недоступной записи — background/subtle и text/secondary. Иконки наследуют semantic-цвет текста.

**Типографика:** Body Copy/Medium для статуса, Fine Print/Regular для причины; существующие Text Styles. Цвет не является единственным признаком состояния.

## Проверка после согласования и отрисовки

1. Перед созданием повторно проверить дубли и готовность Foundation в Dashboard.
2. Создавать небольшими пакетами согласно директиве, каждый проверять отдельным чтением и screenshot. Не отсоединять вложенные instances.
3. Проверять Component/ComponentSet, число вариантов 2/2/3, текстовые стили, bindings цветов/радиусов/spacing, длинные русские подписи и отсутствие обрезки.
4. Аудит: каждый компонент → пройдено / конкретное расхождение. Исправить расхождения до объявления готовности.
5. Только после фактического создания внести реальные Node ID в ds/components.md и ds/index.json; сохранять fileKey для отличия source от product extensions.

## Согласование

Подтвердить предложенные HeatmapLegend, ReplayControls и DataCoverage либо отметить исключения. Это согласование текстового состава и минимальных вариантов; реализация зависит от проверки/подготовки Foundation и импорта. Публикация библиотеки или создание новых шрифтовых стилей этим черновиком не выполняется.
'''


def main():
    if '--record-preflight' in sys.argv:
        out = ROOT / 'ds/.tmp'
        out.mkdir(parents=True, exist_ok=True)
        draft = out / 'grow_ui_kit_draft.md'
        current = draft.read_text(encoding='utf-8')
        current = current.replace('Статус: описания подготовлены; апрув не получен; Figma в рамках этой директивы не изменялась. Новые компоненты в основной каталог не записаны.', 'Статус: пользователь подтвердил все три описания. Проверка Foundation выявила недоступный импорт. Новые компоненты ещё не созданы и не записаны в основной каталог; повторный апрув состава не требуется.')
        draft.write_text(current, encoding='utf-8')
        status = {
            'approved': ['HeatmapLegend', 'ReplayControls', 'DataCoverage'],
            'status': 'blocked_on_foundation_import',
            'targetFileKey': '1LeVoicxDT7Sl8TpMPs4hr',
            'sourceFileKey': 'SNBSKtwsO81j3BdjRGFpAw',
            'targetLocalTextStyles': 0,
            'targetLocalVariables': {'COLOR': 20, 'FLOAT': 0},
            'importChecks': [
                {'kind':'style','key':'055057128653b8e0591ad4af0f3f89ef9b2a5065','result':'not found'},
                {'kind':'variable','key':'723a30bab117da7a71b48251ea5a84eb3614f264','result':'not found','publishStatus':'UNPUBLISHED'},
                {'kind':'componentSet','key':'4458604dc6ab94c6e37132d13dcb44b9f4869305','result':'not found','publishStatus':'UNPUBLISHED'},
            ],
            'stylePublishStatus': 'API unavailable: TypeError: not a function',
            'browserFallback': 'No connected browsers; iab unavailable',
            'createdComponents': [],
            'auditPassed': False,
            'nextStep': 'Make source components, variables and existing text styles available in Dashboard; resume without repeating scope approval',
        }
        (ROOT / 'ds/grow-ui-kit-status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        (ROOT / 'ds/grow-ui-kit-status.md').write_text('''# UI Kit extension: статус

Состав подтверждён пользователем: HeatmapLegend, ReplayControls, DataCoverage. Повторное согласование этих описаний не требуется.

## Проверено

- Dashboard: 20 цветовых Variables, 0 локальных Text Styles, 0 локальных размерных Variables.
- В доступных/подключённых библиотеках Dashboard Elastic UI не показана.
- Импорт по проверенным ключам стиля, Size/Base и .Button Group / Button возвращает not found.
- Компонент .Button Group / Button и токен Size/Base в исходном файле имеют UNPUBLISHED. Статус публикации текстового стиля данным API получить не удалось.
- Запасной путь через интерфейс недоступен: список браузеров пуст; iab unavailable.
- После проверки количество страниц и Variables Dashboard осталось прежним. Компоненты не созданы, каталог не дополнен вымышленными ID. Аудит компонентов ещё не выполнен.

## Что нужно для продолжения

Сделать исходную библиотеку доступной из Dashboard через публикацию/подключение либо перенос существующей основы в Dashboard с сохранением компонентных связей, Variables и Text Styles. После этого повторить импорт и проверку привязок; затем подготовить Foundation, собрать утверждённые 2/2/3 варианта, визуально проверить и внести реальные ID в каталог.

Не создавать новые Text Styles или похожие базовые компоненты в обход требований grow_ui_kit. Цветовая примерка ResultsOverview не заменяет Foundation.
''', encoding='utf-8')
        print(json.dumps(status, ensure_ascii=False))
        return
    catalog = (ROOT / 'ds/components.md').read_text(encoding='utf-8-sig')
    names = re.findall(r'^### (.+)$', catalog, re.M)
    assert len(names) == 204, f'Catalog changed: {len(names)} entries; review required'
    candidates = ['HeatmapLegend', 'ReplayControls', 'DataCoverage']
    assert not set(candidates).intersection(names)
    out = ROOT / 'ds/.tmp'
    out.mkdir(parents=True, exist_ok=True)
    if not (ROOT / 'ds/grow-ui-kit-status.json').exists():
        (out / 'grow_ui_kit_draft.md').write_text(DRAFT, encoding='utf-8')
    inventory = '# Проверка каталога перед расширением\n\nПрочитано 204 заголовка. Точное совпадение имён трёх кандидатов не найдено; семантическую заменимость проверять отдельно. Каталог ограничен глубиной ds_scan.\n\n' + '\n'.join(f'{i}. {name}' for i, name in enumerate(names, 1)) + '\n'
    (out / 'grow_ui_kit_catalog_check.md').write_text(inventory, encoding='utf-8')
    source = Path('C:/Users/InfDesign/Downloads/directive_grow_ui_kit.md')
    target = ROOT / 'directives/directive_grow_ui_kit.md'
    if not target.exists():
        target.write_text(source.read_text(encoding='utf-8-sig'), encoding='utf-8')
    print(json.dumps({'catalogCount': len(names), 'draft': str(out / 'grow_ui_kit_draft.md'), 'proposed': candidates, 'figmaChanged': False, 'status': 'awaiting_description_approval'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
