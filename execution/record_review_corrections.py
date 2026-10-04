"""Record verified replay, Studies and TaskChoiceCard corrections."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return (ROOT/path).read_text(encoding='utf-8-sig')
def write(path,text): (ROOT/path).write_text(text,encoding='utf-8')
def data(path):return json.loads(read(path))
def save(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def payload(result):return json.loads(next(c['text'] for c in result['content'] if c['type']=='text'))
def append(path,marker,text):
    old=read(path)
    if marker not in old:write(path,old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n')

receipt=data('ds/screens/review-corrections-audit.json')
assert receipt['finalAudit']['passed']
registry=payload(receipt['taskChoiceCard']['registry'])
component={'id':registry['setId'],'name':'TaskChoiceCard','type':'COMPONENT_SET','variants':registry['variants'],'properties':registry['properties'],'usedIn':['screens/task-picker'],'source':'Composition of themed Elastic Radio instances from ScenarioRow; source Radio set 135:828','auditPassed':True,'visualCheckPassed':True}
index=data('ds/index.json')
items=index['productExtensions']['components']
items[:]=[c for c in items if c['id']!=component['id']]+[component]
index['productExtensions']['reviewCorrections']='ds/screens/review-corrections-audit.json'
for c in items:
    if c['id']=='84:713':c['playbackAction']={'background':'accent/strong','foreground':'text/inverse','hex':'#626E32','variants':4}
save('ds/index.json',index)
status=data('ds/grow-ui-kit-status.json')
status.update({'createdComponents':items,'componentCount':len(items),'variantCount':sum(len(c.get('variants',[])) for c in items)})
save('ds/grow-ui-kit-status.json',status)
audit=data('ds/screens/final-pack-audit.json')
audit.update(receipt['finalAudit']);audit['reviewCorrections']='ds/screens/review-corrections-audit.json'
save('ds/screens/final-pack-audit.json',audit)

append('ds/components.md','<!-- task-choice-card-2026-09-23 -->','''
## TaskChoiceCard · выбор задания

[Компонент в UI Kit](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=260-3028), ComponentSet `260:3028`. Selected=False/True × State=Default/Hover/Focus/Disabled — 8 вариантов. Title и Description — редактируемые текстовые свойства. Радиоконтрол — связанный instance существующей Elastic Radio, не текстовый символ.

Выбранное состояние: accent/soft, контур accent/strong 2 px, отмеченный радиоконтрол и подпись «Выбрано». Hover выбранного усиливает внутренний контур до 3 px; Focus — отдельный внешний контур 3 px. Disabled — opacity 0.4. Поверхность radius/surface=12, padding 24, gap 16/8 из Dimensions, тексты используют существующие Text Styles.

В модальном TaskPicker три прежние native-карточки заменены instances. Действие выбирает ровно один вариант; в реализации нужны radiogroup, переключение стрелками и Space, область нажатия — вся карточка. Figma-прототип не подключён.

Текущий итог: **21 набор / 156 вариантов**. Исходный каталог Elastic сохранён.

ReplayControls: Play/Pause во всех четырёх вариантах используют accent/strong #626E32 с белым текстом и иконкой; красный replay/playhead сохранён.
''')
append('ds/source.md','<!-- review-corrections-2026-09-23 -->','''
## Уточнения после проверки экранов

Текущий UI Kit: **21 набор / 156 вариантов**, добавлен TaskChoiceCard (`260:3028`). В TaskPicker используются его instances. ReplayControls Play/Pause — accent/strong с белыми текстом/иконкой. В ReplayIncomplete поле «Имя» исправлено на HUG (76 px вместо ошибочных 40).
Studies: поиск слева, Select «Статус исследования» справа; Control одинаковой высоты 40 px. Карточки сводки детализированы по данным таблицы. Аудит: [review-corrections-audit.json](screens/review-corrections-audit.json).
''')
append('ds/screens/studies.md','<!-- studies-detail-2026-09-23 -->','''
## Детализация сводки и фильтры

Три SummaryMetric по 208 px. Всего: 3 исследования, по одному в каждом статусе; 2 с заданиями и 1 в свободном режиме. Сбор: 1 из 3 (33%), 20 участников. Черновики: 1 из 3 (33%), «Навигация каталога», 2 сценария. Проценты обозначают долю исследований, не успешность участников; используются демонстрационные данные таблицы.
В StudyFilters поиск занимает доступную ширину слева, ProductField Type=Select справа имеет ширину 240 px. Оба контрола 40 px и выровнены по верхней/нижней границам; подписи находятся над ними.
''')
append('ds/screens/task-picker.md','<!-- task-card-applied-2026-09-23 -->','''
## Карточки выбора

Три TaskChoiceCard instances вместо текста с символами ●/○. Первая карточка Selected=True; оливковый фон, контур, настоящий Radio и «Выбрано». Title/Description сохраняются как свойства. Модальное окно пересчитано по содержимому и центрировано (720×544).
''')
for name in ['replay','replay-incomplete','finding-editor','finding-saved']:
    append('ds/screens/'+name+'.md','<!-- replay-action-2026-09-23 -->','''
Play/Pause в ReplayControls — оливковый accent/strong #626E32 с text/inverse; отличается от графитовых действий демонстрационного магазина. Форма внутри плеера — пример тестируемого интерфейса. Поля с подписью используют HUG; проверка 40 ProductField на финальных экранах не обнаружила выхода содержимого по высоте.
''')
append('directives/directive_final_screens.md','<!-- labeled-field-check-2026-09-23 -->','''
### Поля с подписью и карточки выбора

ProductField вместе с Label нельзя принудительно сжимать до высоты внутреннего Control (40 px). Использовать HUG и проверять максимум child.y+child.height относительно высоты instance. Проверка добавлена в audit_final_pack.py.
Поиск и статус в общей панели предпочтительно собирать из ProductField Search/Select с одинаковой высотой Control и подписями сверху. Не выравнивать кнопку фильтра по верхнему краю подписи поиска.
В выборе заданий использовать TaskChoiceCard из UI Kit, а не ●/○ в тексте. Для исправлений: fix_replay_form_and_action.py, refine_studies_summary.py, build_task_choice_card.py, apply_task_choice_card.py.
''')
# Keep regeneration aligned with the verified playback colour and field sizing.
p='execution/restyle_replay_controls.py'
write(p,read(p).replace("primary?'action/primary':'background/surface'","primary?'accent/strong':'background/surface'").replace("theme(transportButton,'text/inverse','action/primary')","theme(transportButton,'text/inverse','accent/strong')"))
p='execution/build_final_pack.py'
write(p,read(p).replace("if(!label)n.findOne(x=>x.name==='Label').visible=false;return n;","if(!label)n.findOne(x=>x.name==='Label').visible=false;n.layoutSizingVertical='HUG';return n;"))
print(json.dumps({'components':status['componentCount'],'variants':status['variantCount'],'auditPassed':True}))
