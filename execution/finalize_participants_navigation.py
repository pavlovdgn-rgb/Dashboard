"""Record verified live Figma additions without overwriting source-library data."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DS=ROOT/'ds'
URL='https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def link(node):
    return URL+node.replace(':','-')

def append_block(path,marker,body):
    old=path.read_text(encoding='utf-8') if path.exists() else ''
    start='<!-- '+marker+' -->'
    end='<!-- /'+marker+' -->'
    block=start+'\n'+body+'\n'+end
    if start in old:
        before,rest=old.split(start,1)
        _,after=rest.split(end,1)
        old=before+block+after
    else:
        old=old.rstrip()+'\n\n'+block+'\n'
    path.write_text(old,encoding='utf-8')

analytics=read(ROOT/'.tmp/analytics-components/final-audit.json')
current=read(ROOT/'.tmp/participants-navigation/final-audit.json')
assert analytics['passed'] and current['passed'], 'Fix live audit before cataloguing'
new=[]
for source in (analytics,current):
    for item in source['report']:
        new.append({key:item[key] for key in ('name','id','variants','properties')}|{'type':'COMPONENT_SET','auditPassed':True})
index=read(DS/'index.json')
ext=index['productExtensions']
by_name={c['name']:c for c in ext['components']}
by_name.update({c['name']:c for c in new})
ext['components']=list(by_name.values())
ext['variantCount']=sum(len(c['variants']) for c in ext['components'])
ext['componentCount']=len(ext['components'])
ext['analyticsReport']='ds/analytics-components.md'
ext['participantsNavigationReport']='ds/participants-navigation.md'
write(DS/'index.json',index)
status=read(DS/'grow-ui-kit-status.json')
status.update(componentCount=ext['componentCount'],variantCount=ext['variantCount'],createdComponents=ext['components'])
status['participantsNavigation']={'status':'complete','report':'ds/participants-navigation.md','auditPassed':True}
write(DS/'grow-ui-kit-status.json',status)
write(DS/'participants-navigation-audit.json',current)
write(DS/'analytics-components-audit.json',analytics)

rows='\n'.join(f"| [{c['name']}]({link(c['id'])}) | {len(c['variants'])} | "+'; '.join(v['name'] for v in c['variants'])+' |' for c in current['report'])
report=f'''# Участники и боковая навигация

Компоненты созданы и проверены в Dashboard. Это макеты Figma; клики, фильтры, сортировка и загрузка данных не являются реализованным приложением. Исходная Elastic UI не изменялась.

| Компонент | Вариантов | Состояния |
| --- | ---: | --- |
{rows}

## Таблица участников

[Готовый пример]({link('153:702')}). Поиск по ID, фильтры исхода и полноты данных, четыре демонстрационные строки, пагинация. Одна строка описывает выбранную попытку участника. При выборе другой попытки приложение должно одновременно менять исход, время, сигналы, полноту и целевую запись. Эти взаимодействия описаны, но не подключены к данным.

Исход задания и полнота данных — независимые вложенные компоненты. Полные данные не гарантируют достижения цели, неполные не означают неуспех. У недоступной записи показано пояснение вместо кнопки открытия. Фильтр по меткам, настройка колонок и отдельная выгрузка не добавлены. Сортировку необходимо подключить на экране; ложного признака уже отсортированных данных в примере нет.

«Выбрать попытку» использует ProductButton/Secondary, иконку layers слева и arrowDown справа; обе иконки — instances Elastic UI. Меню списка попыток и прототип взаимодействия не входят в текущую отрисовку.

## NavMenu

[Пример с активными участниками]({link('153:2369')}). Размер 320×1080. Active переключает 10 разделов. Projects показывает рабочее пространство; Studies добавляет проект; разделы исследования показывают всю структуру. Заголовки проекта и исследования редактируются через свойства. Пункты собраны из ProductNavItem и библиотечных иконок. Наведение и фокус доступны в свойствах вложенного ProductNavItem. Нижний блок прижат вниз через растягиваемый Auto Layout; готовность исследования — демонстрационный статус, не реальное состояние сервера. Номер версии приложения не выдуман и не добавлен.

## Последние визуальные решения

- ScenarioRow: серые фоны счётчиков сохранены при Selected=False; при Selected=True число графитовое без фона.
- ProductButton/Secondary: фон background/sidebar, Hover — border/subtle, Pressed — accent/soft. Белый фон и контур убраны; рамка Focus сохранена. Tertiary в спокойном состоянии прозрачен.
- Ширина внутреннего контрола ProductButton растягивается вместе с instance, иконки не обрезаются.
- Новых цветов нет: используются утверждённые Variables. Источники, размеры, шрифты и палитра сохранены.

## Проверка и воспроизведение

Геометрия видимых дочерних элементов, привязки цветов и текстовые стили проверены у всех 27 новых вариантов. Ошибок нет. Визуально проверены все пять состояний таблицы, меню участников и кнопка выбора попытки. Состояния макета не являются интерактивным прототипом.

Исполнение: build_participants_navigation.py (стадии outcome, coverage, action, row, table, nav; после каждой — combine), затем polish_participants_navigation.py и add_attempt_button_icons.py. Последние два скрипта используют ID из текущего файла; перед применением к заново созданной библиотеке ID нужно обновить по квитанциям. Для визуальных правок сценариев — refine_secondary_buttons.py. Проверка — audit_participants_navigation.py.

Учтённое ограничение MCP: импортированный, но не вставленный source-компонент может не находиться по временному ID в следующем вызове. Search field импортируется по стабильному key в том же вызове, где создаётся instance.
'''
(DS/'participants-navigation.md').write_text(report,encoding='utf-8')
arows='\n'.join(f"| [{c['name']}]({link(c['id'])}) | {len(c['variants'])} |" for c in analytics['report'])
(DS/'analytics-components.md').write_text('# Аналитические компоненты\n\n| Компонент | Вариантов |\n| --- | ---: |\n'+arows+'\n\nВсе пять наборов прошли проверку геометрии, цветов, текстовых стилей и отношений ширины полос к долям 14/18, 12/17, 10/15. Числа демонстрационные. Режимы ширины в коллекции Demo data относятся к данным примера, а не к палитре. Семантика единицы первого клика требует отдельного продуктового определения. Последние правила счётчиков и кнопок — в participants-navigation.md.\n',encoding='utf-8')
append_block(DS/'components.md','analytics-and-navigation','## Аналитика, участники и навигация\n\n'+'\n'.join(f"- [{c['name']}]({link(c['id'])}): {len(c['variants'])} вариантов." for c in new)+f"\n\nВсего локальных наборов: {ext['componentCount']}; вариантов: {ext['variantCount']}. Исходный каталог: 204 элемента, без изменений. Отчёты: [аналитика](analytics-components.md), [участники и навигация](participants-navigation.md).")
append_block(DS/'patterns.md','participants-navigation','## Участник → попытка → запись\n\nParticipantsTable → ParticipantRow → независимые TaskOutcome, RecordingCoverage, AttemptAction. Смена попытки обновляет все значения строки. NavMenu объединяет ProductNavItem и библиотечные иконки; Active задаёт выбранный маршрут. [Описание](participants-navigation.md).')
append_block(DS/'product-palette.md','secondary-neutral-update','## Secondary-кнопки: уточнение\n\nОбычный фон — background/sidebar (#F3F3EE); Hover — border/subtle (#E4E5DC); Pressed — accent/soft (#ECEEDC). Текст — text/primary. Tertiary прозрачен в спокойном состоянии. Плашка счётчика неполных данных присутствует только в невыбранной строке. Новые цвета не добавлены.')
print(json.dumps({'components':ext['componentCount'],'variants':ext['variantCount'],'auditPassed':True}))
