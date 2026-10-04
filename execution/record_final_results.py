"""Record verified delivery; keep unfinished screens explicitly pending."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / 'ds'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def append_once(path, marker, body):
    text = path.read_text(encoding='utf-8')
    if marker not in text:
        path.write_text(text.rstrip() + '\n\n' + marker + '\n' + body.strip() + '\n', encoding='utf-8')

def main():
    audit = read(DS / 'screens/results-overview-audit.json')
    assert audit['passed'], 'Audit must pass before recording completion'
    index = read(DS / 'index.json')
    ext = index['productExtensions']
    for component in audit['components']:
        current = next((c for c in ext['components'] if c['name'] == component['name']), None)
        if current:
            current.update(component)
        else:
            ext['components'].append(component)
    used = {'SummaryMetric', 'ScenarioTable', 'ScenarioRow', 'SuccessMetric', 'NavMenu', 'ProductNavItem', 'ProductButton'}
    for component in ext['components']:
        if component['name'] in used:
            component['usedIn'] = sorted(set(component.get('usedIn', []) + ['screens/results-overview']))
    ext['componentCount'] = len(ext['components'])
    ext['variantCount'] = sum(len(c.get('variants', [])) for c in ext['components'])
    ext['finalScreens'] = {'ResultsOverview': {'id': audit['screenId'], 'auditPassed': True, 'states': len(audit['states'])}}
    write(DS / 'index.json', index)
    status = read(DS / 'grow-ui-kit-status.json')
    status['componentCount'] = ext['componentCount']
    status['variantCount'] = ext['variantCount']
    status['createdComponents'] = ext['components']
    status['finalScreensExtension'] = {'screenId': audit['screenId'], 'newComponent': 'SummaryMetric', 'newScenarioTableVariants': 2, 'audit': 'ds/screens/results-overview-audit.json'}
    write(DS / 'grow-ui-kit-status.json', status)
    refinements = read(DS / 'nav-secondary-refinements.json')
    refinements['secondaryProposals']['status'] = 'deferred by user; current secondary style retained'
    write(DS / 'nav-secondary-refinements.json', refinements)
    append_once(DS / 'components.md', '<!-- final-results-overview -->', '''
## Дополнение final_screens · ResultsOverview

- **SummaryMetric** — ComponentSet `171:1801`; Ready / Loading / NoData; Label, Value, Hint, ShowLink. [Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=171-1801). Used in: screens/results-overview.
- **ScenarioTable** `136:715` — теперь 7 вариантов: добавлены OverviewUnselected `172:1756` и OverviewSelected `172:1877`, 1536×512. Первоначальные 5 вариантов сохранены. Used in: screens/results-overview.
- **ScenarioRow**, **SuccessMetric**, **NavMenu**, **ProductNavItem**, **ProductButton** — Used in: screens/results-overview.
- ProductButton: убран унаследованный minWidth=172 у вложенного Control; FILL сохранён. Внешний вид secondary не менялся. Неиспользуемые скрытые иконки ProductNavItem привязаны к Variables.
- Текущий итог локального UI-кита: **18 наборов, 100 вариантов**; исходные 204 элемента библиотеки не изменялись.
''')
    append_once(DS / 'foundation.md', '<!-- final-results-shadow -->', '''
## Тень карточки · final_screens

- Primitive `black/4%`: RGBA(0,0,0,0.04), `VariableID:171:1757`, коллекция `UX-Lab · Primitives` (`VariableCollectionId:171:1756`). Scope пустой; CSS `var(--black-4-percent)`.
- Semantic `shadow/color`: alias к black/4%, `VariableID:171:1758`, scope EFFECT_COLOR; CSS `var(--shadow-color)`.
- Effect Style `shadow/card`, ID `S:33899efc313cd34c3be9f04a04d0853ed7091433,`: x=0, y=2, blur=8, spread=0. Цвет эффекта связан с shadow/color. Применён к SummaryMetric.
- Внешний исходный Plain/Dark не удалось импортировать, поэтому создан локальный примитив согласованного чёрного 4%. Цвета существующих контролов не менялись.
''')
    path = DS / 'screens/results-overview.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('Статус: на согласовании; финальный экран ещё не создан. Основание — локальные спецификации и реестр; актуальное состояние Figma проверяется после согласования.', 'Статус: согласовано пользователем; финальный экран создан и проверен в Figma 22 сентября 2026 года.')
    text = text.replace('Final Screen Node ID: —', 'Final Screen Node ID: `175:614` · [Открыть Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=175-614)')
    text = text.replace('## Доработки перед сборкой', '## Выполненные доработки').replace('Предлагаю добавить в UI-кит SummaryMetric:', 'Добавлен в UI-кит SummaryMetric `171:1801`:')
    text = text.replace('В каталоге нет подтверждённых продуктовых Effect Styles. Предложение: добавить shadow/card', 'Добавлен Effect Style shadow/card')
    text = text.replace('; новый стиль проверить после подключения к Figma.', '; привязка и параметры проверены в Figma.')
    path.write_text(text, encoding='utf-8')
    append_once(path, '<!-- delivery -->', '''
## Доставка и проверка

Секция Screens `175:613` на странице UX-Lab · Wireframes. Исходники wireframes сохранены.

Состояния Main: Ready `175:2642`, Selected `175:2790`, Loading `175:2975`, Error `175:3034`, Empty `175:3055`, FilteredEmpty `175:3253`, Overflow `175:3429`, FreeExploration `175:3574`. По умолчанию виден только Ready. Длинный контекст выбранного сценария продолжается в вертикальной прокрутке Main.

Это дизайн-макет: переходы кнопок и автоматическое переключение состояний ещё не соединены в кликабельный прототип. Для просмотра включить нужный State и скрыть остальные; у свободного изучения изменить подпись Mode, у FilteredEmpty — устройство на «Мобильное». Скрипт build_final_results.py show <State> формирует согласованное переключение всех этих слоёв.

Аудит включая скрытые состояния: 0 непривязанных цветов, 0 текстов без стиля, 0 переполнений компоновки по горизонтали. Шрифт Inter. Шесть проверок прогресс-баров соответствуют 14/18, 12/17, 10/15. Контраст: основной текст 15.67:1; вторичный 5.60:1; активное меню 4.70:1. Все восемь состояний просмотрены. [Машинный аудит](results-overview-audit.json).

На экране сохранены текущие secondary и активная подложка. Выбор новых вариантов их оформления отложен пользователем.
''')
    queue = DS / 'screens/queue.md'
    content = queue.read_text(encoding='utf-8').replace('| ResultsOverview | 22:3 | 1920 × 1080 | Карта на согласовании |', '| ResultsOverview | 22:3 | 1920 × 1080 | Готов: 175:614 |')
    queue.write_text(content, encoding='utf-8')
    (DS / 'screens/_index.md').write_text('''# Screens index

- [ResultsOverview](results-overview.md) — **готов**, Figma `175:614`, 1920×1080; основной вид и 7 дополнительных состояний.
- [Очередь](queue.md) — 55 исходников/состояний; остальные финальные экраны не объявлены готовыми.
''', encoding='utf-8')
    append_once(ROOT / 'directives/directive_final_screens.md', '<!-- implementation-notes-2026-09-22 -->', '''
## Проверенные особенности исполнения — 22 сентября 2026

- В текущем Figma MCP `overflowDirection` принимает `VERTICAL`, не `VERTICAL_SCROLLING`.
- Перед полным аудитом включать `figma.skipInvisibleInstanceChildren=false`: иначе скрытые вложенные слои могут не попасть в проверку. Видимость отдельных State не означает, что они не нуждаются в проверке.
- Проверять minWidth вложенного Control у ProductButton: ограничение 172 px приводило к выходу коротких кнопок за границы. В локальных мастерах ограничение снято; цвет и форма сохранены.
- Одна TEXT property на всех вариантах задаёт единое начальное значение. Для Loading/NoData не связывать служебное значение с Value основного состояния, иначе вместо «Загрузка…» появляется демонстрационное число.
''')
    assert ext['componentCount'] == 18 and ext['variantCount'] == 100
    print(json.dumps({'screen': audit['screenId'], 'components': ext['componentCount'], 'variants': ext['variantCount'], 'auditPassed': audit['passed']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
