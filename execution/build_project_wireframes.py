"""Extend the approved low-fi set with projects, setup and launch screens."""
from pathlib import Path
import json
import re
from build_wireframes import t, box, row, button, field, heading, stats, table, RENDER, contextual_sidebar

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.tmp/project-wireframes'
SECTION = '30:2'

def project_modal():
    return box('CreateProjectModal',640,[
        row('ModalHeader',576,[t('Новый проект',512,26,True),box('CloseButton',40,[t('×',24,24)],40,pad=8,gap=0)],40,gap=24),
        t('Объедините исследования одного продукта или интерфейса.',576,17),
        field('Название проекта *','Сервис доставки',576),
        field('Описание · необязательно','Проверяем выбор и оформление доставки',576),
        t('Проект будет доступен обоим коллегам команды.',576,15),
        row('CreateProjectActions',576,[button('Отмена',224),button('Создать проект',328)],48,gap=24),
    ],gap=20,pad=32,border=True)

MODAL_JS=r'''
const backdrop=track(figma.createRectangle());f.appendChild(backdrop);backdrop.name='ModalBackdrop';backdrop.layoutPositioning='ABSOLUTE';backdrop.resize(1920,1080);backdrop.x=0;backdrop.y=0;backdrop.fills=[{type:'SOLID',color:ink,opacity:0.40}];
const modal=make(f,DATA.modal);modal.layoutPositioning='ABSOLUTE';modal.fills=[{type:'SOLID',color:{r:1,g:1,b:1}}];modal.x=(f.width-modal.width)/2;modal.y=(f.height-modal.height)/2;
'''

def panel(name, width, children, height=None):
    if name in ('TaskOne', 'TaskTwo'):
        return box(name, width, children, 144, gap=8, pad=16, border=True)
    return box(name, width, children, height, gap=14 if name=='ConnectionPanel' else 18, pad=24, border=True)

def screens():
    projects = [
        heading('Все проекты', 'Рабочее пространство команды', 'Создать проект'),
        row('ListToolbar', 1616, [field('Найти проект', 'Название проекта', 600), t('3 проекта · доступ у обоих коллег', 760)], 72, gap=24),
        row('ProjectsWorkspace', 1616, [
            box('ProjectsList', 1016, [
                table('ProjectsTable', 1016, [440, 200, 200, 176], ['Проект', 'Исследований', 'Идёт сбор', 'Действие'], [
                    ['Интернет-магазин\nКаталог, корзина и оформление', '3', '1', 'Открыть'],
                    ['Личный кабинет\nПрофиль и настройки', '1', '0', 'Открыть'],
                    ['Мобильный каталог\nИнтерфейс для смартфонов', '0', '0', 'Открыть'],
                ]),
                t('Внутри проекта — отдельные исследования со своими заданиями, участниками и результатами.', 1016, 17),
            ], gap=24),
            panel('CreateProjectPanel', 576, [
                t('Новый проект', 528, 24, True),
                t('Объедините исследования одного продукта или интерфейса.', 528, 17),
                field('Название проекта *', 'Сервис доставки', 528),
                field('Описание · необязательно', 'Проверяем выбор и оформление доставки', 528),
                t('Проект будет доступен обоим коллегам команды.', 528, 15),
                row('CreateProjectActions', 528, [button('Создать проект', 300), button('Отмена', 204)], 48, gap=24),
                t('После создания откроется проект. В нём можно создать первое исследование.', 528, 15),
            ], 568),
        ], 568, gap=24),
    ]
    studies = [
        heading('Интернет-магазин', 'Все проекты / Интернет-магазин', 'Создать исследование'),
        t('Каталог, корзина и оформление. Каждое исследование хранит собственные настройки и результаты.', 1616, 17),
        stats([('Исследований', '3', 'В этом проекте'), ('Идёт сбор', '1', 'Участники могут проходить тест'), ('Черновиков', '1', 'Ожидает настройки и запуска')]),
        row('StudyFilters', 1616, [button('Все статусы', 260), field('Найти исследование', 'Название исследования', 640)], 72, gap=24),
        table('StudiesTable', 1616, [570, 200, 180, 180, 486], ['Исследование', 'Статус', 'Сценариев', 'Участников', 'Действия'], [
            ['Покупка в интернет-магазине\nРежим: задания', 'Идёт сбор', '3', '20', 'Результаты     ·     Управление запуском'],
            ['Навигация каталога\nРежим: задания', 'Черновик', '2', '0', 'Продолжить настройку'],
            ['Первое знакомство с магазином\nРежим: свободное изучение', 'Завершено', 'Не применимо', '12', 'Результаты'],
        ]),
        t('Участники считаются отдельно в каждом исследовании. Контрольные прохождения в это число не входят.', 1616, 15),
    ]
    setup = [
        heading('Настройка исследования', 'Все проекты / Интернет-магазин / Навигация каталога', 'К проверке и запуску'),
        row('SetupNavigation', 1616, [t('1. Настройка · текущий шаг', 510, 18, True), t('2. Проверка и запуск', 510, 18), t('Черновик · изменения сохранены', 548)], 48),
        row('SetupWorkspace', 1616, [
            box('StudyForm', 1016, [
                field('Название исследования *', 'Навигация каталога', 1016),
                box('ModeChoice', 1016, [t('Режим исследования', 1016, 15, True), row('ModeOptions', 1016, [button('Задания · выбран', 330), button('Свободное изучение', 330)], 48), t('Участник выполняет задания. Достижение цели оценивается по заданному критерию.', 1016, 15)], gap=10),
                field('Стартовая страница прототипа *', 'https://prototype.example.test/catalog', 1016),
                row('TaskListHeading', 1016, [t('Сценарии · 2', 652, 22, True), button('Добавить сценарий', 340)], 48, gap=24),
                panel('TaskOne', 1016, [t('1. Найти городской рюкзак', 968, 19, True), t('Найдите городской рюкзак и откройте его карточку.', 968), row('TaskActionsOne', 968, [t('Цель: открыта карточка товара', 488), button('Критерий успеха', 240), button('Изменить', 208)], 48)], 160),
                panel('TaskTwo', 1016, [t('2. Добавить товар в корзину', 968, 19, True), t('Выберите размер M и добавьте рюкзак в корзину.', 968), row('TaskActionsTwo', 968, [t('Цель: нажата кнопка добавления', 488), button('Критерий успеха', 240), button('Изменить', 208)], 48)], 160),
            ], gap=20),
            panel('ConnectionPanel', 576, [
                t('Подключение прототипа', 528, 24, True),
                t('Добавьте код сбора в тестируемый интерфейс, затем выполните проверку.', 528, 17),
                box('CodePlaceholder', 528, [t('Код подключения исследования', 480, 17, True), t('Здесь сервис выдаст фрагмент для установки в прототип.', 480, 15)], 100, pad=24, fill=True, gap=12),
                row('ConnectionActions', 528, [button('Скопировать код', 252), button('Проверить', 252)], 48, gap=24),
                t('Данные поступают', 528, 20, True),
                t('Последняя проверка: сегодня, 14:32\nКонтрольные клики и переходы получены.', 528),
                t('Перед запуском', 528, 19, True),
                t('Откройте прототип с устройства и сети участника. Доступность для команды не гарантирует доступ по приглашению.', 528, 15),
                t('Записываются действия и введённое содержимое полей. Объяснение записи показывается участнику до старта.', 528, 15),
            ], 680),
        ], 680, gap=24),
        row('SaveActions', 1616, [button('Сохранить черновик', 280), t('Сохранение не запускает сбор данных', 1280, 15)], 48, gap=24),
    ]
    launch = [
        heading('Проверка и запуск', 'Все проекты / Интернет-магазин / Навигация каталога'),
        row('LaunchNavigation', 1616, [button('Вернуться к настройке', 340), t('Черновик · ещё не запущено', 610, 18, True), t('2 сценария · режим заданий', 618)], 48),
        row('LaunchWorkspace', 1616, [
            panel('ReadinessChecklist', 984, [
                t('Готовность исследования', 936, 24, True),
                t('Проверено · настройки сохранены', 936, 19, True),
                t('Два задания и критерии успеха заданы.', 936),
                t('Проверено · прототип подключён', 936, 19, True),
                t('Контрольные события поступают. Последняя проверка: 14:32.', 936),
                t('Проверено · контрольное прохождение завершено', 936, 19, True),
                t('Задания, переходы и запись просмотрены. Контрольная попытка отделена от результатов участников.', 936),
                row('PreflightActions', 936, [button('Пройти ещё раз', 280), button('Посмотреть проверку', 300)], 48, gap=24),
                t('Убедитесь, что приглашённым участникам доступен сервер прототипа.', 936, 15),
            ], 528),
            panel('StartPanel', 608, [
                t('Пригласить участников', 560, 24, True),
                t('Исследование готово к запуску', 560, 20, True),
                t('После запуска появится ссылка. Вы отправляете её участникам самостоятельно.', 560, 17),
                button('Запустить и создать ссылку', 560),
                box('InvitationPlaceholder', 560, [t('Ссылка для участников', 512, 15, True), t('Появится после успешного запуска', 512, 17)], 100, pad=24, gap=12, border=True),
                t('Участники входят без регистрации и получают номер. Введённое содержимое полей может попасть в запись.', 560, 15),
                t('Участников: 0 · контрольное прохождение не учитывается', 560, 15),
            ], 528),
        ], 528, gap=24),
        panel('ResultsNext', 1616, [row('ResultsNextContent', 1568, [box('ResultsNextText', 1130, [t('Когда начнут поступать данные', 1130, 20, True), t('В обзоре появятся цифры по сценариям. Оттуда можно открыть карту, воронку и записи.', 1130)], gap=8), button('Открыть обзор результатов', 414)], 64, gap=24)], 112),
    ]
    return [('Projects', projects), ('Studies', studies), ('StudySetup', setup), ('Launch', launch)]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for index, (name, children) in enumerate(screens()):
        if name == 'Projects':
            area=children[2]
            area['children']=area['children'][:1]
            listing=area['children'][0];listing['w']=1616
            listing['children'][1]['w']=1616
            project_table=listing['children'][0];project_table['w']=1616
            for table_row in project_table['children']:
                table_row['w']=1616
                for cell,width in zip(table_row['children'],[820,260,260,276]):
                    cell['w']=width-16
        if name == 'Launch':
            children[2]['h'] = 600
            for child in children[2]['children']:
                child['h'] = 600
        header=row('Header',1920,[t('UX-Lab',200,22,True),t('Все проекты',240),t('Рабочее пространство команды' if name=='Projects' else 'Проект: Интернет-магазин',960,18,True),t('Коллега',340)],64,gap=24,pad=24)
        nav=['Все проекты'] if name=='Projects' else ['Все проекты','Исследования проекта']
        if name in ('StudySetup','Launch'):
            nav += ['Настройка исследования','Проверка и запуск','Обзор результатов']
        active={'Projects':'Все проекты','Studies':'Исследования проекта','StudySetup':'Настройка исследования','Launch':'Проверка и запуск'}[name]
        sidebar=box('Sidebar',240,[t('КОМАНДА' if name=='Projects' else 'ПРОЕКТ',192,12,True)]+[box('NavigationItem',192,[t(('• ' if n==active else '')+n,192,16,n==active)],52,gap=0) for n in nav],1016,gap=12,pad=24)
        sidebar=contextual_sidebar(name)
        workspace=row('Workspace',1920,[sidebar,box('Main',1680,children,1016,gap=24,pad=32)],1016,gap=0)
        data=dict(name=name,index=index,header=header,workspace=workspace)
        renderer=RENDER.replace("getNodeByIdAsync('20:3')",f"getNodeByIdAsync('{SECTION}')")
        renderer=renderer.replace("if(d.direction==='HORIZONTAL')n.counterAxisAlignItems='CENTER';", "if(d.direction==='HORIZONTAL')n.counterAxisAlignItems=['ProjectsWorkspace','SetupWorkspace','LaunchWorkspace'].includes(d.name)?'MIN':'CENTER';")
        if name == 'Projects':
            data['modal']=project_modal()
            renderer=renderer.replace('const issues=[];',MODAL_JS+'\nconst issues=[];')
        (OUT/f'{index+1:02}.js').write_text('const DATA='+json.dumps(data,ensure_ascii=False)+';\n'+renderer,encoding='utf-8')
    print('Prepared four additional screens in section '+SECTION)

if __name__=='__main__':main()
