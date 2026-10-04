"""Synchronize approved Secondary styling with the local design registry."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def write(path, value):
    (ROOT / path).write_text(value, encoding='utf-8')

def data(path):
    return json.loads(read(path))

def save(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def replace(path, old, new):
    value = read(path)
    if old in value:
        write(path, value.replace(old, new))
    elif new not in value:
        raise ValueError(f'Missing expected text in {path}: {old[:60]}')

audit = data('ds/secondary-choice-audit.json')
assert len(audit['pages']) == 7 and all(not p['pending'] for p in audit['pages'])
assert audit['geometryAudit']['passed'] and audit['geometryAudit']['screenCount'] == 55
decision = {
    'status': 'approved and applied', 'date': '2026-09-23',
    'choice': 'A without outline', 'componentSetId': '125:450',
    'tokens': audit['tokens'], 'audit': 'ds/secondary-choice-audit.json',
    'scannedPages': 7, 'verifiedControls': sum(p['okCount'] for p in audit['pages']),
    'focusRingRetained': True, 'selectedOliveRetained': True,
}
index = data('ds/index.json')
index['productExtensions']['secondaryChoice'] = decision
index['productExtensions']['secondaryContrastComparison'].update({
    'status': 'A without outline selected and applied', 'selectedOptionId': '237:11664',
    'legacyOptionId': '245:2920', 'legacyOptionExplicitFill': 'background/sidebar',
})
save('ds/index.json', index)
status = data('ds/grow-ui-kit-status.json')
status['secondaryChoice'] = decision
save('ds/grow-ui-kit-status.json', status)
nav = data('ds/nav-secondary-refinements.json')
nav['secondaryProposals'].update({
    'status': 'historical comparison; replaced by approved choice 237:11664',
    'appliedToMasters': True, 'currentChoice': decision,
})
save('ds/nav-secondary-refinements.json', nav)
palette = data('ds/product-palette.json')
palette['colors'].update({t['name']: t['hex'] for t in audit['tokens']})
palette['secondaryChoice'] = decision
save('ds/product-palette.json', palette)

marker = '<!-- secondary-approved-2026-09-23 -->'
note = '''

<!-- secondary-approved-2026-09-23 -->
## Secondary · выбран A без обводки

23 сентября 2026 пользователь утвердил образец A `237:11664` без контура. Все шесть состояний ProductButton Secondary обновлены, включая локальные заливки на страницах. Обычный фон — `action/secondary/background` #E4E5DC, Hover — `action/secondary/hover` #D8DACD, Pressed — `action/secondary/pressed` #CCD0BE. Семантика ссылается на отдельные neutral/secondary primitives; общий border/subtle не менялся.

Контур появляется только при клавиатурном фокусе; Disabled сохраняет opacity 0.4. Оливковые выбранные режимы и скорости сохранены. Primary и Tertiary не изменялись. Исторические варианты B/C/D и прежняя доска сравнения сохраняют собственные настройки.

Проверены 7 страниц: 378 обычных Secondary-контролов соответствуют новому стилю, устаревших применений среди них нет. На Final Screens — 248 контролов; проверка геометрии и привязок всех 55 экранов пройдена. [Аудит и токены](secondary-choice-audit.json).
'''
for path in ['ds/components.md', 'ds/foundation.md', 'ds/source.md']:
    content = read(path)
    if marker not in content:
        write(path, content.rstrip() + note)
replace('ds/components.md', 'Ранее отложенный вопрос оформления Secondary остаётся отдельным открытым вопросом.', 'Вопрос Secondary решён позднее: выбран A без обводки; см. актуальное решение ниже.')
replace('ds/components.md', 'Это предложения; утверждённые мастера кнопок не изменены.', 'Историческая запись примерки: позднее пользователь выбрал A без контура, мастера обновлены (см. ниже).')
replace('ds/components.md', 'Вариант D наследует оформление мастера `125:319`.', 'Вариант D теперь имеет явную историческую заливку background/sidebar.')
replace('ds/screens/_index.md', 'Текущий Secondary сохранён;', 'Secondary: утверждён A без контура (#E4E5DC), применён ко всем соответствующим кнопкам;')
old = 'Отложенные стили Secondary и Tertiary не пересматриваются.'
new = 'Secondary использует утверждённый A без контура и токены action/secondary/*. Вопрос Tertiary остаётся отложенным.'
for path in (ROOT / 'ds/screens').glob('*.md'):
    content = path.read_text(encoding='utf-8-sig')
    if old in content:
        path.write_text(content.replace(old, new), encoding='utf-8')
replace('execution/build_final_pack.py', old, new)
replace('execution/refine_secondary_buttons.py', "paint(State==='Hover'?'border/subtle':State==='Pressed'?'accent/soft':'background/sidebar')", "paint(State==='Hover'?'action/secondary/hover':State==='Pressed'?'action/secondary/pressed':'action/secondary/background')")
replace('execution/build_interaction_variants.py', "if(kind==='Secondary'&&state==='Hover')bg='border/subtle';", "if(kind==='Secondary')bg=state==='Hover'?'action/secondary/hover':state==='Pressed'?'action/secondary/pressed':'action/secondary/background';")
replace('execution/replace_close_button_icons.py', "v.name==='background/sidebar'", "v.name==='action/secondary/background'")
# Comparison is intentionally historical; regenerate A without outline and freeze D.
replace('execution/compare_secondary_contrast.py', "control.strokes=[paint(config.border)]", "control.strokes=config.border?[paint(config.border)]:[]")
replace('execution/compare_secondary_contrast.py', "title='A · Серый фон + контур',description='Рекомендую. Тёплая серая заливка и заметная граница на всех поверхностях.',fill='border/subtle',border='border/control'", "title='A · Выбран — без контура',description='Принят: тёплая серая заливка без контура.',fill='border/subtle',border=None")
replace('execution/compare_secondary_contrast.py', "title='D · Текущий стиль',description='Как сейчас на экранах: очень светлый тёплый серый фон, без контура. Образец для сравнения.',current=True", "title='D · Прежний стиль',description='Прежний стиль: очень светлый тёплый серый фон без контура.',fill='background/sidebar',border=None")
replace('execution/compare_secondary_contrast.py', 'Четыре оформления на одинаковых поверхностях. D — текущий стиль. Размеры и текст кнопок одинаковые. Стиль на экранах не изменён.', 'Выбран A без обводки; применён к Secondary на страницах продукта. D — прежний стиль для сравнения.')
replace('execution/compare_secondary_contrast.py', 'A — рекомендованный вариант. B — легче визуально. C — может восприниматься как выбранное состояние.', 'A — принят без контура. B и C сохранены для сравнения.')
replace('execution/compare_secondary_contrast.py', 'A — рекомендованный вариант. B — легче визуально. C — ближе к выбранному состоянию. D — текущие кнопки без изменений.', 'A — принят без контура. B/C/D сохранены для сравнения.')
print(json.dumps({'verifiedControls': decision['verifiedControls'], 'screens': 55, 'status': 'recorded'}))
