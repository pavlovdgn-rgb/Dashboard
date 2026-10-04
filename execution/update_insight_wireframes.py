"""Incremental, reproducible wireframe updates from the approved reference analysis.

Existing frame IDs are retained. New states reuse the current workspace shell.
Python prepares specs/payloads; Figma MCP executes the generated Plugin API code.
"""
from pathlib import Path
import json
import sys
from grow_ui_kit import COMMON, BUILD_COMMON

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/insight-wireframes'
EXISTING={'ResultsOverview':'22:3','Signals':'49:263','Participants':'49:79','Report':'50:465','Replay':'24:93','Heatmaps':'22:95','HeatmapsFirstClick':'50:137','Funnel':'24:3'}
NEW={'SignalsByPage':'49:263','SignalsPageDetails':'49:263','Findings':'49:263','FindingsEmpty':'49:263','FindingDetails':'49:263','FindingEditor':'24:93','FindingSaved':'24:93','ParticipantsFromHeatmap':'49:79'}
PURPOSE={
'ParticipantsFromHeatmap':'Список участников выбранной области карты с сохранением сценария, страницы и устройства.',
'SignalsByPage':'Сводка затруднений по страницам и состояниям; участники, события и вход в карту/записи.',
'SignalsPageDetails':'Выбранная страница и конкретные сигналы; исходная выборка видна.',
'Findings':'Сохранённые наблюдения команды с доказательствами и ручным приоритетом.',
'FindingsEmpty':'Пустой список находок с понятным входом в просмотр сигналов.',
'FindingDetails':'Правая панель находки: наблюдение, интерпретация, доказательства, повторная проверка.',
'FindingEditor':'Правая панель сохранения наблюдения из записи; момент и контекст заполнены.',
'FindingSaved':'Возврат к записи с подтверждением сохранения и ссылкой на находку.',
'ResultsOverview':'Обзор первым экраном; свежесть данных, критерий и точка потери выбранного сценария.',
'Signals':'Существующие четыре типа событий плюс вход во вкладку находок и группировку по страницам.',
'Participants':'Фильтры исхода/сигнала и прямой вход в конкретную попытку, без смешения с участником.',
'Report':'Выбор находок и предпросмотр выводов с доказательствами в PDF.',
'HeatmapsFirstClick':'Список целей первого клика рядом с картой и сохранение наблюдения.',
'Replay':'Сохранение наблюдения в выбранный момент записи.',
'Heatmaps':'Сохранение наблюдения о выбранной области карты.',
'Funnel':'Сохранение наблюдения о выбранном шаге воронки.',
}

PREP=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('20:2'));
const createdNodeIds=[],mutatedNodeIds=[];let section=figma.currentPage.children.find(n=>n.name==='Analysis · Findings & Insights');
if(!section){section=figma.createSection();figma.currentPage.appendChild(section);section.name='Analysis · Findings & Insights';section.x=160;section.y=Math.max(...figma.currentPage.children.filter(n=>n.id!==section.id).map(n=>n.y+n.height))+240;section.resizeWithoutConstraints(8160,2780);createdNodeIds.push(section.id);}
const frames=[];let index=0;
for(const [name,sourceId]of Object.entries(NEW)){
 let f=section.children.find(n=>n.type==='FRAME'&&n.name===name);
 if(!f){const source=await figma.getNodeByIdAsync(sourceId);for(const t of source.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
 f=source.clone();section.appendChild(f);f.name=name;f.x=80+(index%4)*2000;f.y=100+Math.floor(index/4)*1340;createdNodeIds.push(f.id,...f.findAll().map(n=>n.id));
 const label=figma.createText();section.appendChild(label);await figma.loadFontAsync({family:'Inter',style:'Medium'});label.fontName={family:'Inter',style:'Medium'};label.fontSize=22;label.characters=name;label.name='ScreenTitle';label.x=f.x;label.y=f.y-42;createdNodeIds.push(label.id);
 }frames.push({name,id:f.id});index++;
}
return {createdNodeIds,mutatedNodeIds,sectionId:section.id,frames};
'''

HELPERS=COMMON+BUILD_COMMON[BUILD_COMMON.index('async function theme'):]+r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('20:2'));
const f=await figma.getNodeByIdAsync(TARGET);await fonts(f);
const main=f.findOne(n=>n.name==='Main');const changed=[f.id,main.id];
function fixed(n,w,h){n.resize(w,h);n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';}
function clear(n){for(const c of [...n.children])c.remove();changed.push(n.id);}
async function txt(p,value,style='body',name='Label'){return text(p,name,value,style);}
async function act(p,label,w=220,primary=false){const n=await button(p,label,primary);n.setBoundVariable('minWidth',dimensions.xl);n.resizeWithoutConstraints(w,40);n.primaryAxisSizingMode='FIXED';return n;}
async function actions(p,labels,w=1616){const row=frame('Actions',p,'HORIZONTAL',w);spacing(row,'md');row.counterAxisAlignItems='CENTER';for(const entry of labels)await act(row,entry[0],entry[1],entry[2]||false);return row;}
async function block(p,name,title,body,w=1616){const n=frame(name,p,'VERTICAL',w,'base');spacing(n,'md','base');n.strokes=[paint('border/subtle')];fill(n,'background/surface');await txt(n,title,'medium');if(body)await txt(n,body);return n;}
async function heading(title,sub){const n=main.findOne(n=>n.name==='PageHeading');const texts=n.findAllWithCriteria({types:['TEXT']});texts[0].characters=title;if(texts[1])texts[1].characters=sub;changed.push(...texts.map(t=>t.id));}
function fresh(){const h=main.children.find(n=>n.name==='PageHeading');for(const n of [...main.children])if(n.id!==h.id)n.remove();spacing(main,'base','xl');}
async function tabs(p,active,count=2){return actions(p,[['Сигналы',180,active==='signals'],['Находки · '+count,180,active==='findings']]);}
async function filters(p,labels){return actions(p,labels.map((s,i)=>[s,i===0?480:280]));}
async function table(p,name,widths,headers,rows){
 const n=frame(name,p,'VERTICAL',widths.reduce((a,b)=>a+b,0));n.itemSpacing=0;
 for(const [i,cells]of [headers,...rows].entries()){
  const row=frame(i===0?'TableHeader':'TableRow'+i,n,'HORIZONTAL',n.width);row.itemSpacing=0;row.counterAxisAlignItems='CENTER';row.strokes=[paint('border/subtle')];
  for(let j=0;j<cells.length;j++){const cell=frame('Cell'+j,row,'VERTICAL',widths[j],'md');await txt(cell,cells[j],i===0?'medium':'body');}
 }return n;
}
async function introSignals(active='signals',count=2){
 await heading('Сигналы затруднений','Покупка в интернет-магазине · Оформить заказ');
 await tabs(main,active,count);
 await filters(main,['Сценарий: оформить заказ','Устройство: все','Сбросить фильтры']);
}
const pageRows=[['Оформление / Контактные данные','4 из 15','2','3','2','1','Открыть'],['Оформление / Доставка','3 из 15','1','4','1','2','Открыть'],['Подтверждение заказа','1 из 10','0','1','0','0','Открыть']];
const pageHeaders=['Страница / состояние','Участники с сигналами','Повторы','Без результата','Возвраты','Паузы','Детали'];
const widths=[440,280,160,190,160,160,226];
async function findingList(empty=false){
 fresh();await introSignals('findings',empty?0:2);
 await txt(main,'Находки команды','medium');
 if(empty){await block(main,'EmptyState','Пока нет сохранённых находок','Посмотрите сигнал или запись и сохраните наблюдение с доказательством.');await actions(main,[['Открыть сигналы',240,true],['Выбрать запись',240]]);return;}
 await txt(main,'2 находки · приоритет выставлен командой, а не вычислен по кликам.','small');
 await table(main,'FindingsTable',[520,200,280,320,296],['Наблюдение','Участники','Приоритет команды','Проверка','Действие'],[
 ['Не замечают выбор доставки','3 из 15','Высокий','Проверено по записям','Открыть находку'],
 ['Возвращаются к контактным данным','4 из 15','Средний','Нужно проверить','Открыть находку']]);
 await actions(main,[['Включить находки в PDF',320,true],['Открыть сигналы',240]]);
 await txt(main,'Участники могут повторяться в разных находках. Числа строк не складываются. Все данные демонстрационные.','small');
}
async function drawer(title){
 const old=f.children.find(n=>n.name==='FindingOverlay');if(old)old.remove();
 const overlay=frame('FindingOverlay',f,'HORIZONTAL',1920);overlay.layoutPositioning='ABSOLUTE';overlay.x=0;overlay.y=0;fixed(overlay,1920,1080);overlay.itemSpacing=0;
 const scrim=frame('Scrim',overlay,'VERTICAL',1184);fixed(scrim,1184,1080);fill(scrim,'text/primary');scrim.opacity=.28;
 const panel=frame('FindingDrawer',overlay,'VERTICAL',736,'xl');fixed(panel,736,1080);spacing(panel,'md','xl');fill(panel,'background/surface');panel.clipsContent=true;
 const h=frame('DrawerHeading',panel,'HORIZONTAL',672);spacing(h,'md');await txt(h,title,'medium');await act(h,'Закрыть',100);
 return panel;
}
async function field(p,label,value,multiline=false){
 const wrap=frame('FormField',p,'VERTICAL',672);await txt(wrap,label,'small');
 const key=multiline?'ae1a78a262dd4a0229adadbb8105941ff2784915':'40608e701957c128bd761f39222d8576145711bf';
 const source=await figma.importComponentByKeyAsync(key);const n=source.createInstance();wrap.appendChild(n);created.push(n.id);await fonts(n);await theme(n,'text/primary','background/surface');
 const t=n.findAllWithCriteria({types:['TEXT']})[0];t.characters=value;n.resizeWithoutConstraints(672,multiline?80:40);return n;
}
'''

SCRIPTS={
'SignalsByPage':r'''
fresh();await introSignals();await actions(main,[['Отдельные события',280],['По страницам · выбрано',320,true]]);
await txt(main,'Где возникают затруднения','medium');await txt(main,'Сортировка: число участников с сигналами. База — участники, посетившие страницу в текущей выборке.','small');
await table(main,'PageSignalsTable',widths,pageHeaders,pageRows);
await block(main,'CountingNote','События и участники считаются отдельно','Один участник может дать несколько сигналов. Четыре столбца — число событий; люди между страницами и типами могут повторяться.');
''',
'SignalsPageDetails':r'''
fresh();await introSignals();await actions(main,[['К сводке страниц',260],['Открыть тепловую карту',300]]);
await block(main,'PageContext','Оформление / Доставка','3 из 15 посетивших участников с сигналами · 8 событий · Все устройства. Для карты выберите устройство и размер окна.');
await table(main,'PageEvents',[200,360,420,200,436],['Участник / попытка','Сигнал','Место','Время','Действие'],[['014 / 1','Клик без результата','Выбор доставки','01:52','Открыть запись в 01:52'],['009 / 1','Повторные клики','Пункт выдачи','01:16','Открыть запись в 01:16'],['012 / 1','Длительная пауза','Блок доставки','02:05','Открыть запись в 02:05']]);
await txt(main,'Показано 3 из 8 событий.  ‹ Назад     Далее ›','small');await actions(main,[['Все 3 участника',260],['Сохранить наблюдение',300,true]]);
await txt(main,'Сигналы требуют просмотра контекста; причина не определяется автоматически.','small');
''',
'Findings':"await findingList();",
'FindingsEmpty':"await findingList(true);",
'FindingDetails':r'''
await findingList();const p=await drawer('Находка · Не замечают выбор доставки');
await txt(p,'Оформить заказ · Оформление / Доставка','small');
await txt(p,'Высокий приоритет · оценка команды','medium');
await block(p,'Observation','Наблюдение','3 из 15 участников возвращались к блоку доставки и повторяли действия перед продолжением.',672);
await txt(p,'Предположение команды: вариант доставки недостаточно заметен. Требует проверки.');
await txt(p,'Доказательства · 3 участника','medium');
await actions(p,[['014 · попытка 1 · 01:52',310],['Открыть запись',230]],672);
await actions(p,[['009 · попытка 1 · 01:16',310],['Открыть запись',230]],672);
await actions(p,[['012 · попытка 1 · 02:05',310],['Открыть запись',230]],672);
await txt(p,'Снимок v1 · компьютер · блок «Доставка». Контекст каждого источника сохраняется.','small');
await block(p,'Retest','Как проверим изменение','Повторить задание после изменения; проверить, находят ли участники выбор доставки без повторных действий. Порог команда ещё не установила.',672);
await txt(p,'Данные на 22.09, 14:32 · подтверждено просмотром записей. Числа демонстрационные.','small');
await actions(p,[['Редактировать',220],['Включить в PDF',240,true]],672);
''',
'FindingEditor':r'''
const p=await drawer('Сохранить наблюдение');
await txt(p,'Из записи · Участник 014 · Попытка 1 · 02:18','small');
await txt(p,'Оформить заказ · Оформление · Компьютер · 1440×900','small');
await field(p,'Название *','Повторные клики по отправке заказа');
await field(p,'Что наблюдали *','Участник несколько раз нажал «Отправить заказ».\nПроверяем, что происходило после клика.',true);
await field(p,'Предположение причины · необязательно','Ответ интерфейса мог быть недостаточно заметен.',true);
await txt(p,'Доказательство прикреплено: запись 014 / попытка 1 / 02:18','medium');
await actions(p,[['Добавить доказательство',300],['Существующая находка',300]],672);
await actions(p,[['Приоритет: не задан',300],['Нужно проверить',250]],672);
await field(p,'Как проверим изменение · необязательно','Повторить сценарий и проверить реакцию на отправку заказа.',true);
await txt(p,'Сохраняется контекст источника. Сигнал сам по себе не подтверждает проблему.','small');
await actions(p,[['Отмена',170],['Сохранить находку',300,true]],672);
''',
'FindingSaved':r'''
const old=f.findOne(n=>n.name==='FindingSavedNotice');if(old)old.remove();
const toast=await block(f,'FindingSavedNotice','Находка сохранена','Запись 014 · попытка 1 · 02:18 прикреплена.',800);toast.layoutPositioning='ABSOLUTE';toast.x=1088;toast.y=896;
await actions(toast,[['Открыть находку',260],['Продолжить просмотр',300]],768);
''',
'Signals':r'''
const old=main.children.find(n=>n.name==='InsightTabs');if(old)old.remove();const tab=await tabs(main,'signals');tab.name='InsightTabs';main.insertChild(1,tab);
const old2=main.children.find(n=>n.name==='SignalGrouping');if(old2)old2.remove();const mode=await actions(main,[['Отдельные события · выбрано',380,true],['По страницам',240]]);mode.name='SignalGrouping';main.insertChild(4,mode);spacing(main,'base','xl');
''',
'Participants':r'''
fresh();await heading('Участники исследования','Оформить заказ · Выбрана конкретная попытка');
await filters(main,['Сценарий: оформить заказ','Устройство: все','Сбросить фильтры']);
await actions(main,[['Исход: любой',260],['Сигнал: любой',280],['Данные: любые',280]]);
await txt(main,'16 участников начали · показаны 4 · время относится к выбранной попытке, а не ко всем сессиям человека.','small');
await table(main,'ParticipantsTable',[140,160,300,180,200,220,416],['Участник','Попытка','Исход задания','Время','Сигналы','Данные','Действие'],[
 ['014','1','Цель не достигнута','04:32','4','Полные','Открыть запись попытки 1'],['018','1','Нет оценки','03:10','2','Неполные','Открыть запись попытки 1'],['009','1 из 2','Цель достигнута','02:48','3','Полные','Выбрать попытку'],['012','1','Цель достигнута','03:24','2','Полные','Открыть запись попытки 1']]);
await txt(main,'Участники 1–4 из 16    ‹ Назад     Далее ›','small');
await actions(main,[['Открыть детали участника',340],['Все участники исследования',380]]);
await txt(main,'При переходе из карты сохраняются область, страница, состояние и устройство. В этом примере открыт весь сценарий.','small');
''',
'ResultsOverview':r'''
spacing(main,'base','xl');const old=main.findOne(n=>n.name==='ScenarioAnalysis');clear(old);spacing(old,'md');
const texts=f.findAllWithCriteria({types:['TEXT']});const selected=texts.find(n=>n.characters.includes('Найти товар и добавить в корзину\nВыбранный'));if(selected)selected.characters='Найти товар и добавить в корзину';
const checkout=texts.find(n=>n.characters==='Оформить заказ');if(checkout)checkout.characters='Оформить заказ\nВыбранный сценарий';
const rows=main.findAll(n=>n.name==='TableRow1'||n.name==='TableRow3');for(const row of rows){const ts=row.findAllWithCriteria({types:['TEXT']});ts[ts.length-1].characters=row.name==='TableRow1'?'Выбрать сценарий':'Выбран';changed.push(ts[ts.length-1].id);}
await txt(old,'Выбран сценарий: Оформить заказ','medium');
await txt(old,'Цель: открыть оформление → заполнить данные → отправить заказ. Наибольшая потеря: 3 из 15 между шагами 1 и 2.','small');
await actions(old,[['Тепловая карта',240],['Воронка',180],['Участники и записи',280],['Сигналы / находки',280]]);
await txt(old,'Где посмотреть: Контактные данные — 4 из 15 участников с сигналами; Доставка — 3 из 15.','small');
const context=main.findOne(n=>n.name==='ContextBar');const ct=context.findAllWithCriteria({types:['TEXT']});ct[2].characters='Сбор идёт · обновлено 14:32';
await txt(old,'Последнее событие: 14:30 · Обновить результаты · Снять выбор. Демо-данные.','small');
''',
'Report':r'''
fresh();await heading('Отчёт PDF','Состав отчёта и выводы команды');
const row=frame('ReportWorkspace',main,'HORIZONTAL',1616);spacing(row,'lg');
const config=frame('ReportConfiguration',row,'VERTICAL',752,'base');spacing(config,'base','base');
await txt(config,'Область: все 3 сценария · все устройства','medium');
await txt(config,'☑ Сводные показатели\n☑ Результаты сценариев и воронки\n☑ Тепловые карты выбранных страниц\n☑ Сигналы и полнота данных\n☑ Находки и выводы команды');
await txt(config,'Включённые находки · 2','medium');
await txt(config,'☑ Не замечают выбор доставки\n☑ Возвращаются к контактным данным');
await actions(config,[['Выбрать находки',300]],720);
await txt(config,'У каждой находки: наблюдение, доказательства, интерпретация отдельно, предложенная повторная проверка.');
await txt(config,'Данные зафиксированы на 22.09, 14:32. Выборка и фильтры указаны в каждой секции.','small');
await act(config,'Сформировать PDF',320,true);
const preview=await block(row,'ReportPagePreview','Выводы команды','Покупка в интернет-магазине · Оформить заказ',840);
await txt(preview,'01 · Не замечают выбор доставки','medium');
await txt(preview,'Наблюдение: 3 из 15 участников повторяли действия в блоке доставки. Приоритет: высокий — оценка команды.');
await txt(preview,'Доказательства: 014 / 01:52, 009 / 01:16, 012 / 02:05. Попытка 1. Ссылки на записи доступны коллегам с доступом.');
await txt(preview,'Интерпретация: выбор доставки может быть недостаточно заметен. Это предположение, не автоматический диагноз.');
await txt(preview,'Повторная проверка: повторить задание после изменения и проверить выбор доставки.');
await txt(preview,'02 · Возвращаются к контактным данным','medium');
await txt(preview,'4 из 15 участников · требует проверки контекста. Ограничения: малая выборка, повторяющиеся участники между находками.');
await txt(preview,'Предпросмотр · страница 3 из 4 · демонстрационные данные','small');
''',
'HeatmapsFirstClick':r'''
const p=f.findOne(n=>n.name==='SelectionPanel');clear(p);spacing(p,'md');
await txt(p,'Цели первого клика','medium');await txt(p,'18 участников · 18 первых кликов','small');
await txt(p,'Добавить в корзину — 6\nИзображение товара — 5\nВыбор размера — 4\nДругие области — 3');
await actions(p,[['Выделить на карте',300]],p.width);
await txt(p,'Выбрано: Добавить в корзину','medium');await txt(p,'6 из 18 первых кликов\n6 из 18 участников карты');
await act(p,'Открыть 6 участников',300);await act(p,'Сохранить наблюдение',300,true);await act(p,'Снять выбор',220);
await txt(p,'Это распределение кликов. Правильность первого действия не определяется автоматически. Единица отсчёта — D02.','small');
''',
'Replay':r'''
const p=f.findOne(n=>n.name==='EventsPanel');spacing(p,'base');const old=p.findOne(n=>n.name==='SaveObservation');if(old)old.remove();
const b=await act(p,'Сохранить наблюдение · 02:18',390,true);b.name='SaveObservation';
''',
'Heatmaps':r'''
const p=f.findOne(n=>n.name==='SelectionPanel');spacing(p,'md');const old=p.findOne(n=>n.name==='SaveObservation');if(old)old.remove();const b=await act(p,'Сохранить наблюдение',300,true);b.name='SaveObservation';
''',
'Funnel':r'''
const p=f.findOne(n=>n.name==='StepDetails');spacing(p,'md');const old=p.findOne(n=>n.name==='SaveObservation');if(old)old.remove();const b=await act(p,'Сохранить наблюдение',330,true);b.name='SaveObservation';
''',
}

END=r'''
return {name:f.name,frameId:f.id,createdNodeIds:[...new Set(created)],mutatedNodeIds:[...new Set(changed)],mainBottom:Math.max(...main.children.map(n=>n.y+n.height)),height:main.height};
'''

SCRIPTS['ParticipantsFromHeatmap']=SCRIPTS['Participants'].replace(
    "'Оформить заказ · Выбрана конкретная попытка'", "'Из карты · Найти товар и добавить в корзину'").replace(
    "'Сценарий: оформить заказ','Устройство: все'", "'Сценарий: добавить в корзину','Устройство: компьютер'").replace(
    "'16 участников начали · показаны 4 · время относится к выбранной попытке, а не ко всем сессиям человека.'",
    "'9 участников выбранной области: Карточка товара / Добавить в корзину · компьютер · 1440×900 · снимок v1.'").replace(
    "['014','1','Цель не достигнута','04:32'", "['014','1','Цель достигнута','02:10'").replace(
    "Участники 1–4 из 16", "Участники 1–4 из 9").replace(
    "'При переходе из карты сохраняются область, страница, состояние и устройство. В этом примере открыт весь сценарий.'",
    "'Выборка из карты сохраняется при просмотре участника и записи. Вернуться к выбранной области карты.'")

def docs():
    folder=ROOT/'ia/wireframes'
    for name, purpose in PURPOSE.items():
        if name in NEW:
            body=f'# {name}\n\n**Статус:** подготовлен к отрисовке по команде пользователя от 22 сентября 2026.\n**Размер:** 1920×1080.\n**Назначение:** {purpose}\n\n'
            body+='Существующая оболочка рабочего пространства и 10 пунктов меню сохраняются. Находки — вкладка внутри сигналов. Демо-данные не являются результатами настоящего теста.\n\n'
            body+='Точное содержимое и секции: `execution/update_insight_wireframes.py`, SCRIPTS['+name+']. Источник решения: [анализ референса](../../reference_dashboard_analysis.md).\n'
            (folder/f'{name}.md').write_text(body,encoding='utf-8')
    note='''# Обновление wireframes по инсайтам — 22 сентября 2026

Пользователь поручил изменить макеты согласно анализу референса; повторный апрув не требуется. 8 существующих экранов обновляются на прежних ID, добавляются 7 состояний. Размеры 1920×1080, прежние 10 пунктов меню. Вход в результаты по-прежнему через обзор.

Новые сущности: сохранённая находка с наблюдением, отдельной интерпретацией, несколькими доказательствами и повторной проверкой; ручной приоритет. Источник: запись/время, карта/область либо шаг воронки. Участник, попытка, сценарий, устройство и версия страницы сохраняются. К одному доказательству можно вернуться; источники не копируются в новые события.

Сводка страниц использует число затронутых участников и число событий, без общего балла трения. Медиана времени до цели, автоматический вердикт гипотезы, AI-агент и раунды не добавляются. В первом клике добавляется распределение целей, не автоматическая оценка правильности.

Панель редактора: название и наблюдение обязательны, интерпретация/повторная проверка необязательны, доказательство прикреплено из контекста. Можно прикрепить к существующей находке. Сохранение возвращает к источнику с подтверждением. Ошибка сохраняет введённое и предлагает повтор; конфликт изменений коллеги не должен молча затирать данные. Детальный механизм совместного редактирования остаётся D08.

Фильтры сохраняются при переходах. Пустой список находок отрисовывается отдельно. Загрузка, ошибка и пустая фильтрация используют SharedPatterns. Неполные данные не становятся автоматически неуспехом. При удалённом/недоступном доказательстве сохраняются подпись контекста и предупреждение; восстановление самой записи не имитируется.

PDF включает выбранные находки, основания, контекст выборки, ограничения и время снимка. Ссылка на запись не открывает доступ внешнему получателю PDF. Генерация файла и интерактивные переходы не считаются реализованными от наличия макетов.

ДС: существующие low-fi оболочки сохранены; новые кнопки и поля — instances подключённой Elastic UI той же согласованной версии. Тексты и новые поверхности используют её стили и переменные продукта. Code Connect в проекте не найден; Button подтверждён существующим UI Kit, поля проверены в каталоге и исходных компонентах. Отдельный финальный UI всех экранов не создаётся.
'''
    (folder/'insight-update.md').write_text(note,encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    stage=sys.argv[1]
    if stage=='prepare':
        docs();code='const NEW='+json.dumps(NEW)+';\n'+PREP
    else:
        mapping=json.loads((OUT/('frames-current.json' if (OUT/'frames-current.json').exists() else 'frames.json')).read_text(encoding='utf-8'))
        ids={**EXISTING,**{f['name']:f['id'] for f in mapping['frames']}}
        code='const TARGET='+json.dumps(ids[stage])+';\n'+HELPERS+SCRIPTS[stage]+END
    (OUT/(stage+'.js')).write_text(code,encoding='utf-8')
    print(json.dumps({'code':code},ensure_ascii=False))

if __name__=='__main__':main()
