"""Record verified Figma edits without regenerating older final screens."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,data):(ROOT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def append(path,marker,body):
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    if marker not in text:p.write_text(text.rstrip()+'\n\n'+marker+'\n'+body.strip()+'\n',encoding='utf-8')

r=read('.tmp/review-batch-receipts.json')
a=read('.tmp/review-batch-final-audit.json')
assert a['passed'] and a['screenCount']==55
reg=r['checkbox']
entry={'name':'ProductCheckbox','id':reg['setId'],'type':'COMPONENT_SET','properties':reg['properties'],'variants':reg['variants'],'source':'Elastic Checkbox 203:4618; original source marked Deprecated; existing selected generation retained','usage':['screens/report'],'documentation':'ProductCheckbox: Off / On / Mixed × Default / Hover / Focus / Disabled; editable Label. Olive selected square and white glyph; visible neutral outline when unchecked.'}
index=read('ds/index.json')
items=index['productExtensions']['components']
items[:]=[i for i in items if i['name']!='ProductCheckbox']+[entry]
write('ds/index.json',index)
status=read('ds/grow-ui-kit-status.json')
status['createdComponents'][:]=[i for i in status['createdComponents'] if i['name']!='ProductCheckbox']+[entry]
status['componentCount']=len(status['createdComponents'])
status['variantCount']=sum(len(c.get('variants',[])) for c in status['createdComponents'])
write('ds/grow-ui-kit-status.json',status)
write('ds/screens/final-pack-audit.json',a)
write('ds/screens/storefront-hierarchy-audit.json',{'date':r['date'],'scope':'Current review batch: external storefront, analytics hierarchy, copying and checkboxes','component':reg,'checkboxApplication':r['checkboxApplied']['applied'],'tabs':r['tabs'],'resets':r['resets'],'storefront':r['storefront'],'mobile':r['mobile'],'close':r['close'],'asset':'assets/demo-storefront/city-backpack.png','imageHash':'d6ed599147ffc6640ab8795c34a162ca83aa4093','imageNodes':['205:6766','210:11828','210:14541','210:14934','210:17116'],'codeBlocks':['278:10658','278:11039'],'participantLink':'278:11433','metric':'210:7689','audit':{'passed':True,'screenCount':55,'checks':['visible widths','text styles','bound fill and stroke colours','form height']},'visualReview':['209:6256','205:6763','210:14931','210:17090','210:17611','210:18056','210:7689','210:10706','210:11409','280:2821','210:16160'],'prototypeWired':False})
palette=read('ds/demo-storefront-palette.json')
palette.update({'scope':'Nine external storefront views on Final Screens; deliberately separate from product UI','tokens':r['storefront']['tokens'],'styles':r['storefront']['styles'],'rootIds':[x['id'] for x in r['storefront']['roots']]+[x['id'] for x in r['mobile']['roots']],'photo':'assets/demo-storefront/city-backpack.png','imageHash':'d6ed599147ffc6640ab8795c34a162ca83aa4093'})
write('ds/demo-storefront-palette.json',palette)

marker='<!-- storefront-hierarchy-review-2026-09-23 -->'
append('ds/source.md',marker,'''
## Единый внешний магазин и иерархия управления

UI Kit: **22 набора / 168 вариантов**. ProductCheckbox `282:2918`: 12 состояний, 7 экземпляров в настройках PDF. ProductTab `128:1055`: прозрачный фон; выбранная вкладка — оливковый текст и подчёркивание 2 px.

NOVA — ad-hoc оформление внешнего тестируемого сайта по прямому указанию пользователя. Во всех 9 встраиваниях на Final Screens: Manrope, отдельные лавандовые поверхности, фиолетовые действия, поля и карточки. 5 фото товара вместо заглушек. Крестик модального окна — отдельная круглая кнопка NOVA. Оболочка UX-сервиса и цветная тепловая карта сохраняют собственный стиль.

Сброс фильтров — текстовое действие на 8 экранах. Сигналы / Находки — ProductTab на 4 экранах. Кнопки повторной загрузки, проверки подключения, включения находок в PDF и формирования PDF получили основной приоритет. Карточка достижения цели отделяет число, основание и процент.

Код подключения и ссылка для участников показаны рядом с копированием. Фрагмент SDK использует демонстрационный домен `.test`, подписан как пример; это не рабочий интеграционный код. Кликабельный прототип не подключался.

[Проверка и реестр изменений](screens/storefront-hierarchy-audit.json), [палитра магазина](demo-storefront-palette.json), [фото и промпт](../assets/demo-storefront/README.md).
''')
append('ds/components.md',marker,'''
## Checkbox и прозрачные вкладки

[ProductCheckbox](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=282-2918): Value=Off/On/Mixed × State=Default/Hover/Focus/Disabled. 12 вариантов, свойство Label. Связанная структура Elastic сохранена; отдельный текстовый слой Label добавлен на уровень локального компонента для редактируемого свойства. Включённый квадрат accent/strong с белой галочкой; выключенный — surface с border/control 1.5 px. Hover усиливает контур, Focus имеет внешний контур, Disabled — opacity 0.4. Строка 32 px, интервал 8 px; радиус и типографика используют существующие Variables / Text Styles.

ProductTab: прозрачная подложка во всех 8 вариантах, muted у неактивной вкладки, accent/strong и нижний индикатор 2 px у выбранной. Экземпляры группы Сигналы / Находки имеют ширину 180 px для соблюдения внутренней геометрии.

На Final Screens применены 7 ProductCheckbox в Report и 8 ProductTab в аналитической навигации. Семантика в реализации: checkbox + associated label, Space переключает; tablist/tab для вкладок. Состояния Figma статические.
''')
append('ds/patterns.md',marker,'''
## Копирование, фильтры и внешний прототип

- CodeCopyBlock: native Auto Layout + связанный Elastic Code Block `276:10375` + ProductButton. Заголовок и кнопка копирования находятся в одной строке; сам фрагмент моноширинный, на нейтральной поверхности. Для демонстрации явно обозначен пример кода.
- ParticipantLinkCopy: моноширинная ссылка и кнопка рядом в общем контейнере. Ссылка может переноситься, кнопка сохраняет размер.
- Фильтры одинакового назначения используют одинаковый secondary/dropdown стиль; сброс — Tertiary с оливковым текстом. Навигационные вкладки не подменяются кнопками действий.
- NOVA storefront: девять внешних представлений используют `demo/storefront/*` и `Demo storefront/*` Text Styles. Нативный круглый крестик относится к магазину. Фирменные аналитические контролы и тепловой слой не перекрашиваются.
''')
for f in ['ds/CONTRACT.md','ds/source.md','ds/screens/_index.md']:
    p=ROOT/f;t=p.read_text(encoding='utf-8');t=t.replace('20 локальных наборов / 148 вариантов','22 локальных набора / 168 вариантов').replace('UI-кит продукта: 20 наборов / 148 вариантов','UI-кит продукта: 22 набора / 168 вариантов');p.write_text(t,encoding='utf-8')
notes={
 'report':'7 экземпляров ProductCheckbox из набора 282:2918; выбор разделов и находок виден по оливковому квадрату и белой галочке. «Сформировать PDF» — Primary.',
 'connection-error':'CodeCopyBlock с демонстрационным фрагментом и кнопкой рядом. «Повторить проверку» — Primary.',
 'study-setup':'Код подключения виден в моноширинном CodeCopyBlock; кнопка копирования рядом. Фрагмент демонстрационный; «Проверить» — Primary.',
 'launch-active':'Ссылка и кнопка копирования объединены в ParticipantLinkCopy; длинный URL переносится.',
 'findings':'Прозрачные ProductTab Сигналы / Находки, активна вкладка Находки. Сброс — текстовое действие. «Включить находки в PDF» — Primary; дублирующий переход к сигналам убран.',
 'finding-details':'ProductTab с активными Находками, текстовый сброс, главное действие включения в PDF.',
 'signals-by-page':'Прозрачные ProductTab; активны Сигналы. Сброс отделён от фильтров как текстовое действие.',
 'signals-page-details':'Прозрачные ProductTab. «К сводке страниц» — текстовый переход со стрелкой; «Открыть тепловую карту» — Secondary; сброс текстовый.',
 'replay-unavailable':'«Повторить загрузку» — Primary, «Вернуться к участнику» — Secondary.',
}
for slug,note in notes.items():
    p=ROOT/'ds/screens'/f'{slug}.md'
    if p.exists():append(str(p.relative_to(ROOT)),marker,note)
for slug in ['replay','replay-incomplete','finding-editor','finding-saved','heatmaps','heatmaps-first-click','heatmaps-dynamic-state','participant-session','participant-session-mobile']:
    p=ROOT/'ds/screens'/f'{slug}.md'
    if p.exists():append(str(p.relative_to(ROOT)),marker,'Внешний магазин оформлен в едином стиле NOVA: Manrope, независимая лавандово-фиолетовая палитра, собственные поверхности и контролы. В товарных представлениях используется фото city-backpack.png. Стиль UX-сервиса сохраняется.')
registry=read('ds/screens/final-pack.json')
for screen in registry['screens']:
    if screen['name']=='Report' and '282:2918' not in screen['componentSets']:screen['componentSets'].append('282:2918')
    if screen['name'] in ['SignalsByPage','SignalsPageDetails','Findings','FindingDetails'] and '128:1055' not in screen['componentSets']:screen['componentSets'].append('128:1055')
write('ds/screens/final-pack.json',registry)
print(json.dumps({'components':status['componentCount'],'variants':status['variantCount'],'auditedScreens':55,'demoViews':len(palette['rootIds'])}))
