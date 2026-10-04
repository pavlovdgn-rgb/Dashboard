"""Prepare five low-fi screen payloads and finish the authorized text package."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/wireframes'

def t(value,w,size=16,medium=False,name='Label'):
    return dict(kind='text',name=name,text=value,w=w,size=size,medium=medium)
def box(name,w,children=(),h=None,direction='VERTICAL',gap=16,pad=0,fill=False,border=False):
    return dict(kind='box',name=name,w=w,h=h,children=list(children),direction=direction,gap=gap,pad=pad,fill=fill,border=border)
def row(name,w,children,h=None,gap=16,pad=0,border=False):
    return box(name,w,children,h,'HORIZONTAL',gap,pad,border=border)
def button(label,w=190):return box('Action',w,[t(label,w-24,16,True)],48,pad=12,border=True)
def field(label,value,w):return box('Field',w,[t(label,w,13),box('Input',w,[t(value,w-24)],40,pad=10,border=True)],gap=6)
def contextual_sidebar(screen):
    active={'ResultsOverview':'Обзор результатов','Heatmaps':'Тепловая карта','Funnel':'Воронка','Replay':'Участники','SuccessCriteria':'Настройка исследования','Projects':'Все проекты','Studies':'Исследования проекта','StudySetup':'Настройка исследования','Launch':'Проверка и запуск'}[screen]
    def item(label, enabled=True):
        result=box('NavigationItem' if enabled else 'NavigationItemDisabled',192,[t(('• ' if label==active else '')+label,192,16,label==active)],48,gap=0)
        result['opacity']=1 if enabled else 0.45
        return result
    children=[t('РАБОЧЕЕ ПРОСТРАНСТВО',192,11,True),item('Все проекты')]
    has_project=screen!='Projects'
    has_study=screen not in ('Projects','Studies')
    study=('Навигация каталога' if screen in ('StudySetup','Launch') else 'Покупка в интернет-магазине') if has_study else 'Не выбрано'
    children += [box('ProjectContext',192,[t('ПРОЕКТ',192,11,True),t('Интернет-магазин' if has_project else 'Не выбран',192,16,True)],64,gap=8),item('Исследования проекта',has_project)]
    children += [box('StudyContext',192,[t('ИССЛЕДОВАНИЕ',192,11,True),t(study,192,16,True)],80,gap=8)]
    children += [item(n,has_study) for n in ['Настройка исследования','Проверка и запуск','Обзор результатов','Тепловая карта','Воронка','Участники','Сигналы затруднений','Отчёт PDF']]
    if not has_study:
        children.append(t('Выберите проект и исследование для доступа к разделам.' if not has_project else 'Выберите исследование для доступа к разделам.',192,14,name='NavigationHint'))
    return box('Sidebar',240,children,1016,gap=12,pad=24)
def heading(title,sub,action=None):
    children=[box('HeadingText',1210,[t(title,1210,30,True),t(sub,1210,15)],gap=8)]
    if action:children.append(button(action,382))
    return row('PageHeading',1616,children,76,gap=24)
def stats(items):
    return row('Summary',1616,[box('Metric',528,[t(label,480,15),t(number,480,28,True),t(note,480,14)],112,pad=12,gap=6) for label,number,note in items],112)
def table(name,width,widths,headers,rows):
    children=[row('TableHeader',width,[t(v,w-16,14,True) for v,w in zip(headers,widths)],48,gap=16)]
    for i,values in enumerate(rows):
        children.append(row('TableRow'+str(i+1),width,[t(v,w-16,16) for v,w in zip(values,widths)],88,gap=16,border=True))
    return box(name,width,children,gap=0)

def product(w,h,checkout=False):
    if checkout:
        return box('PrototypePlaceholder',w,[t('Магазин / Оформление заказа',w-48,19,True),row('CheckoutContent',w-48,[box('FormPreview',(w-72)*.58,[t('Контактные данные',500,23,True),field('Имя','Анна — демонстрационный ввод',500),field('Email','anna@example.test',500),field('Адрес','Тестовая улица, дом 10',500),button('Отправить заказ',250)],gap=16),box('OrderPreview',(w-72)*.42,[t('Ваш заказ',330,23,True),t('Городской рюкзак · 1 шт.',330),t('4 900 ₽',330,28,True),t('Доставка: пункт выдачи',330)],gap=24)],gap=24)],h,pad=24,gap=24,border=True)
    return box('PrototypePlaceholder',w,[t('Магазин / Рюкзаки / Городской рюкзак',w-48,18,True),row('ProductPreview',w-48,[box('ProductImage',320,[t('Изображение товара',260,18)],300,pad=30,fill=True),box('ProductDetails',w-392,[t('Городской рюкзак',w-392,26,True),t('4 900 ₽',w-392,28,True),t('Лёгкий рюкзак для города и поездок',w-392),field('Размер','M',220),button('Добавить в корзину',280),t('Слой тепловой карты — плейсхолдер',w-392,14)],gap=18)],gap=24)],h,pad=24,gap=24,border=True)

def screens():
    overview=[heading('Обзор результатов','Сценарии исследования и результаты участников','Экспорт в PDF'),row('ContextBar',1616,[t('Устройство: все устройства',480),t('Режим: задания',480),t('Демонстрационные данные',480)],48),stats([('Сценариев','3','В исследовании'),('Участников','20','Уникальных в текущей выборке'),('С неполными данными','2 из 20','Посмотреть участников')]),box('Scenarios',1616,[t('Сценарии · 3',1616,22,True),table('ScenariosTable',1616,[480,150,210,330,210,236],['Сценарий','Начали','Завершили попытку','Достигли цели','Неполные данные','Действие'],[['Найти товар и добавить в корзину\nВыбранный сценарий','20','16','14 / 18 · 78%\nОценены 18 из 20','2','Выбран'],['Изменить количество товара','18','15','12 / 17 · 71%\nОценены 17 из 18','1','Выбрать сценарий'],['Оформить заказ','16','12','10 / 15 · 67%\nОценены 15 из 16','1','Выбрать сценарий']])],gap=12),box('ScenarioAnalysis',1616,[t('Выбран сценарий: Найти товар и добавить в корзину',1616,20,True),row('AnalysisActions',1616,[button('Тепловая карта',250),button('Воронка',200),button('Участники и записи',280),button('Сигналы затруднений',290),button('Снять выбор',180)],gap=16)],gap=16)]
    heat=[heading('Тепловая карта кликов','К обзору результатов · Найти товар и добавить в корзину'),box('HeatmapContext',1616,[row('ContextRow',1616,[t('Сценарий: Найти товар и добавить в корзину',760),t('Страница: Карточка товара · /products/backpack',840)],48),row('StateRow',1616,[t('Состояние: Карточка товара',460),t('Устройство: компьютер',350),t('Окно: 1440×900',310),t('Снимок: версия 1',448)],48)],gap=8),row('DataSummary',1616,[t('98 кликов · 18 участников',460,18,True),t('1 попытка без кликов · 1 неполная',590),t('Как считается',200)],48),row('AnalysisWorkspace',1616,[box('MapPanel',1240,[row('MapToolbar',1240,[button('Все клики',200),button('Первый клик',200),t('Масштаб: вписать',270),t('Скрыть слой кликов',322)],48),product(1240,500),t('Меньше кликов — больше кликов   ·   Текущее состояние и выборка',1240,15)],628,gap=16),box('SelectionPanel',352,[t('Выбранная область',320,22,True),t('Кнопка «Добавить в корзину»',320,19),t('18 из 98 кликов',320,26,True),t('9 из 18 участников карты',320,18),button('Открыть 9 участников',320),t('Неполнота данных отмечена у участников. Выбор области не означает достижение цели.',320,15),button('Снять выбор',320),t('Все участники этой карты',320,16,True)],628,gap=24)],628,gap=24)]
    funnel=[heading('Воронка прохождения','К обзору результатов · Оформить заказ','Критерий успеха'),row('ContextBar',1616,[t('Сценарий: Оформить заказ',640),t('Устройство: все устройства',550),t('Критерий: версия 1',394)],48),stats([('Начали сценарий','16','Участников'),('Достигли цели','10 из 15 · 67%','Оценены 15 из 16'),('Недостаточно данных','1 из 16','Посмотреть участника')]),box('GoalDefinition',1616,[t('Критерий: последовательность действий',1616,18,True),t('Открыл оформление → заполнил данные → отправил заказ     ·     Правила расчёта',1616)],64,gap=8),row('AnalysisWorkspace',1616,[box('FunnelPanel',1168,[t('Шаги сценария',1168,22,True),table('FunnelTable',1168,[400,160,200,216,192],['Шаг','Дошли','От начала','От предыдущего','Действие'],[['1. Открыл оформление','15','15 / 15 · 100%','Не применимо','Выбрать'],['2. Заполнил данные\nВыбранный шаг','12','12 / 15 · 80%','12 / 15 · 80%','Выбран'],['3. Отправил заказ','10','10 / 15 · 67%','10 / 12 · 83%','Выбрать']]),t('База расчёта: 15 оценимых попыток.\nЕщё 1 участник с неизвестным исходом учитывается отдельно.',1168,15)],480,gap=16),box('StepDetails',424,[t('Шаг 2. Заполнил данные',424,22,True),t('Дошли до шага: 12',424,22),t('Перешли дальше: 10 из 12 · 83%',424),t('Не достигли следующего шага:\n2 из 12 · 17%',424,18,True),button('Все 12 участников шага',400),button('2 участника без следующего шага',400),t('Наблюдение завершено. Причину остановки проверяем по записи.',424,15)],480,gap=20)],480,gap=24)]
    replay=[heading('Запись сессии · Участник 014','К участникам · Оформить заказ · Выбранная попытка'),row('ReplayContext',1616,[t('Компьютер · 1440×900',390),t('Длительность: 04:32',330),t('Исход: цель не достигнута',500),t('Данные: полные',348)],56),row('ReplayWorkspace',1616,[box('Player',1184,[product(1184,490,True),box('Timeline',1184,[t('00:00             00:48              01:36               02:24               03:12               04:32',1184,14),box('TimelineTrack',1184,[],12,fill=True),t('Позиция: 02:18   ·   Повторные клики у кнопки «Отправить заказ»',1184,15)],80,gap=12),row('PlayerControls',1184,[button('Воспроизвести',220),t('02:18 / 04:32',230),button('Скорость: 1×',200),button('Вписать',180)],56,gap=24),t('Содержимое полей — демонстрационные данные. Камера и голос не записываются.',1184,14)],690,gap=16),box('EventsPanel',408,[t('События и затруднения',408,22,True),t('Все события / Сигналы',408,16,True),t('02:18   Повторные клики\n«Отправить заказ»',408,18,True),t('02:06   Ввод email\nanna@example.test',408),t('01:52   Клик без результата\nОбласть «Доставка»',408),t('01:36   Возврат\nНазад к контактным данным',408),t('00:48   Длительная пауза\nПроверьте контекст записи',408),t('Нажмите событие, чтобы перейти к его времени.',408,15),t('Сигнал не доказывает проблему.\nПравила определения — в методике исследования.',408,15)],690,gap=26)],690,gap=24)]
    criteria=[heading('Критерий успеха','Настройка исследования · Оформить заказ'),box('TaskContext',1616,[t('Задание участнику',1616,14),t('Оформите заказ на выбранный товар с доставкой в пункт выдачи.',1616,20)],76,gap=8),row('GoalType',1616,[button('Целевая страница',290),button('Целевая кнопка',290),button('Последовательность · выбрана',420)],56),row('CriteriaWorkspace',1616,[box('StepsEditor',1040,[t('Шаги в заданном порядке',1040,23,True),box('StepOne',1040,[t('1. Открыл оформление',1000,18,True),row('StepFields',1040,[field('Тип условия','Страница',280),field('URL / путь','/checkout',720)])],126,gap=12),box('StepTwo',1040,[t('2. Заполнил данные',1000,18,True),row('StepFields',1040,[field('Тип условия','Событие интерфейса',280),field('Привязка события','checkout_details_completed',720)])],126,gap=12),box('StepThree',1040,[t('3. Отправил заказ',1000,18,True),row('StepFields',1040,[field('Тип условия','Нажатие кнопки',280),field('Элемент','[data-testid="place-order"]',720)])],126,gap=12),button('Добавить шаг',230)],520,gap=14),box('RuleSummary',552,[t('Условие выполнения',552,23,True),t('Успех, когда участник выполнил все три шага в указанном порядке.',552,20),t('Открыл оформление\n↓\nЗаполнил данные\n↓\nОтправил заказ',552,20),t('Текст задания и критерий успеха задаются отдельно.',552),t('Привязка к событиям / элементам показана как проектное предложение. Способ настройки уточняется в D01.',552,15),t('Повторы и альтернативные пути:\nправило должно быть определено до запуска.',552,15)],520,gap=24)],520,gap=24),row('SaveBar',1616,[button('Сохранить критерий',270),button('К контрольному прохождению',360),t('Есть несохранённые изменения',700)],56,gap=24)]
    return [('ResultsOverview','Обзор',overview,24),('Heatmaps','Тепловая карта',heat,16),('Funnel','Воронка',funnel,24),('Replay','Участники',replay,24),('SuccessCriteria','Настройка исследования',criteria,24)]

RENDER=r'''
const p=await figma.getNodeByIdAsync('20:2');await figma.setCurrentPageAsync(p);
const section=await figma.getNodeByIdAsync('20:3');
if(section.children.some(n=>n.name===DATA.name))throw new Error('Screen already exists; inspect before retry');
await figma.loadFontAsync({family:'Inter',style:'Regular'});await figma.loadFontAsync({family:'Inter',style:'Medium'});
const ids=[];const track=n=>{ids.push(n.id);return n;};
const ink={r:26/255,g:26/255,b:26/255},gray={r:229/255,g:229/255,b:229/255};
function txt(parent,value,w,size=16,medium=false,name='Label'){
 const n=track(figma.createText());parent.appendChild(n);n.name=name;n.fontName={family:'Inter',style:medium?'Medium':'Regular'};n.fontSize=size;n.characters=value;n.fills=[{type:'SOLID',color:ink}];n.resize(w,1);n.textAutoResize='HEIGHT';return n;
}
function make(parent,d){
 if(d.kind==='text')return txt(parent,d.text,d.w,d.size,d.medium,d.name);
 const n=track(figma.createAutoLayout(d.direction));parent.appendChild(n);n.name=d.name;n.resize(d.w,d.h||1);
 n.primaryAxisSizingMode=d.direction==='VERTICAL'&&!d.h?'AUTO':'FIXED';n.counterAxisSizingMode=d.direction==='HORIZONTAL'&&!d.h?'AUTO':'FIXED';
 n.paddingLeft=n.paddingRight=n.paddingTop=n.paddingBottom=d.pad;n.itemSpacing=d.gap;n.cornerRadius=0;n.opacity=d.opacity===undefined?1:d.opacity;
 n.fills=d.fill?[{type:'SOLID',color:gray}]:[];if(d.border){n.strokes=[{type:'SOLID',color:ink}];n.strokeWeight=1;}
 if(d.direction==='HORIZONTAL')n.counterAxisAlignItems='CENTER';
 for(const child of d.children)make(n,child);return n;
}
const title=txt(section,DATA.name,1920,24,true,'ScreenTitle');title.x=80+DATA.index*2000;title.y=30;
const f=track(figma.createAutoLayout('VERTICAL'));section.appendChild(f);f.name=DATA.name;f.resize(1920,1080);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';f.itemSpacing=0;f.fills=[{type:'SOLID',color:{r:1,g:1,b:1}}];f.x=80+DATA.index*2000;f.y=90;f.clipsContent=true;
make(f,DATA.header);
const workspace=make(f,DATA.workspace);
const main=workspace.children.find(n=>n.name==='Main');
const issues=[];for(const n of f.findAllWithCriteria({types:['FRAME']})){
 const visible=n.children.filter(c=>c.visible);for(const c of visible)if(c.x+c.width>n.width+1||c.y+c.height>n.height+1)issues.push({parent:n.name,child:c.name,id:c.id,bottom:c.y+c.height,height:n.height,right:c.x+c.width,width:n.width});
}
return {createdNodeIds:ids,frameId:f.id,name:f.name,width:f.width,height:f.height,overflow:issues};
'''

def prepare_docs():
    folder=ROOT/'ia/wireframes'
    docs={
    'Replay':'''# Replay

**Размер:** desktop 1920×1080 px.
**Назначение:** воспроизведение действий, переходов и введённых данных.
**Статус:** включено в отрисовку по общей команде пользователя «на все апрув не спрашивай рисуй варфреймы»; отдельного просмотра этой структуры пользователем не было.

## Секции сверху вниз

- Header 64 px и Sidebar 240 px — общая оболочка согласованных экранов; активен раздел участников.
- Main 1680 px с отступами 32 px. Заголовок «Запись сессии · Участник 014», возврат к исходной выборке. Указываются сценарий и конкретная попытка.
- ReplayContext 56 px: устройство, размер окна, длительность, исход попытки и полнота данных. Эти показатели не приравниваются друг к другу.
- ReplayWorkspace: Player 1184 px + промежуток 24 px + EventsPanel 408 px, высота 690 px.
- Player: изображение восстановленного интерфейса 490 px, временная шкала 80 px, управление 56 px. Пауза/воспроизведение, позиция, скорость, вписать. Камера и голос не нужны; тип хранения и реализация replay пока не выбраны.
- EventsPanel: события и четыре типа сигналов — повторные клики, клики без результата, возвраты, паузы. Нажатие события перемещает к времени. Сигналы не являются автоматическими выводами о причинах.
- Введённые значения видны в интерфейсе без маскирования по брифу; в макете только искусственные данные anna@example.test и тестовый адрес.
- Возврат сохраняет исследование, сценарий, исходный шаг/область карты и фильтры. Автопоиск проблемного момента и пропуск неактивности не добавляются.

## Состояния

Loading — сообщение загрузки без подстановки чужой записи. ReplayUnavailable/LoadError — причина и повтор либо возврат к участнику. IncompleteData — обозначенный интервал разрыва на шкале и в событиях, без фиктивного непрерывного воспроизведения. Нет событий — пустая панель; нет сигналов не означает отсутствие проблем. Участник с незавершённой попыткой не объявляется автоматически неуспешным.

## Placeholder-контент

Участник 014, сценарий «Оформить заказ», 04:32, позиция 02:18. В плеере форма заказа; справа события со временем. Все числа, события и значения искусственные, служат компоновке, не являются результатами исследования.

## Открытые решения

F12–F17, F23–F24; определения сигналов D04, совместимость записи D05/D09, правила попыток D03 и хранения D07. Размер данных и срок хранения не утверждены.
''',
    'SuccessCriteria':'''# SuccessCriteria

**Размер:** desktop 1920×1080 px.
**Назначение:** успех по URL, кнопке или последовательности.
**Статус:** включено в отрисовку по общей команде пользователя «на все апрув не спрашивай рисуй варфреймы»; отдельного просмотра этой структуры пользователем не было.

## Секции сверху вниз

- Общие Header 64 px, Sidebar 240 px, Main 1680 px с отступами 32 px. Активна настройка исследования.
- PageHeading 76 px: «Критерий успеха», текущий сценарий.
- TaskContext 76 px: сохранённый текст задания для сверки, отдельно от машинного условия успеха.
- GoalType 56 px: целевая страница, целевая кнопка, последовательность. В основном wireframe выбрана последовательность; для одного URL/кнопки показывается одно условие вместо списка шагов.
- CriteriaWorkspace 520 px: StepsEditor 1040 px, промежуток 24 px, RuleSummary 552 px. Слева название каждого шага, тип условия, поле привязки к URL/элементу/событию, действие добавить шаг. Справа читаемая формулировка успеха и порядок шагов.
- Предложенный способ привязки через URL, идентификатор события или селектор показан для проработки формы, не закрывает D01 и не требует конкретного SDK. AI-интерпретация задания не подразумевается.
- SaveBar 56 px: сохранить критерий, перейти к контрольному прохождению, явный статус сохранения. Действие перехода ведёт в Launch; ошибки обязательных полей исправляются до проверки.

## Состояния

ValidationError — сообщение у конкретного пустого/некорректного условия. SaveStatus — несохранено, сохраняется, сохранено после подтверждения, ошибка с повтором. Loading/LoadError — загрузка существующего критерия и повтор, без потери введённых значений. Для свободного изучения без цели настройка не обязательна. Изменения активного исследования не применяются молча к старым данным: версия и правила D03 остаются открыты.

## Placeholder-контент

Сценарий «Оформить заказ». 1: страница /checkout; 2: условное событие checkout_details_completed; 3: кнопка [data-testid="place-order"]. Это примеры привязок, не реальные интеграции. Успех — выполнение всей допустимой последовательности; повторы и альтернативные пути определяются отдельно.

## Открытые решения

F05, F25; D01 — способ выбора/привязки цели, D03 — попытки и версии, D09 — подключение. Сохранённый критерий не равен подтверждённой готовности теста.
'''}
    for name,content in docs.items():
        p=folder/f'{name}.md'
        if p.exists() and p.read_text(encoding='utf-8')!=content:raise FileExistsError(p)
        p.write_text(content,encoding='utf-8',newline='\n')
    p=folder/'Funnel.md';text=p.read_text(encoding='utf-8').replace('**Статус:** структура предложена для согласования, фаза 1.3. Ещё не отрисовано в Figma.','**Статус:** пользователь дал общий апрув и поручил отрисовку всех экранов без дальнейших согласований.').replace('Согласовать Funnel. После апрува — структура Replay. До согласования всего текстового пакета Figma MCP не вызывается.','Переход к отрисовке всех пяти экранов разрешён прямой командой пользователя; отдельные апрувы больше не запрашиваются.');p.write_text(text,encoding='utf-8',newline='\n')
    p=folder/'README.md';text=p.read_text(encoding='utf-8');text=text[:text.index('Фаза 1.3:')]+'''Фаза 1.3: все пять текстовых структур подготовлены. Пользователь дал общий апрув и прямо отменил дальнейшие запросы согласования: «на все апрув не спрашивай рисуй варфреймы». Это разрешение продолжить работу; позднее подготовленные детали Replay/SuccessCriteria не выдаются за отдельно просмотренные пользователем.

Отрисовка выполняется в существующем Dashboard на отдельной странице «UX-Lab · Wireframes», секция «Wireframes — low-fi». Используется уже известный файл, чтобы исполнить команду без нового запроса ссылки. Ранее созданные схемы сохраняются.

Структуры: [ResultsOverview](ResultsOverview.md), [Heatmaps](Heatmaps.md), [Funnel](Funnel.md), [Replay](Replay.md), [SuccessCriteria](SuccessCriteria.md).

Discovery: Code Connect не найден; Cover не содержит instances; опубликованный UI-kit не применяется, поскольку текущая директива прямо требует low-fi, Inter Regular/Medium и три цвета. Это не вывод об отсутствии всех доступных библиотек. Все текущие изображения — локальные смысловые плейсхолдеры.
''';p.write_text(text,encoding='utf-8',newline='\n')

def main():
    if not (ROOT/'ia/wireframes/figma-delivery.md').exists():
        prepare_docs()
    OUT.mkdir(parents=True,exist_ok=True)
    for i,(name,active,children,gap) in enumerate(screens()):
        header=row('Header',1920,[t('UX-Lab',200,22,True),t('Все исследования',240),t('Покупка в интернет-магазине',960,18,True),t('Коллега',340)],64,gap=24,pad=24)
        nav=['Настройка исследования','Обзор','Тепловая карта','Воронка','Участники','Сигналы затруднений','Отчёт PDF']
        sidebar=box('Sidebar',240,[t('ИССЛЕДОВАНИЕ',192,12,True)]+[box('NavigationItem',192,[t(('• ' if n==active else '')+n,192,16,n==active)],52,gap=0) for n in nav],1016,gap=12,pad=24)
        sidebar=contextual_sidebar(name)
        header['children'][1]['text']='Все проекты'
        mainarea=box('Main',1680,children,1016,gap=gap,pad=32)
        workspace=row('Workspace',1920,[sidebar,mainarea],1016,gap=0)
        if name == 'Replay':
            player = children[2]['children'][0]
            player['children'][0]['h'] = 400
            form = player['children'][0]['children'][1]['children'][0]
            form['children'][3] = t('Адрес: Тестовая улица, дом 10', 500)
            player['children'][1]['h'] = 72
            player['children'][2]['h'] = 48
        if name == 'SuccessCriteria':
            children[3]['children'][1]['children'][4]['text'] = 'Контрольное прохождение покажет, фиксируются ли выбранные действия.'
        data=dict(name=name,index=i,header=header,workspace=workspace)
        (OUT/f'{i+1:02}.js').write_text('const DATA='+json.dumps(data,ensure_ascii=False)+';\n'+RENDER,encoding='utf-8')
    print('Five wireframe payloads prepared; remaining text structures and authorization recorded.')

if __name__=='__main__':main()
