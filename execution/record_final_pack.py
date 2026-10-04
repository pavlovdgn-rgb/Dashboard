"""Publish the verified Figma screen inventory into project documentation.

Consumes read-back evidence, never infers completion from successful creation.
The source Elastic catalog stays unchanged; product extensions are separate.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / 'ds'
SCREENS = DS / 'screens'
BASE = 'https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def slug(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()


def link(node_id):
    return BASE + node_id.replace(':', '-')


def append_once(path, marker, body):
    text = path.read_text(encoding='utf-8')
    if marker not in text:
        path.write_text(text.rstrip() + '\n\n' + marker + '\n' + body.strip() + '\n', encoding='utf-8')


def main():
    evidence = read(ROOT / '.tmp/final-pack/delivery-evidence.json')
    latest = ROOT / '.tmp/final-pack/latest-audit.json'
    audit = read(latest) if latest.exists() else evidence['audit']
    names = {s['name'] for s in audit['screens']}
    assert audit['passed'] and audit['screenCount'] == 55
    assert not any(s['issues'] for s in audit['screens'])
    assert names == set(evidence['visualReviewed']), 'Every screen needs visual review'
    assert evidence['registry']['componentCount'] == 20
    assert evidence['registry']['variantCount'] == 148
    receipts = {r['name']: r for r in evidence['receipts']}
    receipts['ResultsOverview'] = {'sourceId': '22:3', 'screenId': '175:614'}
    assert set(receipts) == names
    index = read(DS / 'index.json')
    ext = index['productExtensions']
    components_by_id = {c['id']: c for c in ext['components']}
    for component in evidence['registry']['components']:
        current = components_by_id.setdefault(component['id'], {'type': 'COMPONENT_SET'})
        current.update(component)
        current['usedIn'] = sorted('screens/' + slug(name) for name, ids in evidence['usage'].items() if component['id'] in ids)
    ext['components'] = list(components_by_id.values())
    ext['componentCount'] = len(ext['components'])
    ext['variantCount'] = sum(len(c['variants']) for c in ext['components'])
    assert (ext['componentCount'], ext['variantCount']) == (20, 148)
    ext['heatmapVariables'] = [v for v in evidence['tokens'] if v['name'].startswith('heatmap/')]
    ext['thermalAndRadiusVariables'] = evidence['tokens']
    ext['date'] = evidence['date']
    ext['finalScreensPageId'] = '191:847'
    ext['finalScreens'] = {}
    manifest = {'fileKey': '1LeVoicxDT7Sl8TpMPs4hr', 'pageId': '191:847', 'sectionId': '175:613',
                'date': evidence['date'], 'screenCount': 55, 'desktopCount': 51, 'mobileCount': 4,
                'prototypeWired': False, 'screens': []}
    table = ['| Экран / состояние | Макет | Размер | Спецификация |', '| --- | --- | --- | --- |']
    for screen in audit['screens']:
        name = screen['name']
        receipt = receipts[name]
        assert screen['id'] == receipt['screenId']
        used = [components_by_id[c]['name'] for c in evidence['usage'][name]]
        info = dict(name=name, id=screen['id'], sourceId=receipt['sourceId'], width=screen['width'], height=screen['height'],
                    auditPassed=True, visuallyReviewed=True, url=link(screen['id']), componentSets=evidence['usage'][name])
        manifest['screens'].append(info)
        ext['finalScreens'][name] = {k: v for k, v in info.items() if k != 'name'}
        path = SCREENS / (slug(name) + '.md')
        assert path.exists(), str(path)
        content = path.read_text(encoding='utf-8').replace(
            'Статус: composition map; сборка разрешена пользователем для всего пакета без повторного апрува.',
            'Статус: финальный макет создан и проверен 23 сентября 2026 года.')
        path.write_text(content, encoding='utf-8')
        append_once(path, '<!-- final-pack-delivery-2026-09-23 -->', f'''
## Проверенная передача

[Открыть финальный экран]({info['url']}) · Node `{screen['id']}` · {screen['width']} × {screen['height']}.
Страница **UX-Lab · Final Screens**, секция Screens. Источник wireframe `{receipt['sourceId']}` сохранён.

Фактически использованные локальные наборы: {', '.join(used) if used else 'нет; экран состоит из текстов и контейнеров с токенами'}.
Данные таблицы: связанные экземпляры компонентов; уникальные композиционные контейнеры — native Auto Layout.

Проверено: видимый экран, ширина дочерних элементов, привязки цветов и градиентов, Text Styles.
Проверка ширины не является автоматическим тестом всех адаптивных размеров или интерактивного поведения.
Все данные демонстрационные. Связи кликабельного прототипа не настроены.
''')
        table.append(f'| {name} | [Figma]({info["url"]}) | {screen["width"]} × {screen["height"]} | [{slug(name)}]({slug(name)}.md) |')
    audit['checkedAt'] = evidence['date']
    audit['visuallyReviewedScreens'] = sorted(names)
    audit['scope'] = 'Visible nodes: horizontal overflow, semantic color bindings including gradient stops, text styles; manual screenshots of 55 frames.'
    write(SCREENS / 'final-pack-audit.json', audit)
    write(SCREENS / 'final-pack.json', manifest)
    write(DS / 'index.json', index)
    write(DS / 'thermal-radius-tokens.json', evidence['tokens'])
    write(DS / 'close-button-icons.json', evidence['closeIcons'])
    status = read(DS / 'grow-ui-kit-status.json')
    status.update(componentCount=20, variantCount=148, createdComponents=ext['components'])
    status['finalScreensExtension'] = {'date': evidence['date'], 'pageId': '191:847', 'screenCount': 55,
                                     'newComponents': ['SummaryMetric', 'ProductField', 'ResearchTableRow'],
                                     'audit': 'ds/screens/final-pack-audit.json', 'prototypeWired': False}
    write(DS / 'grow-ui-kit-status.json', status)
    header = f'''# Финальные экраны

Проверено 23 сентября 2026: **55 макетов — 51 desktop и 4 mobile**.
[Страница UX-Lab · Final Screens]({link('191:847')}).

Desktop: 1920 × 1080; экраны участника на телефоне: 390 × 844.
Это редактируемые дизайн-макеты с демонстрационными данными, а не работающий сервис или связанный кликабельный прототип.
Исходные wireframes сохранены. Пустые, ошибочные и мобильные состояния из исходного пакета представлены отдельными фреймами; у ResultsOverview также сохранены внутренние состояния.

Тепловые карты и легенда: жёлтый → оранжевый → красный по wireframe `22:101`; элементы управления — в палитре продукта.
Радиус крупных поверхностей — 12 px. Текущий Secondary сохранён; вопрос различимости Tertiary на белом фоне отложен пользователем.

'''
    (SCREENS / '_index.md').write_text(header + '\n'.join(table) + '\n', encoding='utf-8')
    (SCREENS / 'queue.md').write_text('# Очередь final_screens — завершённый пакет\n\nВсе 55 исходников/состояний имеют финальный макет и пройденную проверку.\n\n' + '\n'.join(table) + '\n', encoding='utf-8')
    usage_lines = '\n'.join(f'- **{c["name"]}** `{c["id"]}`: ' + (', '.join(c['usedIn']) or 'в этом пакете напрямую не используется') + '.' for c in ext['components'])
    append_once(DS / 'components.md', '<!-- final-pack-2026-09-23 -->', '''
## Полный пакет final_screens · 23 сентября 2026

Текущий локальный UI-кит: **20 наборов, 148 вариантов**. Исторические числа выше относятся к предыдущим срезам; исходные 204 элемента Elastic не изменены.

- ProductField `203:4474`: Text / Textarea / Select / Search / Password × Default / Focus / Invalid / Disabled — 20 вариантов; вложенный Form Control Elastic сохранён. Label и Help — свойства; значение редактируется в InputValue. ShowHelp включает пояснение.
- ResearchTableRow `203:5669`: 2–8 колонок × Default / Zebra / Selected / Header — 28 вариантов; ячейки Elastic остаются instances и растягиваются по ширине строки.
- Кнопки закрытия: ProductButton с вложенным Elastic Button, `Icon only=True`, INSTANCE_SWAP на библиотечный `cross` (`106:617`, key `ccaa0c0dfc78be0e85701649b3d8b6393f842c36`). Зона 40×40, без текстового символа ×. Доступное имя для реализации — «Закрыть».
- ReplayControls: группы управления переносятся при узкой колонке, временные маркеры сохраняют относительное положение.

Фактическое использование в финальных экранах:

''' + usage_lines)
    append_once(DS / 'foundation.md', '<!-- thermal-final-2026-09-23 -->', '''
## Цветовая шкала тепловой карты · 23 сентября 2026

По прямому указанию пользователя прежняя оливковая шкала заменена на **жёлтую → оранжевую → красную**, как в wireframe `22:101` (пятна `57:3`). Это шкала данных, а не фирменный акцент.
`heatmap/intensity/1…10` теперь aliases к отдельным thermal-примитивам: #FFF8DF, #FFF0B8, #FFE788, #FFDB36, #FFC630, #FFAC29, #FF8C22, #F77323, #ED5525, #E33C26.
Радиальный слой: core #E33C26 / 70%, middle #FF8C22 / 56%, outer #FFDA36 / 30%, edge #FFDF38 / 0%. Позиции: 0, 0.36, 0.72, 1.
Идентификаторы, scopes, aliases и codeSyntax прочитаны из Figma: [thermal-radius-tokens.json](thermal-radius-tokens.json).
Три финальных режима карты и HeatmapLegend синхронизированы. Алгоритм плотности и числовые границы шкалы не выведены из демонстрационных пятен.
''')
    append_once(DS / 'CONTRACT.md', '<!-- final-pack-status-2026-09-23 -->', '''
## Актуализация · 23 сентября 2026

После явного разрешения пользователя собран пакет 55 финальных экранов на отдельной странице `191:847`, [реестр](screens/_index.md).
Исходный каталог выше остаётся снимком скана. Для продукта дополнительно применяются 20 локальных наборов / 148 вариантов, смысловые цвета и radius/surface=12.
Тепловая карта использует отдельную жёлто-оранжево-красную шкалу по указанию пользователя; брендовые элементы управления сохраняют оливковую палитру.
Подключение Elastic и кириллица проверены в использованных экземплярах. Это не подтверждение доступности каждой исходной внешней зависимости.
''')
    append_once(DS / 'source.md', '<!-- final-product-status-2026-09-23 -->', f'''
## Текущее состояние продукта · 23 сентября 2026

Исторический исходный скан выше сохранён. Продуктовые расширения и экраны находятся в Dashboard:
[55 финальных макетов]({link('191:847')}); [реестр экранов](screens/_index.md).
UI-кит продукта: 20 наборов / 148 вариантов поверх подключённой Elastic UI. Его токены не меняют исходную библиотеку.
Тепловая карта использует жёлтый → оранжевый → красный; фирменный оливковый применяется к контролам.
''')
    append_once(ROOT / 'ia/figma-delivery.md', '<!-- final-screen-pack-2026-09-23 -->', f'''
## Финальные экраны · 23 сентября 2026

[UX-Lab · Final Screens]({link('191:847')}) — 55 макетов, 51 desktop 1920×1080 и 4 mobile 390×844.
[Полный список со ссылками](../ds/screens/_index.md). Все 55 просмотрены; автоматический аудит видимых узлов пройден.
Wireframes и схемы сохранены. Это дизайн-макеты; интерактивные переходы прототипа не соединены.
''')
    append_once(ROOT / 'directives/directive_final_screens.md', '<!-- implementation-notes-2026-09-23 -->', '''
## Проверенные особенности исполнения — 23 сентября 2026

- Нельзя определять тип кнопки только по дочернему имени Control: оно также встречается у ProductField и ProductNavItem. Проверять ComponentSet ID мастера перед изменением размеров.
- Для контейнеров с внутренней обводкой проверять strokesIncludedInLayout: учитываемая обводка уменьшает доступную ширину; в финальных крупных поверхностях false.
- Переход FILL → FIXED требует явного resize текста на доступную ширину. После изменения размеров окна перепроверять заголовок и ряды кнопок.
- INSTANCE_SWAP для крестика закрытия — существующий Icon only=True у Elastic Button; не использовать символ ×. У вложенного instance minWidth может запрещать override; исправлять мастер, а не отсоединять экземпляр.
- Компоненты с длинными props/variants читать компактно: MCP обрезает слишком большой JSON. Отдельно получать варианты и свойства.
- Счётчики переиспользованного ParticipantsTable и HeatmapLegend переопределять для текущей выборки. Сводка и внутренняя таблица должны показывать одинаковую базу.
- Итог фиксировать record_final_pack.py после аудита и визуальной проверки всех экранов. Старый record_final_results.py описывает ранний этап с одним ResultsOverview и не подходит для перезаписи полного реестра.
''')
    append_once(DS / 'components.md', '<!-- control-spacing-2026-09-23 -->', '''
## Высота кнопок и строки таблиц · финальная сверка

У ProductButton наружный контейнер 40 px остаётся прозрачным, видимая заливка находится на вложенном Control высотой 32 px. Выбранное состояние меняет его цвет, а не высоту подложки. Исправлено 11 экземпляров; обычные кнопки не перекрашивались.
У таблиц строки и заголовок примыкают: itemSpacing=0. Зебра сохраняется; внутренние отступы ячеек не являются межстрочным расстоянием. Убраны 8 px в ControlChecklist, ParticipantTasks, ExploredPages и PageEvents; все 12 таблиц с ResearchTableRow проверены по фактическим координатам.
[Результат проверки](screens/control-spacing-audit.json). Правило пользователя: если UI-кит не определяет иное, зазоров между строками таблицы нет.
''')
    append_once(ROOT / 'directives/directive_final_screens.md', '<!-- control-spacing-rule-2026-09-23 -->', '''
### Высота выбранных кнопок и таблицы

В ProductButton не заливать наружный wrapper при выделении: это визуально меняет высоту с 32 до 40 px. Цвет менять на внутреннем Control. Таблицы определять по дочерним TableHeader/TableRow, а не только суффиксу Table; gap между строками 0 по прямому указанию пользователя. Проверять фактический y следующей строки минус нижняя граница предыдущей.
''')
    print(json.dumps({'screens': 55, 'components': 20, 'variants': 148, 'auditPassed': True, 'index': str(SCREENS / '_index.md')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
