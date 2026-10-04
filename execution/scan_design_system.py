"""Prepare bounded read-only Figma payloads; index captured DS metadata locally.

Run prepare, execute payloads via use_figma, save each JSON response to .tmp/ds-scan,
then run build. Never recurse into component variants, instances or nested groups.
"""
from pathlib import Path
import json
import argparse
import shutil
import re
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'.tmp/ds-scan'
DEST=ROOT/'ds'
KEY='SNBSKtwsO81j3BdjRGFpAw'
PAGE='23678:450'
URL=f'https://www.figma.com/design/{KEY}/Elastic-UI--Copy-?node-id=23678-450'
PRE="const p=await figma.getNodeByIdAsync('23678:450');await figma.setCurrentPageAsync(p);\n"
FLAT="""const catalog=[];for(const n of p.children){if(['COMPONENT','COMPONENT_SET'].includes(n.type))catalog.push({n,section:null});else if(['FRAME','SECTION'].includes(n.type)){for(const c of n.children)if(['COMPONENT','COMPONENT_SET'].includes(c.type))catalog.push({n:c,section:{id:n.id,name:n.name}});}}\n"""

def prepare():
    TMP.mkdir(parents=True,exist_ok=True)
    DEST.mkdir(exist_ok=True)
    source=Path('C:/Users/InfDesign/Downloads/directive_ds_scan.md')
    target=ROOT/'directives/directive_ds_scan.md'
    if not target.exists():shutil.copyfile(source,target)
    for offset in range(0,204,20):
        code=PRE+FLAT+f"return {{offset:{offset},total:catalog.length,items:catalog.slice({offset},{offset+20}).map(({{n,section}})=>({{id:n.id,key:n.key,name:n.name,type:n.type,section,description:n.description,properties:n.type==='COMPONENT_SET'?n.componentPropertyDefinitions:null}}))}};"
        (TMP/f'components-{offset:03}.js').write_text(code,encoding='utf-8')
    for offset,size in [(0,45),(45,30),(75,15),(90,45),(135,30),(165,30),(195,30),(225,30),(255,18)]:
        code=PRE+f"const vs=await figma.variables.getLocalVariablesAsync();return {{offset:{offset},total:vs.length,items:vs.slice({offset},{offset+size}).map(v=>({{id:v.id,key:v.key,name:v.name,type:v.resolvedType,collectionId:v.variableCollectionId,values:v.valuesByMode,description:v.description,scopes:v.scopes}}))}};"
        (TMP/f'variables-{offset:03}.js').write_text(code,encoding='utf-8')
    code=PRE+"const cs=await figma.variables.getLocalVariableCollectionsAsync();const ts=await figma.getLocalTextStylesAsync();return {collections:cs.map(c=>({id:c.id,name:c.name,defaultModeId:c.defaultModeId,modes:c.modes,count:c.variableIds.length})),textStyleCount:ts.length,fonts:[...new Set(ts.map(t=>t.fontName.family+' / '+t.fontName.style)))]};".replace(')))]','))]')
    (TMP/'foundation-meta.js').write_text(code,encoding='utf-8')
    code=PRE+"const ts=await figma.getLocalTextStylesAsync();return {items:ts.map(t=>({id:t.id,key:t.key,name:t.name,font:t.fontName,size:t.fontSize,lineHeight:t.lineHeight,letterSpacing:t.letterSpacing,boundVariables:t.boundVariables}))};"
    (TMP/'text-styles.js').write_text(code,encoding='utf-8')
    print(json.dumps({'prepared':22,'directory':str(TMP)},ensure_ascii=False))

def capture(kind):
    items={};offsets=[]
    for f in sorted(TMP.glob(kind+'-*.json')):
        data=json.loads(f.read_text(encoding='utf-8'));offsets.append([data['offset'],len(data['items'])])
        for item in data['items']:
            if item['id'] in items:assert items[item['id']]==item,'Conflicting snapshots'
            items[item['id']]=item
    return list(items.values()),offsets

def verification():
    """Compare captured metadata against a fresh bounded read; never traverse nodes."""
    def normalize(v):
        if isinstance(v,bool) or v is None:return v
        if isinstance(v,(float,int)):return int(v*1000000+0.5) if v>=0 else int(v*1000000-0.5)
        if isinstance(v,dict):return {k:normalize(x) for k,x in v.items()}
        if isinstance(v,list):return [normalize(x) for x in v]
        return v
    def hash_value(v):
        raw=json.dumps(normalize(v),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-16-le')
        h=2166136261
        for i in range(0,len(raw),2):h=((h^(raw[i]+raw[i+1]*256))*16777619)&0xffffffff
        return h
    comps,_=capture('components');variables,_=capture('variables')
    expected={'components':{c['id']:hash_value(c) for c in comps},'variables':{v['id']:hash_value(v) for v in variables}}
    js=r'''
function norm(v){if(typeof v==='number')return v<0?-Math.round(-v*1e6):Math.round(v*1e6);if(Array.isArray(v))return v.map(norm);if(v&&typeof v==='object')return Object.fromEntries(Object.keys(v).sort().map(k=>[k,norm(v[k])]));return v;}
function hash(v){const s=JSON.stringify(norm(v));let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619)>>>0;return h;}
const cc=catalog.map(({n,section})=>({id:n.id,key:n.key,name:n.name,type:n.type,section,description:n.description,properties:n.type==='COMPONENT_SET'?n.componentPropertyDefinitions:null}));
const vs=await figma.variables.getLocalVariablesAsync();const vv=vs.map(v=>({id:v.id,key:v.key,name:v.name,type:v.resolvedType,collectionId:v.variableCollectionId,values:v.valuesByMode,description:v.description,scopes:v.scopes}));
const changedComponents=cc.filter(x=>hash(x)!==EXPECTED.components[x.id]).map(x=>x.id);const changedVariables=vv.filter(x=>hash(x)!==EXPECTED.variables[x.id]).map(x=>x.id);
const ids=new Set(vs.map(v=>v.id));const missing=[...new Set(vs.flatMap(v=>Object.values(v.valuesByMode).filter(x=>x&&x.type==='VARIABLE_ALIAS').map(x=>x.id)))].filter(id=>!ids.has(id));
const targets=[];for(const id of missing){try{const v=await figma.variables.getVariableByIdAsync(id);targets.push(v?{id,name:v.name,type:v.resolvedType,remote:v.remote}:{id,unavailable:true});}catch(e){targets.push({id,unavailable:true});}}
return {componentCount:cc.length,variableCount:vv.length,changedComponents,changedVariables,expectedComponentCount:Object.keys(EXPECTED.components).length,expectedVariableCount:Object.keys(EXPECTED.variables).length,aliasTargets:targets};
'''
    (TMP/'verify.js').write_text(PRE+FLAT+'const EXPECTED='+json.dumps(expected,separators=(',',':'))+';\n'+js,encoding='utf-8')
    print('Prepared verify.js')

def cell(value):return str(value).replace('<','&lt;').replace('>','&gt;').replace('|','\\|').replace('\n',' / ')

def purpose(c):
    n=c['name'].lower()
    for term,desc in [('timeline','Элемент временной шкалы'),('toast','Краткое всплывающее уведомление'),('tooltip','Контекстная подсказка'),('tabs','Группа вкладок'),('text - heading','Текст заголовка'),('text - paragraph','Текст абзаца'),('text - <small>','Мелкий вспомогательный текст'),('text - link','Текстовая ссылка'),('text - blockquote','Блок цитаты'),('text - keyboard','Обозначение клавиши'),('text in a sentence','Пример текста со встроенным элементом'),('heading with a paragraph','Заголовок с абзацем')]:
        if term in n:return desc
    rules=[('auto refresh','Управление автоматическим обновлением'),('refresh interval','Выбор интервала обновления'),('avatar','Аватар или группа аватаров'),('notification badge','Индикатор числа уведомлений'),('badge','Метка статуса'),('breadcrumb','Навигационная цепочка'),('accordion','Раскрывающийся блок'),('data grid','Таблица данных или её структурная часть'),('table','Таблица или её структурная часть'),('date picker','Выбор даты, времени или диапазона'),('color palette','Выбор или отображение цветовой палитры'),('color picker','Выбор цвета'),('form','Форма или её структурный элемент'),('checkbox','Флажок выбора'),('radio','Переключатель взаимоисключающих значений'),('selectable','Список с выбором элементов'),('select field','Поле выбора значения'),('combobox','Комбинированное поле выбора'),('textarea','Многострочный ввод'),('field','Поле ввода'),('file picker','Выбор файла'),('slider','Ползунок или его часть'),('range','Ввод диапазона'),('switch','Переключатель состояния'),('search','Поиск'),('filter','Фильтрация'),('button','Кнопка действия или её часть'),('callout','Выделенное сообщение'),('empty prompt','Пустое состояние'),('progress','Индикатор прогресса'),('spinner','Индикатор загрузки'),('modal','Модальное окно'),('flyout','Выдвижная панель'),('popover','Всплывающая панель'),('panel','Панель-контейнер'),('card','Карточка-контейнер'),('pagination','Постраничная навигация'),('side nav','Боковая навигация'),('collapsible nav','Сворачиваемая навигация'),('header','Заголовочная область'),('page','Макет страницы или его часть'),('tree','Элемент древовидного списка'),('steps','Последовательность шагов'),('step','Шаг последовательности'),('tour','Обучающий тур'),('list','Список или его элемент'),('comment','Комментарий или его часть'),('stat','Числовой показатель'),('expression','Подпись и значение выражения'),('facet','Фасетный фильтр'),('code','Отображение кода'),('markdown','Редактор Markdown'),('image','Изображение'),('horizontal rule','Разделитель'),('spacer','Отступ'),('health','Индикатор состояния'),('bottom bar','Нижняя панель'),('thumbnail','Миниатюра'),('number indicator','Числовая выноска')]
    for term,desc in rules:
        if term in n:return desc
    return 'Назначение не установлено: неоднозначное имя; требуется контекст автора'

TRANSLATIONS={
 '26861:286195':'Временная шкала с настраиваемой иконкой/аватаром; содержимое Children можно заменить другим компонентом. Для последнего элемента установить Top (no lines).',
 '13555:24644':'Краткое уведомление; дополнительные сведения открывать кнопкой в постоянной панели или на отдельной странице.',
 '23938:281323':'Преднастроенное поле только для чтения; открывает панель настройки интервала обновления.',
 '26768:281544':'В коде ещё не реализовано. В группе не более 10 аватаров, последний показывает число остальных; обводку согласовать с фоном. Нажатие управляет доступом или показывает полный список.',
 '26769:282323':'Пример списка пространств на Selectable; длинный список ограничивать по высоте и прокручивать.',
 '36238:395246':'Нижняя часть карточки остаётся внизу; при выравнивании высот переключать Hug contents на Fill container.',
 '15173:122940':'Встроенный в текст код поддерживает подсветку синтаксиса.',
 '15884:167851':'Выбор цвета с настройками строки формы; дополнительные параметры находятся у подписи и поля.',
 '15884:173636':'Выбор палитры с настройками формы и типа отображения; для текстового значения использовать Select field.',
 '20785:279182':'Содержимое группы обычно List Group, но допускается другой компонент.',
 '44991:80757':'При переносе заголовка выравнивать иконку по первой строке через Auto Layout.',
 '20788:280525':'Комментарий с настраиваемой иконкой временной шкалы; Slots в заголовке позволяют добавлять содержимое, например вкладки.',
 '15884:158445':'Парный ввод диапазона даты/времени с настройками строки формы.',
 '15884:160184':'Одиночный ввод даты/времени с настройками строки формы.',
 '15884:162483':'Ввод только времени с настройками строки формы.',
 '14787:3001':'Календарь Date Picker; содержит концепции переработки, допускает размещение в Popover или на странице.',
 '36674:394711':'Пустое состояние с минимальной шириной 805 px; дополнительные действия рядом с основным или под ним.',
 '14849:51':'Выражение требует значения и описания; может быть интерактивным или редактируемым.',
 '14850:110142':'Выражения в колонках; обязательны значение и описание. Источник предлагает пробелы для выравнивания — это рекомендация источника, не правило нашего проекта.',
 '13653:64632':'Фасетные фильтры со счётчиком; слой счётчика можно скрыть.',
 '135:602':'Горизонтальная группа фасетов: источник предлагает разбор компонента для изменения числа элементов, интервалы 20 px по горизонтали и 8 px по вертикали. Не применять автоматически в обход контракта.',
 '26803:282479':'Выбор файла с настройками строки формы; дополнительные параметры у подписи и поля.',
 '15884:200789':'Пример обычной формы с вариантом ошибки; обычная максимальная ширина 400 px, пример растягивается по контейнеру.',
 '15884:202224':'Пример компактной формы с вариантом ошибки для небольших контейнеров, например Popover.',
 '9871:3787':'Использовать эту навигационную цепочку только внутри Header.',
 '15079:109018':'Использовать только внутри Header.',
 '14711:1':'Заменяемое изображение с необязательной подписью; убрать тень, если нет открытия на весь экран.',
 '15132:132472':'Группа списка: граница и краевые отступы отключаемы; интервалы 0, 8 или 16.',
 '24329:291092':'Настраиваемая шапка страницы: возврат, навигационная цепочка, до 4 действий справа, дополнительный контент перед вкладками; для своей правой части вариант Time or Custom.',
 '24329:283356':'Параметры содержимого шапки находятся на следующем уровне вложенности; здесь не читались.',
 '24329:303983':'Компонент можно последовательно складывать в вертикальную структуру.',
 '24329:308827':'Шаблон страницы воспроизводит варианты боковой навигации EuiPageTemplate через pageSideBar.',
 '38872:21244':'Текстовый стиль Small / Paragraph.',
 '38872:21246':'Текстовый стиль Small / Paragraph.',
 '13648:4438':'Ширина прогресса задаётся невидимым текстовым слоем; цвета полосы и значения должны соответствовать друг другу.',
 '16011:195480':'Прогресс можно закреплять сверху контейнера или окна; источник рекомендует убирать серый фон и скругление при таком размещении.',
 '14757:86523':'Позиции бегунков меняются через текст компонентов Range.',
 '14757:83542':'Подсказка показывает текущее значение единственного бегунка; сместить при выходе за границы.',
 '15138:3267':'Сочетает поисковое поле и группу фильтров без дополнительных предположений.',
 '14645:214':'Ветви показывают вложенность; активный пункт должен быть раскрыт.',
 '14792:135915':'Концепция переработки: быстрый выбор и календарь объединены в одной панели.',
 '14795:111805':'Концепция переработки: выбор даты одной кнопкой и отдельное обновление.',
 '14652:151':'Вложенность регулируется левым отступом Auto Layout.'
}

def category(c):
    n=c['name'].lower()
    if purpose(c).startswith('Назначение не'):return 'Прочее'
    if any(t in n for t in ['field','form','picker','checkbox','radio','switch','range','slider','combobox','selectable','search','textarea','markdown']):return 'Ввод'
    if any(t in n for t in ['breadcrumb','nav','pagination','step','tour','tree','tabs']):return 'Навигация'
    if any(t in n for t in ['button','refresh','filter','facet']):return 'Действия'
    if any(t in n for t in ['callout','empty','progress','spinner','badge','health','toast','tooltip']):return 'Фидбэк'
    if any(t in n for t in ['modal','panel','popover','flyout','card','page','bar','header','accordion']):return 'Контейнеры'
    if any(t in n for t in ['data','table','stat','list','code','comment','expression','image','avatar']):return 'Данные'
    return 'Прочее'

def build():
    DEST.mkdir(exist_ok=True)
    comps,cbatches=capture('components');variables,vbatches=capture('variables')
    meta=json.loads((TMP/'foundation-meta.json').read_text(encoding='utf-8'))
    styles=json.loads((TMP/'text-styles.json').read_text(encoding='utf-8'))['items']
    sets=sum(c['type']=='COMPONENT_SET' for c in comps)
    missing_desc=[c for c in comps if not c['description']]
    deprecated=[c for c in comps if 'Deprecated' in c['description']]
    ambiguous=[c for c in comps if purpose(c).startswith('Назначение не')]
    duplicates={n:count for n,count in Counter(c['name'] for c in comps).items() if count>1}
    no_props=[c for c in comps if c['type']=='COMPONENT_SET' and not c['properties']]
    vars_by_id={v['id']:v for v in variables}
    verification_path=TMP/'verification.json'
    verification_data=json.loads(verification_path.read_text(encoding='utf-8')) if verification_path.exists() else {}
    external_targets={v['id']:v for v in verification_data.get('aliasTargets',[]) if v.get('remote')}
    aliases={value['id'] for v in variables for value in v['values'].values() if isinstance(value,dict) and value.get('type')=='VARIABLE_ALIAS'}
    unresolved=sorted(aliases-vars_by_id.keys()-external_targets.keys())
    duplicate_vars={name:count for name,count in Counter(v['collectionId']+' / '+v['name'] for v in variables).items() if count>1}
    complete=len(comps)==204 and len(variables)==273
    if complete:
        assert verification_data.get('componentCount')==204 and verification_data.get('variableCount')==273,'Verify complete snapshot before delivery'
        assert not verification_data['changedComponents'] and not verification_data['changedVariables'],'Snapshot changed during scan'
    status='полный' if complete else 'частичный: чтение остановлено лимитом Figma MCP Starter'
    report={'status':status,'complete':complete,'expectedComponents':204,'readComponents':len(comps),'expectedSets':157,'readSets':sets,'expectedSingles':47,'readSingles':len(comps)-sets,'expectedVariables':273,'readVariables':len(variables),'textStyles':len(styles),'noSourceDescription':len(missing_desc),'deprecatedComponents':len(deprecated),'ambiguousPurpose':len(ambiguous),'duplicateComponentNames':duplicates,'setsWithoutProperties':[c['id'] for c in no_props],'unresolvedAliasTargets':unresolved,'componentBatches':cbatches,'variableBatches':vbatches,'remainingPayloads':['components-180.js','variables-135.js','variables-165.js','variables-195.js','variables-225.js','variables-255.js'] if not complete else []}
    report.update(scope='Components: direct children + one FRAME/SECTION level; all local Variables; local Text Styles',externalAliasTargetCount=len(external_targets),externalAliasValuesResolved=False,snapshotVerified=bool(complete),cyrillicChecked=False)
    source=f'''# Источник дизайн-системы

Дата: 2026-09-21. Статус сканирования: **{status}**.

- Файл: [Elastic UI (Copy)]({URL}), key `{KEY}`.
- Проверенная страница: Components, Node ID `{PAGE}`; тип PAGE.
- Пользователь подтвердил: настройки, иконки, шрифты и цвета находятся в этом же файле.
- Название указывает на копию Elastic UI; происхождение из Community и право менять библиотеку отдельно не подтверждены. Сканирование только чтение.
- Локаль продукта: ru, по согласованному брифу.
- Пользователь планирует выбрать свои цвета. Палитра Elastic UI сохраняется как исходный снимок, не утверждённый фирменный стиль продукта.
- Скан: прямые дети Components и один уровень FRAME/SECTION. Внутрь COMPONENT/COMPONENT_SET/INSTANCE/GROUP и более глубоких контейнеров не заходили.
- Иконки на других страницах или глубже границы обхода не входят в этот каталог. Нахождение в том же файле не означает, что они проиндексированы.
- Обнаружены 204 элемента каталога (157 наборов и 47 одиночных компонентов), 273 Variables в 3 коллекциях. Сохранено {len(comps)} элементов и {len(variables)} Variables; отдельно 29 локальных текстовых стилей.
- Не прочитанный хвост не означает отсутствие компонентов/токенов. До завершения индекс нельзя считать полным UI-китом.

Продолжение: см. [scan-status.json](scan-status.json). После восстановления доступа дочитать недостающие порции, проверить изменения списка/порядка и пересобрать индекс. Figma и Dashboard не изменялись.
'''
    if complete:
        source=source.replace('- Не прочитанный хвост не означает отсутствие компонентов/токенов. До завершения индекс нельзя считать полным UI-китом.','- Сканирование завершено в указанной глубине. Это не полный обход всех страниц иконок или вложенных примеров. Метаданные всех 204 элементов и 273 локальных Variables повторно сверены с Figma: расхождений нет.')
        source=source.replace('Продолжение: см. [scan-status.json](scan-status.json). После восстановления доступа дочитать недостающие порции, проверить изменения списка/порядка и пересобрать индекс. Figma и Dashboard не изменялись.','Результат проверки: [scan-status.json](scan-status.json). Лимит MCP перестал блокировать чтение. Все недостающие порции дочитаны. Найдены 102 внешние цели alias с remote=true; их имена проверены без импорта и изменения библиотек. Внешние значения не разворачивались. Figma и Dashboard не изменялись.')
    (DEST/'source.md').write_text(source,encoding='utf-8')
    def value(v):
        if isinstance(v,dict) and v.get('type')=='VARIABLE_ALIAS':
            other=vars_by_id.get(v['id']) or external_targets.get(v['id']);return '→ '+(other['name'] if other else 'цель не прочитана')+(' [внешняя]' if other and other.get('remote') else '')+' (`'+v['id']+'`)'
        if isinstance(v,dict) and all(k in v for k in ['r','g','b']):return '#'+''.join(f'{round(v[k]*255):02X}' for k in ['r','g','b'])+(f"; α={v['a']:.3g}" if v.get('a',1)!=1 else '')
        return json.dumps(v,ensure_ascii=False)
    lines=['# Foundation (scan)','',f'**Источник:** [Elastic UI, Components]({URL}). **Дата:** 2026-09-21.',f'**Статус: {status}.** Значения получены для {len(variables)} из 273 переменных.','', '**Палитра продукта не выбрана.** Ниже точный индекс исходной библиотеки; цветовые значения не утверждают будущий бренд.','','## Фактическая организация','','В файле три коллекции: Color mode, Dimensions, Typographic scale. Отдельные Primitive/Semantic/Component коллекции не обнаружены. В прочитанной части есть прямые значения и alias внутри общей структуры; не выдаём её за трёхслойную архитектуру. Разделить уровни можно предложить на этапе адаптации, но сейчас ничего не перестраивается.','']
    for collection in meta['collections']:
        vs=[v for v in variables if v['collectionId']==collection['id']];modes=collection['modes']
        lines += [f"## {collection['name']}",'',f"Коллекция `{collection['id']}`. Прочитано {len(vs)} / {collection['count']}. Режим по умолчанию: {next(m['name'] for m in modes if m['modeId']==collection['defaultModeId'])}.",'','| Имя / Variable ID | Тип | '+' | '.join(m['name'] for m in modes)+' |','| --- | --- | '+' | '.join('---' for m in modes)+' |']
        for v in vs:lines += [f"| {cell(v['name'])}<br>`{v['id']}` | {v['type']} | "+' | '.join(cell(value(v['values'][m['modeId']])) if m['modeId'] in v['values'] else 'не прочитано' for m in modes)+' |']
        if not vs:lines += ['','Значения пока не получены; режимы известны из метаданных.']
        lines+=['']
    lines += ['## Типографика: локальные Text Styles','','Это стили, а не отдельные Variables. Значения прочитаны плоским API без обхода текстов в компонентах. Привязки сохранены в index.json; цель вне текущего снимка не означает сломанную ссылку.','','| Стиль | Шрифт | Размер / интерлиньяж | Style ID |','| --- | --- | --- | --- |']
    for s in styles:lines += [f"| {cell(s['name'])} | {s['font']['family']} / {s['font']['style']} | {s['size']} / {cell(s['lineHeight'])} | `{s['id']}` |"]
    lines += ['','## Замечания','','- Дубликаты имён Variables внутри одной коллекции: '+(cell(duplicate_vars) if duplicate_vars else 'не обнаружены в прочитанной части')+'.','- Привязки между смысловыми и базовыми токенами проверены только в полученной части. Полную цепочку не удалось восстановить.',f'- Целей alias вне снимка: {len(unresolved)}. Это пробел чтения, не доказательство ошибки ДС.','- Использование токенов в компонентах не проверено: для этого потребовался бы запрещённый директивой глубокий обход.','- Поддержка кириллицы конкретными версиями Inter и Roboto Mono в этом файле не проверена. Перед финальной типографикой проверить Щ/Ъ/Ь/Ы и русский текст; не подменять проверку названием семейства.',f"- Text Styles с меткой ☠️: {sum('☠' in s['name'] for s in styles)} из {len(styles)}. Статус требует проверки; метка сама по себе не заменяет описание автора.",'- Собственные цвета: следующий этап — согласовать палитру и семантическое соответствие, затем адаптировать токены. Не перекрашивать инстансы по одному. Цвета состояний и шкала тепловой карты требуют отдельного смыслового соответствия, не механической замены акцента.','']
    if complete:
        lines=[line.replace('Привязки между смысловыми и базовыми токенами проверены только в полученной части. Полную цепочку не удалось восстановить.',f'Alias локальных переменных сохранены; {len(external_targets)} целей находятся во внешних библиотеках (remote=true), имена проверены. Цепочки внешних значений не разворачивались.').replace(f'Целей alias вне снимка: {len(unresolved)}. Это пробел чтения, не доказательство ошибки ДС.',f'Неопознанных целей alias локальных Variables: {len(unresolved)}. Все локальные значения и режимы получены; внешние зависимости явно помечены.') for line in lines]
    (DEST/'foundation.md').write_text('\n'.join(lines),encoding='utf-8')
    lines=['# Components (scan)','',f'**Источник:** [Components]({URL}). **Дата:** 2026-09-21.',f'**Статус: {status}.** Прочитано {len(comps)}/204 элементов: {sets}/157 наборов, {len(comps)-sets}/47 одиночных.','', 'Названия и ключи вариантов сохранены как в Figma. Назначения на русском; выводы по имени явно помечены. Node ID и key относятся к файлу библиотеки, а не Dashboard. Для вставки в другой файл потребуется доступ к импорту; это сканирование его не проверяло.','']
    for group in ['Действия','Ввод','Контейнеры','Навигация','Фидбэк','Данные','Прочее']:
        lines += [f'## {group}','']
        for c in comps:
            if category(c)!=group:continue
            desc=TRANSLATIONS.get(c['id'])
            if 'Deprecated' in c['description']:desc=purpose(c)+' (роль по имени). Автор пометил устаревшим и рекомендует Elastic UI [Borealis].'
            elif desc is None:desc=purpose(c)+(' (вывод по имени; исходное описание пустое).' if not c['description'] else ' (роль по имени; исходное описание содержит только техническое название Eui-компонента).')
            props=c.get('properties') or {};variants=[key+': '+' | '.join(map(str,p.get('variantOptions',[]))) for key,p in props.items() if p['type']=='VARIANT']
            others=[key+' ('+p['type']+')' for key,p in props.items() if p['type']!='VARIANT']
            matrix='; '.join(variants) or ('одиночный компонент; дочерние слои не читались' if c['type']=='COMPONENT' else 'матрица VARIANT отсутствует в метаданных')
            lines += [f"### {cell(c['name'])}",'',f'- **Назначение:** {desc}',f'- **Варианты:** {matrix}'+(' · Другие свойства: '+', '.join(others) if others else ''),f"- **Node ID:** `{c['id']}` · [Figma](https://www.figma.com/design/{KEY}/Elastic-UI--Copy-?node-id={c['id'].replace(':','-')}) · {c['type']}"+(f" · Раздел: {c['section']['name']} ({c['section']['id']})" if c['section'] else ''),'']
    lines += ['## Self-check','',f'- **Жёлтый флаг:** пустое исходное description у {len(missing_desc)}/{len(comps)} ({len(missing_desc)/len(comps):.1%}). Назначения по имени не считаются описаниями автора.',f'- Неустановленное назначение: {len(ambiguous)}/{len(comps)}. Имена: '+', '.join(c['name'] for c in ambiguous)+'.',f'- Автор явно пометил Deprecated: {len(deprecated)} элементов, включая Button, Text field, Select field, Checkbox и Radio. Перед использованием нужно решение по версии библиотеки; переход на Borealis не выполнялся.','- Дубликаты имён: '+('; '.join(f'{n} × {count}' for n,count in duplicates.items()) or 'не найдены в прочитанной части')+'. Использовать Node ID, не первый результат поиска по имени.','- Наборы с пустым componentPropertyDefinitions: '+(', '.join(c['name']+' '+c['id'] for c in no_props) or 'не найдены в прочитанной части')+'.','- Комбинации вариантов внутри наборов не раскрывались. Перечень variantOptions не доказывает наличие каждой комбинации.','- Примеры с 💡 и внутренние части с точкой/📦/🧱 включены как найденные элементы; не считать их автоматически самостоятельными продуктовыми компонентами.','- 20 непрочитанных элементов, а также вложенные контейнеры/GROUP и отдельные страницы иконок вне текущего охвата.','', 'Компоненты без описания: '+', '.join(f"{c['name']} (`{c['id']}`)" for c in missing_desc)+'.','']
    if complete:lines=[line.replace('20 непрочитанных элементов, а также вложенные контейнеры/GROUP и отдельные страницы иконок вне текущего охвата.','Все 204 элемента в пределах глубины скана прочитаны. Вложенные контейнеры/GROUP и отдельные страницы иконок вне охвата директивы.') for line in lines]
    generic=[c for c in comps if re.match(r'^(Component\s*\d+|Frame\s*\d+|Untitled)',c['name'],re.I)]
    lines+=['','Подозрительные стандартные имена Component N / Frame N / Untitled: '+(', '.join(c['name'] for c in generic) if generic else 'не обнаружены среди компонентов каталога; названия группирующих фреймов в эту оценку не входят')+'.','']
    (DEST/'components.md').write_text('\n'.join(lines),encoding='utf-8')
    contract=f'''# DS Contract — правила проекта

Дата: 2026-09-21. Источник: [Elastic UI (Copy), Components]({URL}).
**Индекс частичный. Правила активны, сканирование не завершено.** Подробнее: source.md и scan-status.json.

## Перед работой с интерфейсом

1. Прочитать CONTRACT.md, foundation.md, components.md и scan-status.json.
2. Собирать интерфейс из проверенных компонентов каталога; выбирать по Node ID и матрице, вставлять инстансы. Не рисовать похожую замену с нуля и не отсоединять инстансы для удобства.
3. Цвета привязывать к смысловым Variables; отступы/радиусы/размеры — к соответствующим Variables. Типографику — к имеющимся Text Styles и их Variables. Если нужные данные не прочитаны, сначала дочитать конкретную часть, не считать её отсутствующей.
4. Связанные элементы компоновать через Auto Layout. Известные служебные/примерные и устаревшие компоненты не выбирать автоматически.

## Собственная палитра — решение пользователя

Пользователь планирует выбрать свои цвета. Текущие hex в foundation.md описывают Elastic UI и не утверждают палитру продукта. Новая палитра ещё не выбрана. После выбора меняются соответствующие токены в рабочей копии с сохранением смыслов и проверкой читаемости состояний; карта интенсивности кликов требует своей шкалы. Индекс обновить после изменения. Текущий scan ничего не перекрашивает.

## Границы индекса и готовности

- Прочитано {len(comps)}/204 элементов и {len(variables)}/273 Variables. Не найдено в индексе ≠ отсутствует в ДС.
- {len(deprecated)} элементов помечены автором Deprecated с указанием Borealis. Не выдавать их за актуальные компоненты. Перед сборкой затронутых экранов уточнить выбор версии; новую библиотеку не подменять самовольно.
- Способ импорта между файлами, права публикации и кириллица конкретных шрифтов не проверены.
- Старые low-fi wireframes сохраняются как структурный материал. Этот контракт не является командой автоматически перерисовать все 47 фреймов.

## Когда нужного компонента или токена нет

Сначала проверить недочитанную часть. Если отсутствие подтверждено — попробовать композицию существующих компонентов. Паттерн записать в ds/patterns.md с компонентами, Variables и примером. Происхождение копии и разрешение менять исходную библиотеку не установлены: текущий файл при сканировании не менять. После подтверждения собственной/дублированной ДС недостающий компонент создаётся в ДС и индексируется до использования. Для корпоративной ДС использовать локальные композиции и подготовить запрос её владельцам; не отправлять сообщения без поручения пользователя.

## Синхронизация

После изменений ДС пересканировать нужные части, проверить diff и обновить индекс. Не исправлять значения в Markdown так, будто они уже изменились в Figma. Для завершения текущего скана после восстановления MCP выполнить оставшиеся payloads из scan-status.json, сверив список и порядок элементов с сохранённым снимком. Не соединять разновременные данные при расхождении ID/значений.

## Исключения

Явные указания пользователя имеют приоритет. Разовый дизайн вне ДС обозначать как ad-hoc; это не меняет библиотеку проекта. Новые цвета уже предусмотрены этим контрактом и будут отдельным решением пользователя.
'''
    if complete:
        contract=contract.replace('**Индекс частичный. Правила активны, сканирование не завершено.**','**Сканирование завершено в пределах директивы. Правила активны.**')
        contract=contract.replace('Сначала проверить недочитанную часть.','Сначала проверить границы скана: более глубокие группы и отдельные страницы не входили в каталог.')
        contract=contract.replace('Для завершения текущего скана после восстановления MCP выполнить оставшиеся payloads из scan-status.json, сверив список и порядок элементов с сохранённым снимком.','Текущий снимок дочитан и проверен; remainingPayloads в scan-status.json пуст. При обновлении сверять не только число узлов, но и их ID, значения и метаданные.')
        contract=contract.replace('- Способ импорта между файлами, права публикации и кириллица конкретных шрифтов не проверены.',f'- {len(external_targets)} целей alias относятся к внешним библиотекам. Их имена подтверждены; значения и доступность при импорте в Dashboard не проверены.\n- Способ импорта между файлами, права публикации и кириллица конкретных шрифтов не проверены.')
    (DEST/'CONTRACT.md').write_text(contract,encoding='utf-8')
    (DEST/'scan-status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'index.json').write_text(json.dumps({'fileKey':KEY,'pageId':PAGE,'complete':complete,'collections':meta['collections'],'variables':variables,'components':comps,'textStyles':styles,'externalAliasTargets':list(external_targets.values())},ensure_ascii=False,indent=2),encoding='utf-8')
    marker='## Дизайн-система — ds_scan'
    pointer=marker+'\n\nДля задач с интерфейсом прочитай `ds/CONTRACT.md`, затем `ds/foundation.md`, `ds/components.md` и `ds/scan-status.json`. Индекс Elastic UI пока частичный из-за лимита MCP; не считай отсутствующие записи отсутствующими в ДС. Цвета продукта ещё выбираются и будут отличаться от исходной палитры. Правила контракта действуют с учётом этих ограничений и прямых указаний пользователя.\n'
    if complete:pointer=pointer.replace('Индекс Elastic UI пока частичный из-за лимита MCP; не считай отсутствующие записи отсутствующими в ДС.','Индекс Elastic UI завершён в пределах ds_scan: 204 элемента каталога, 273 локальные Variables и 29 Text Styles. Учитывай устаревшие компоненты, внешние зависимости и границы обхода; не считай этот каталог полным обходом всего файла.')
    for name in ['AGENTS.md','Codex.md']:
        path=ROOT/name;old=path.read_text(encoding='utf-8-sig')
        updated=re.sub(r'(?ms)^'+re.escape(marker)+r'\n.*?(?=^## |\Z)',lambda m:pointer+'\n',old) if marker in old else old.rstrip()+'\n\n'+pointer
        path.write_text(updated,encoding='utf-8')
    directive=ROOT/'directives/directive_ds_scan.md';old=directive.read_text(encoding='utf-8-sig')
    marker='## Применение в этом проекте Codex'
    if marker not in old:directive.write_text(old.rstrip()+'\n\n'+marker+'\n\n- Указатель на контракт добавляется в AGENTS.md и существующий Codex.md вместо создания второго CLAUDE.md.\n- Использовать асинхронные getLocalVariablesAsync/getLocalVariableCollectionsAsync.\n- Ответы use_figma ограничены по размеру: полный список 204 компонентов обрезался. Читать компоненты порциями по 20, Variables по 15–30 при длинных описаниях; валидировать JSON до сохранения.\n- При лимите MCP Starter сохранять частичный индекс, точный охват и недостающие порции. Не объявлять скан завершённым, не повторять платные/блокируемые вызовы без изменения условий.\n- Пользователь подтвердил, что ресурсы находятся в одном файле, и планирует выбрать свои цвета: индекс хранит исходную палитру, контракт не закрепляет её как окончательную.\n- В PowerShell запускать Python с -X utf8 при выводе имён с emoji.\n',encoding='utf-8')
    assert len({c['id'] for c in comps})==len(comps)
    assert len({v['id'] for v in variables})==len(variables)
    assert all('`'+c['id']+'`' in (DEST/'components.md').read_text(encoding='utf-8') for c in comps)
    assert all('`'+v['id']+'`' in (DEST/'foundation.md').read_text(encoding='utf-8') for v in variables)
    assert all((TMP/name).exists() for name in report['remainingPayloads'])
    print(json.dumps({k:report[k] for k in ['complete','readComponents','readVariables','textStyles','deprecatedComponents','noSourceDescription','remainingPayloads']},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build','verify']);args=parser.parse_args()
    {'prepare':prepare,'build':build,'verify':verification}[args.command]()
