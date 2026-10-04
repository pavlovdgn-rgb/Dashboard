"""Build the authorized detailed wireframe set from reusable deterministic specs."""
from pathlib import Path
from copy import deepcopy
import json
from build_wireframes import t,box,row,button,field,heading,stats,table,contextual_sidebar,RENDER,product

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/complete-wireframes'
GROUPS={'setup':('45:2',4,2000,1360),'participant':('45:3',4,2000,1360),'analysis':('45:4',3,2000,1360),'reports':('45:5',4,2000,1360),'mobile':('45:6',4,470,1000),'patterns':('45:7',1,2000,1360)}
ITEMS=[]

def existing(folder,number):
    line=(ROOT/f'.tmp/{folder}/{number:02}.js').read_text(encoding='utf-8').splitlines()[0]
    return json.loads(line[len('const DATA='):-1])
BASE={n:existing('wireframes',i+1) for i,n in enumerate(['ResultsOverview','Heatmaps','Funnel','Replay','SuccessCriteria'])}
BASE.update({n:existing('project-wireframes',i+1) for i,n in enumerate(['Projects','Studies','StudySetup','Launch'])})

def find(d,name):
    if d.get('name')==name:return d
    for c in d.get('children',[]):
        result=find(c,name)
        if result:return result
    return None
def replace_text(d,old,new):
    if d.get('kind')=='text':d['text']=d['text'].replace(old,new)
    for value in d.values():
        if isinstance(value,dict):replace_text(value,old,new)
        elif isinstance(value,list):
            for c in value:
                if isinstance(c,dict):replace_text(c,old,new)
def card(name,w,children,pad=24,gap=20,h=None):return box(name,w,children,h,pad=pad,gap=gap,border=True)
def actions(*labels,w=1616):return row('Actions',w,[button(label,width) for label,width in labels],48,gap=16)
def notice(title,body,w=1616):return card('Notice',w,[t(title,w-48,20,True),t(body,w-48,16)],gap=12)
def empty(title,body,cta,w=1616):return card('EmptyState',w,[t(title,w-64,28,True),t(body,w-64,18),button(cta,360)],pad=32,gap=24,h=300)
def shell(name,title,sub,children,context='ResultsOverview',action=None):
    hdr=row('Header',1920,[t('UX-Lab',200,22,True),t('Все проекты',240),t('Интернет-магазин · Покупка в интернет-магазине',960,18,True),t('Коллега',340)],64,gap=24,pad=24)
    main=box('Main',1680,[heading(title,sub,action)]+children,1016,gap=24,pad=32)
    return dict(name=name,width=1920,height=1080,header=hdr,workspace=row('Workspace',1920,[contextual_sidebar(context),main],1016,gap=0))
def clone(name,source):
    d=deepcopy(BASE[source]);d['name']=name;d['width']=1920;d['height']=1080;return d
def main(d):return find(d['workspace'],'Main')
def add(name,group,title,trigger,data,kind='Страница',note=''):
    data.update(name=name,group=group,title=title,trigger=trigger,kind=kind,note=note)
    ITEMS.append(data);return data
def basic(name,title,body,cta,context,group='setup',trigger='Открыть экран'):
    page_title='Все проекты' if context=='Projects' else 'Интернет-магазин' if context=='Studies' else title
    sub='Рабочее пространство команды' if context=='Projects' else 'Все проекты / Интернет-магазин'
    return add(name,group,title,trigger,shell(name,page_title,sub,[empty(title,body,cta)],context),kind='Состояние страницы')

def build_setup():
    login=dict(name='Login',width=1920,height=1080,standalone=card('LoginCard',640,[t('UX-Lab',576,22,True),t('Вход в рабочее пространство',576,30,True),t('Доступ для коллег вашей команды. Участники теста входят по приглашению без регистрации.',576,18),button('Продолжить вход',576),t('Нет доступа? Обратитесь к коллеге, который настраивает сервис.',576,15)],pad=32,gap=24))
    add('Login','setup','Вход коллеги','Открыть командную часть сервиса',login,note='D08 открыт: CTA обозначает границу входа; способ аутентификации не выбран.')
    d=clone('ProjectsDefault','Projects');d.pop('modal',None)
    add('ProjectsDefault','setup','Все проекты','Вход выполнен / закрыть создание проекта',d)
    basic('ProjectsEmpty','Пока нет проектов','Создайте проект для продукта, который будете тестировать. Внутри него появятся исследования.','Создать проект','Projects',trigger='Первый вход в рабочее пространство')
    d=basic('StudiesEmpty','В проекте пока нет исследований','Проект «Сервис доставки» создан. Добавьте первое исследование и настройте тест.','Создать исследование','Studies',trigger='Создать проект → успешное сохранение')
    replace_text(d,'Интернет-магазин','Сервис доставки')
    d=shell('StudySetupBlank','Новое исследование','Все проекты / Сервис доставки / Новое исследование',[
        card('NewStudyForm',1040,[field('Название исследования *','Например, проверка оформления заказа',992),t('Режим исследования',992,18,True),actions(('Задания · выбран',340),('Свободное изучение',340),w=992),field('Стартовая страница прототипа *','https://',992),t('После сохранения можно добавить задания и подключить прототип.',992),actions(('Создать черновик',300),('Отмена',200),w=992)],gap=24),
        t('Исследование появится в проекте после успешного сохранения.',1616,15)],'StudySetup')
    replace_text(d,'Интернет-магазин','Сервис доставки');replace_text(d,'Навигация каталога','Новое исследование')
    add('StudySetupBlank','setup','Новый черновик','Проект → Создать исследование',d,kind='Состояние страницы')
    d=shell('StudySetupFree','Свободное изучение','Все проекты / Интернет-магазин / Первое знакомство',[
        field('Название исследования','Первое знакомство с магазином',1040),
        actions(('Задания',280),('Свободное изучение · выбран',420)),
        field('Стартовая страница','https://prototype.example.test/',1040),
        notice('Исследуйте интерфейс без заданий','Участник свободно знакомится с сайтом. Записываются клики, прокрутка, переходы и ввод. Без заданной цели успешность не рассчитывается.'),
        notice('Инструкция участнику','Ознакомьтесь с магазином так, как сделали бы это обычно. Когда закончите, нажмите «Завершить изучение».'),
        actions(('Сохранить черновик',280),('К проверке и запуску',320))],'StudySetup')
    replace_text(d,'Навигация каталога','Первое знакомство');add('StudySetupFree','setup','Настройка свободного изучения','Выбрать режим «Свободное изучение»',d,kind='Состояние страницы')
    d=shell('TaskEditor','Редактирование задания','Настройка исследования / Сценарий 1',[
        row('TaskEditorWorkspace',1616,[card('TaskForm',1040,[field('Название задания *','Найти городской рюкзак',992),t('Текст для участника *',992,15,True),card('TaskText',992,[t('Найдите городской рюкзак для повседневных поездок и откройте его карточку.',944,18)],h=148),t('Опишите цель участника, не подсказывая нужную кнопку или маршрут.',992,15),actions(('Сохранить задание',300),('Отмена',200),w=992),t('Есть несохранённые изменения',992,15)],gap=20),card('TaskCriterion',552,[t('Критерий успеха',504,24,True),t('Целевая страница',504,18,True),t('/products/backpack',504,18),t('Текст задания и автоматическая проверка задаются отдельно.',504),button('Настроить критерий',504),button('Выбрать задание из списка',504)],gap=24)],gap=24)],'StudySetup')
    add('TaskEditor','setup','Редактор задания','Добавить сценарий / Изменить',d,kind='Редактор внутри страницы')
    d=deepcopy(d);d['modal']=box('TaskPickerModal',800,[row('ModalHeader',736,[t('Выбрать задание из списка',672,26,True),button('×',40)],48,gap=24),t('Выберите задание. Его текст можно изменить после добавления.',736),card('SelectedTask',736,[t('● Найти товар',688,20,True),t('Найдите подходящий товар и откройте его карточку.',688)],gap=12),card('TaskOption',736,[t('○ Добавить товар в корзину',688,20),t('Выберите товар и добавьте его в корзину.',688)],gap=12),card('TaskOption',736,[t('○ Оформить заказ',688,20),t('Оформите заказ на выбранный товар.',688)],gap=12),actions(('Отмена',220),('Добавить задание',492),w=736)],pad=32,gap=20,border=True)
    add('TaskPicker','setup','Выбор задания','Редактор → Выбрать задание из списка',d,kind='Модалка по центру',note='D06: показан пример короткого списка; источник списка ещё не выбран.')
    for name,typ,label,value,hint in [('CriteriaURL','Целевая страница','URL / путь','/products/backpack','Успех фиксируется при открытии указанной страницы.'),('CriteriaButton','Целевая кнопка','Элемент интерфейса','[data-testid="add-to-cart"]','Успех фиксируется при нажатии выбранной кнопки.')]:
        d=shell(name,'Критерий успеха','Настройка исследования / Найти городской рюкзак',[
            t('Задание: найдите городской рюкзак и откройте его карточку.' if name=='CriteriaURL' else 'Задание: добавьте рюкзак размера M в корзину.',1616,20),
            actions((('Целевая страница · выбрана' if name=='CriteriaURL' else 'Целевая страница'),350),(('Целевая кнопка · выбрана' if name=='CriteriaButton' else 'Целевая кнопка'),350),('Последовательность',350)),
            row('CriterionWorkspace',1616,[card('GoalForm',1040,[t(typ,992,24,True),field(label,value,992),t(hint,992,18),button('Проверить условие',300)],gap=24),card('GoalExplanation',552,[t('Перед запуском',504,24,True),t('Выполните контрольное прохождение и убедитесь, что нужное действие фиксируется.',504,18),t('Если данные не поступили, результат проверки неизвестен.',504,16)],gap=24)],gap=24),
            actions(('Сохранить критерий',300),('Вернуться к заданию',300))],'SuccessCriteria')
        if name=='CriteriaButton':replace_text(d,'Найти городской рюкзак','Добавить товар в корзину')
        add(name,'setup',typ,'Критерий успеха → '+typ,d,kind='Состояние страницы',note='D01: URL/селектор — предложение привязки, не утверждение реализации.')
    d=clone('ConnectionError','StudySetup');c=find(d['workspace'],'ConnectionPanel');c['children']=[t('Подключение прототипа',528,24,True),t('Контрольные события не получены',528,20,True),t('Проверка завершена, но сервис пока не может подтвердить запись.',528,17),card('InstallInstructions',528,[t('1. Установите код исследования.\n2. Откройте нужную страницу.\n3. Выполните клик и переход.\n4. Повторите проверку.',480,17)],gap=12),button('Скопировать код',528),button('Повторить проверку',528),t('Прототип открывается, но это ещё не подтверждает поступление данных.',528,15)];
    add('ConnectionError','setup','Нет контрольных событий','Настройка → Проверить подключение',d,kind='Состояние постоянного блока')
    d=shell('ControlResult','Контрольное прохождение','Проверка и запуск / Контрольная попытка',[
        notice('Проверка пройдена','Это контрольная попытка. Она не входит в показатели реальных участников.'),
        table('ControlChecklist',1616,[620,350,646],['Проверка','Результат','Наблюдение'],[['Прототип доступен','Подтверждено','Открыт с устройства участника'],['Клики и переходы','Получены','Записаны контрольные действия'],['Критерии двух заданий','Сработали','Целевые действия зафиксированы'],['Запись и введённые данные','Просмотрены','Воспроизведение доступно']]),
        actions(('Посмотреть контрольную запись',410),('Повторить прохождение',330),('К запуску',250))],'Launch')
    add('ControlResult','setup','Результат контрольного теста','Завершить контрольное прохождение → Проверка',d)
    for name,success in [('LaunchActive',True),('LaunchError',False)]:
        d=clone(name,'Launch');c=find(d['workspace'],'StartPanel')
        c['children']=([t('Пригласить участников',560,24,True),t('Идёт сбор данных',560,22,True),field('Ссылка для участников','https://research.example.test/t/catalog-demo',560),button('Скопировать ссылку',560),t('Ссылка скопирована',560,16,True),t('Отправьте ссылку участникам самостоятельно. Вход без регистрации.',560,17),t('Участников: 0\nКонтрольная попытка не учитывается.',560,16)] if success else [t('Запуск не выполнен',560,26,True),t('Сервис не подтвердил запуск исследования. Ссылка для участников пока не создана.',560,18),notice('Настройки сохранены','Черновик доступен, повторно вводить задания не нужно.',560),button('Повторить запуск',560),button('Вернуться к настройке',560)])
        replace_text(d,'Черновик · ещё не запущено','Идёт сбор данных' if success else 'Черновик · ошибка запуска')
        add(name,'setup','Исследование запущено' if success else 'Ошибка запуска','Запустить и создать ссылку → '+('Успех' if success else 'Ошибка'),d,kind='Состояние страницы',note='example.test — демонстрационный адрес; копирование показано как состояние, а не настоящий буфер обмена.')

def participant_spec(name,title,children,mobile=False,session=False):
    width=390 if mobile else 1920;height=844 if mobile else 1080
    content_width=342 if mobile else 800
    head=row('ParticipantHeader',width,[t('UX-тест · Интернет-магазин',width-48,15,True)],64,pad=24)
    content=box('ParticipantContent',content_width,[t(title,content_width,26 if mobile else 32,True)]+children,gap=20 if mobile else 24)
    return dict(name=name,width=width,height=height,header=head,participant=content,session=session,mobile=mobile)

def build_participants():
    for mobile in (False,True):
        w=342 if mobile else 800;group='mobile' if mobile else 'participant';suffix='Mobile' if mobile else ''
        d=participant_spec('ParticipantIntro'+suffix,'Помогите проверить интерфейс',[
            t('Исследование: покупка в интернет-магазине\nВаш номер: 014 · регистрация не нужна',w,16),
            t('Выполните задания в своём темпе. Мы проверяем интерфейс, а не ваши навыки.',w,17),
            card('RecordingNotice',w,[t('Что записывается',w-40,19,True),t('Клики, прокрутка, переходы и всё, что вы вводите в поля. Запись сможет просмотреть команда исследования.',w-40,16),t('Камера и голос не записываются.',w-40,15)],pad=20,gap=14),
            button('Начать тест',w),t('Если не хотите участвовать, закройте эту страницу до начала теста.',w,14)],mobile)
        add('ParticipantIntro'+suffix,group,'Начало участия','Открыть ссылку приглашения',d,kind='Мобильная страница' if mobile else 'Страница участника')
        d=participant_spec('TaskBriefing'+suffix,'Задание 1 из 3',[
            t('Найдите городской рюкзак и добавьте его в корзину.',w,22,True),
            t('Действуйте так, как сделали бы это при обычной покупке. Во время прохождения текст задания останется доступен.',w,17),
            button('Перейти к выполнению',w),t('Участник 014',w,14)],mobile)
        add('TaskBriefing'+suffix,group,'Инструкция задания','Начать тест / перейти к следующему заданию',d,kind='Мобильная страница' if mobile else 'Страница участника')
        if mobile:
            prototype=card('LivePrototype',w,[t('Магазин · Каталог',w-32,16,True),box('ProductImage',w-32,[t('Изображение рюкзака',w-56,15)],112,pad=12,fill=True),t('Городской рюкзак',w-32,20,True),t('4 900 ₽',w-32,21,True),button('Добавить в корзину',w-32)],pad=16,gap=12)
            d=participant_spec('ParticipantSessionMobile','Выполнение задания',[card('TestControls',w,[t('Задание 1 из 3',w-32,16,True),t('Найдите рюкзак и добавьте в корзину.',w-32,16),actions(('Готово',130),('Не получилось',164),w=w-32)],pad=16,gap=12),prototype,t('Ввод и действия записываются',w,13)],True,True)
        else:
            d=participant_spec('ParticipantSession','Выполнение задания',[],False,True)
            d['participant']=box('ParticipantContent',1800,[row('LiveTestWorkspace',1800,[product(1232,620),card('TaskControls',544,[t('Задание 1 из 3',496,25,True),t('Найдите городской рюкзак и добавьте его в корзину.',496,22),t('Когда закончите, отметьте результат. Это не заменяет проверку критерия успеха.',496,16),button('Готово, перейти дальше',496),button('Не могу выполнить',496),t('Участник 014\nДействия и ввод записываются',496,15)],gap=24,h=620)],gap=24)],gap=24)
            replace_text(d['participant'],'Слой тепловой карты — плейсхолдер','Тестируемый интерфейс · пример')
        add('ParticipantSession'+suffix,group,'Прохождение в прототипе','Перейти к выполнению',d,kind='Мобильное прохождение' if mobile else 'Прототип с панелью теста',note='Оболочка — визуальное предложение D09/D10; не утверждается iframe. Ответ участника отделён от автоматической оценки цели.')
        d=participant_spec('ParticipantFinish'+suffix,'Спасибо за участие!',[
            t('Вы завершили прохождение.',w,22,True),notice('Данные получены','Сервис подтвердил передачу результатов этой попытки.',w),t('Ваш номер: 014\nТеперь можно закрыть страницу.',w,17)],mobile)
        add('ParticipantFinish'+suffix,group,'Участие завершено','Последнее задание завершено и передача подтверждена',d,kind='Мобильная страница' if mobile else 'Страница участника')
    for name,title,body,action in [
        ('UnavailableLink','Эта ссылка недоступна','Исследование закрыто или ссылка больше не действует. Уточните актуальную ссылку у человека, который пригласил вас.','Проверить ещё раз'),
        ('PrototypeUnavailable','Не удалось открыть интерфейс','Тестируемая страница недоступна. Ваше участие не будет автоматически отмечено как неуспешное выполнение задания.','Повторить открытие'),
        ('ParticipantTransferError','Передача данных не подтверждена','Прохождение завершено, но сервис не подтвердил получение всех данных. Проверьте соединение и пока оставьте страницу открытой.','Проверить статус передачи')]:
        d=participant_spec(name,title,[t(body,800,20),button(action,800),t('Номер участника: 014' if name!='UnavailableLink' else 'Регистрация для участия не требуется.',800,16)])
        if name=='PrototypeUnavailable':d['participant']['children'].append(button('Завершить: не удалось открыть',800))
        add(name,'participant',title,'Открытие приглашения / прототипа / завершение → ошибка',d,kind='Состояние участника')

def build_analysis():
    d=shell('Participants','Участники исследования','Покупка в интернет-магазине / Участники',[
        notice('Выборка из тепловой карты','Найти товар и добавить в корзину · Карточка товара · Кнопка «Добавить в корзину» · Компьютер'),
        actions(('Все участники исследования',360),('Устройство: компьютер',320),('Данные: любые',250)),
        t('9 участников выбранной области · показаны первые 4',1616,20,True),
        table('ParticipantsTable',1616,[190,210,220,340,310,346],['Участник','Устройство','Попытка','Исход задания','Данные','Действие'],[['014','Компьютер','1','Цель достигнута','Полные','Открыть участника'],['018','Компьютер','1','Нет оценки','Неполные','Открыть участника'],['009','Компьютер','1','Цель достигнута','Полные','Открыть участника'],['012','Компьютер','1','Цель достигнута','Полные','Открыть участника']]),
        t('Участники 1–4 из 9    ·    Следующая страница',1616,16),t('Неполная запись и недостижение цели — разные признаки.',1616,15)],'Replay')
    add('Participants','analysis','Участники выбранной области','Карта → Открыть участников / пункт «Участники»',d,note='Состояние фильтра из карты; пункт меню без источника открывает полный список.')
    d=shell('ParticipantDetails','Участник 014','Участники / 014',[
        actions(('Вернуться к выборке из карты',400),('Устройство: компьютер',320)),
        stats([('Данные','Полные','Для выбранной попытки'),('Устройство','Компьютер','Окно 1440×900'),('Попыток','1','В каждом начатом задании')]),
        table('ParticipantTasks',1616,[520,300,210,260,326],['Задание','Исход','Время','Данные','Действие'],[['Добавить товар в корзину','Цель достигнута','02:10','Полные','Открыть запись'],['Изменить количество','Цель достигнута','01:08','Полные','Открыть запись'],['Оформить заказ','Цель не достигнута','04:32','Полные','Открыть запись']]),
        notice('Выбрано: Оформить заказ','Наблюдение завершено. Запись 04:32 доступна; 4 сигнала затруднений требуют просмотра контекста.'),
        actions(('Смотреть запись оформления',420),('Сигналы этого участника',360))],'Replay')
    add('ParticipantDetails','analysis','Детали участника','Список участников → Открыть участника',d)
    d=shell('Signals','Сигналы затруднений','Покупка в интернет-магазине / Сигналы',[
        notice('Сигнал — повод посмотреть запись','Повторные клики, отсутствие результата, возвраты и паузы не доказывают причину затруднения.'),
        actions(('Сценарий: оформить заказ',360),('Тип: все сигналы',290),('Устройство: все',290)),
        table('SignalsTable',1616,[360,200,390,180,486],['Сигнал','Участник','Место','Время','Действие'],[['Повторные клики','014','Отправить заказ','02:18','Открыть запись'],['Клик без результата','014','Область «Доставка»','01:52','Открыть запись'],['Возврат','014','Контактные данные','01:36','Открыть запись'],['Длительная пауза','014','Оформление','00:48','Открыть запись']]),
        actions(('Правила определения сигналов',420),('Участники этой выборки',340))],'Replay')
    nav=find(d['workspace'],'Sidebar');replace_text(nav,'• Участники','Участники');replace_text(nav,'Сигналы затруднений','• Сигналы затруднений')
    add('Signals','analysis','Все четыре сигнала','Пункт «Сигналы затруднений» / выбранная группа',d,note='D04: пороги не определены; демонстрационные события не являются научным стандартом.')
    basic('ResultsEmpty','Пока нет результатов','Исследование запущено. Отправьте ссылку участникам — после прохождений здесь появятся показатели.','К ссылке приглашения','ResultsOverview','analysis','Запущенное исследование → Результаты')
    d=shell('ResultsFree','Обзор свободного изучения','Первое знакомство с магазином / Результаты',[
        notice('Режим: свободное изучение','Задания и критерии не заданы. Успешность и сценарная воронка не рассчитываются.'),
        stats([('Участников','12','Уникальные участники'),('С доступной записью','11 из 12','Открыть участников'),('С неполными данными','1 из 12','Проверить полноту')]),
        table('ExploredPages',1616,[750,250,300,316],['Страница','Участников','Кликов','Действие'],[['Главная','12','65','Открыть карту'],['Каталог','10','84','Открыть карту'],['Карточка товара','8','42','Открыть карту']]),
        actions(('Участники и записи',300),('Сигналы затруднений',330),('Экспорт в PDF',270))],'ResultsOverview')
    replace_text(d,'Покупка в интернет-магазине','Первое знакомство с магазином');add('ResultsFree','analysis','Свободное изучение: результаты','Свободное исследование → Результаты',d,kind='Состояние страницы')
    for name,first in [('HeatmapsFirstClick',True),('HeatmapsDynamicState',False)]:
        d=clone(name,'Heatmaps');d['heat']='first' if first else 'dynamic'
        if first:
            replace_text(d,'98 кликов · 18 участников','18 первых кликов · 18 участников');replace_text(d,'18 из 98 кликов','6 из 18 первых кликов');replace_text(d,'9 из 18 участников карты','6 из 18 участников карты');replace_text(d,'Открыть 9 участников','Открыть 6 участников')
            replace_text(d,'Первый клик','Первый клик · выбран');replace_text(d,'Слой тепловой карты — плейсхолдер','Демонстрационные первые клики')
        else:
            replace_text(d,'Состояние: Карточка товара','Состояние: Выбор размера');replace_text(d,'98 кликов · 18 участников','24 клика · 10 участников');replace_text(d,'1 попытка без кликов · 1 неполная','10 участников открыли окно');replace_text(d,'18 из 98 кликов','12 из 24 кликов');replace_text(d,'9 из 18 участников карты','8 из 10 участников карты');replace_text(d,'Открыть 9 участников','Открыть 8 участников');replace_text(d,'Кнопка «Добавить в корзину»','Размер M в окне выбора')
            find(d['workspace'],'PrototypePlaceholder')['children']=[t('Магазин / Карточка товара / Выбор размера',1192,18,True),row('StateModalRow',1192,[box('ProductBackground',296,[t('Карточка товара\nпод открытым окном',248,20)],360,pad=24,fill=True),card('PrototypeSizeDialog',872,[t('Выберите размер',824,28,True),t('Городской рюкзак',824,18),actions(('S',180),('M · выбран',230),('L',180),w=824),button('Подтвердить размер',360)],gap=24,h=360)],gap=24)]
        add(name,'analysis','Первый клик' if first else 'Карта открытого окна','Переключить режим карты' if first else 'Выбрать состояние «Выбор размера»',d,kind='Состояние страницы',note='Точки искусственные. D02/D05 остаются открытыми; размеры/состояния не смешиваются.')
    d=clone('ReplayIncomplete','Replay');replace_text(d,'014','018');replace_text(d,'Исход: цель не достигнута','Исход: нет оценки');replace_text(d,'Данные: полные','Данные: неполные');replace_text(d,'Позиция: 02:18   ·   Повторные клики у кнопки «Отправить заказ»','Нет данных с 01:40 до 02:05 · разрыв записи');d['replay']='incomplete'
    find(d['workspace'],'EventsPanel')['children'].insert(0,t('Разрыв 01:40–02:05\nВ этом интервале действия неизвестны.',408,19,True));find(d['workspace'],'EventsPanel')['gap']=18
    add('ReplayIncomplete','analysis','Неполная запись','Участник с неполными данными → Запись',d,kind='Состояние проигрывателя')
    d=basic('ReplayUnavailable','Запись недоступна','Данные участника сохранены, но воспроизведение сейчас получить не удалось. Результат задания не меняется из-за ошибки загрузки.','Повторить загрузку','Replay','analysis','Открыть запись → ошибка');main(d)['children'].append(button('Вернуться к участнику',340))

def report_preview(w=740):
    return card('ReportPagePreview',w,[t('Покупка в интернет-магазине',w-64,24,True),t('Результаты UX-тестирования · демонстрация',w-64,15),t('20 участников · 3 сценария',w-64,21,True),t('Сценарий: оформить заказ\nДостигли цели: 10 из 15 оценимых · 67%\nУ 1 из 16 начавших недостаточно данных.',w-64,17),box('PDFHeatmap',w-64,[t('Карта кликов · Карточка товара',w-96,17,True),t('18 участников · 98 кликов\nКомпьютер · окно 1440×900',w-96,15)],170,pad=16,fill=True,gap=12),t('Ограничения\nМалая выборка. Неполные данные показаны отдельно. Сигналы не доказывают причину.',w-64,15),t('1 / 3',w-64,14)],pad=32,gap=20,h=660)

def build_reports():
    controls=card('ReportConfiguration',852,[t('Состав отчёта',804,24,True),field('Область данных','Все 3 сценария · все устройства',804),t('☑ Сводные показатели\n☑ Результаты сценариев и воронки\n☑ Тепловые карты выбранных страниц\n☑ Сигналы затруднений\n☑ Полнота данных и ограничения',804,19),notice('Контекст сохраняется','В PDF указываются выборка, состояние страницы, устройство и знаменатели метрик.',804),button('Сформировать PDF',804),t('Просмотр всех записей перед экспортом не обязателен.',804,15)],gap=24,h=660)
    d=shell('Report','Отчёт PDF','Покупка в интернет-магазине / Экспорт',[
        row('ReportWorkspace',1616,[controls,report_preview()],gap=24)],'ResultsOverview')
    nav=find(d['workspace'],'Sidebar');replace_text(nav,'• Обзор результатов','Обзор результатов');replace_text(nav,'Отчёт PDF','• Отчёт PDF')
    add('Report','reports','Настройка и предпросмотр PDF','Обзор → Экспорт в PDF',d,note='D11: состав страниц — предложение. Предпросмотр показывает демонстрационные данные.')
    for name,title,body in [('ReportGenerating','Формируем PDF','Собираем выбранные разделы. Дождитесь результата; повторный запуск сейчас недоступен.'),('ReportError','Не удалось сформировать PDF','Состав отчёта сохранён. Попробуйте сформировать файл ещё раз.')]:
        variant=deepcopy(d);m=main(variant);m['children']=[heading('Отчёт PDF','Покупка в интернет-магазине / Экспорт'),notice(title,body),notice('Выбранный состав','Все 3 сценария · все устройства · показатели, карты, воронки, сигналы и ограничения')]
        if name=='ReportGenerating':m['children'].append(box('ExportProgress',1616,[box('ProgressTrack',1200,[],16,fill=True),t('Формирование…',1200,18)],gap=16))
        else:m['children'].append(actions(('Повторить формирование',370),('К составу отчёта',300)))
        add(name,'reports',title,'Сформировать PDF → '+('Ожидание' if name=='ReportGenerating' else 'Ошибка'),variant,kind='Состояние экспорта')
    d=deepcopy(d);c=find(d['workspace'],'ReportConfiguration');c['children']=[t('PDF готов',804,28,True),t('Покупка в интернет-магазине.pdf',804,22),t('3 страницы · демонстрационный отчёт',804,16),button('Скачать PDF',804),button('Изменить состав отчёта',804),notice('Включены ограничения данных','Полнота записей и база расчёта показаны рядом с метриками.',804)]
    add('ReportReady','reports','Готовый PDF','Формирование успешно завершено',d,kind='Состояние экспорта')

def build_patterns():
    cards=[
        card('LoadingPattern',784,[t('Загрузка результатов',736,24,True),box('Skeleton',736,[],64,fill=True),t('Загружаем данные…',736),t('Применяется: обзор, участники, карты, записи.',736,15)],h=240),
        card('LoadErrorPattern',784,[t('Не удалось загрузить',736,24,True),t('Фильтры сохранены. Повторите запрос.',736),button('Повторить',240)],h=240),
        card('FilterEmptyPattern',784,[t('По выбранным условиям нет данных',736,22,True),t('Само исследование и его результаты сохранены.',736),button('Сбросить фильтры',300)],h=240),
        card('ValidationPattern',784,[t('Ошибка поля',736,24,True),field('Название исследования *','',736),t('Введите название исследования',736,16,True)],h=240),
        card('SaveStatesPattern',784,[t('Состояния сохранения',736,24,True),t('Есть изменения → Сохраняем → Сохранено',736,18),t('Ошибка: изменения не сохранены. Повторить.',736,17)],h=210),
        card('FreeBriefingPattern',784,[t('Инструкция свободного изучения',736,22,True),t('Изучите магазин в своём темпе. Когда закончите, нажмите «Завершить изучение».',736,17),t('Задания и оценка успеха не навязываются.',736,15)],h=210),
    ]
    d=dict(name='SharedPatterns',width=1920,height=1080,standalone=box('PatternsBoard',1640,[t('Общие состояния интерфейса',1640,30,True),t('Паттерны, переиспользуемые на страницах. Это не отдельный экран продукта.',1640,18)]+[row('PatternRow',1640,cards[i:i+2],gap=32) for i in range(0,6,2)],gap=24))
    add('SharedPatterns','patterns','Общие состояния и обратная связь','Загрузка / фильтрация / валидация / сохранение',d,kind='Доска паттернов')

HELPERS=RENDER[RENDER.index('await figma.loadFontAsync'):RENDER.index('const title=')]
RENDER_ALL=r'''
const p=await figma.getNodeByIdAsync('20:2');await figma.setCurrentPageAsync(p);
const section=await figma.getNodeByIdAsync(DATA.sectionId);
if(section.children.some(n=>n.name===DATA.name))throw new Error('Frame exists; inspect before retry: '+DATA.name);
HELPERS
const label=txt(section,DATA.name+' — '+DATA.title,DATA.width,DATA.mobile?18:24,true,'ScreenTitle');label.x=DATA.x;label.y=DATA.y-(DATA.mobile?120:92);
const note=txt(section,DATA.kind+' · '+DATA.trigger+(!DATA.mobile&&DATA.note?'\n'+DATA.note:''),DATA.width,DATA.mobile?11:14,false,'ScreenAnnotation');note.x=DATA.x;note.y=DATA.y-(DATA.mobile?60:56);
const f=track(figma.createAutoLayout('VERTICAL'));section.appendChild(f);f.name=DATA.name;f.resize(DATA.width,DATA.height);f.primaryAxisSizingMode='FIXED';f.counterAxisSizingMode='FIXED';f.itemSpacing=0;f.fills=[{type:'SOLID',color:{r:1,g:1,b:1}}];f.x=DATA.x;f.y=DATA.y;f.clipsContent=true;
if(DATA.header)make(f,DATA.header);
if(DATA.workspace)make(f,DATA.workspace);
if(DATA.standalone){const body=make(f,DATA.standalone);body.layoutPositioning='ABSOLUTE';body.x=(f.width-body.width)/2;body.y=(f.height-body.height)/2;}
if(DATA.participant){const body=make(f,DATA.participant);body.layoutPositioning='ABSOLUTE';body.x=(f.width-body.width)/2;body.y=DATA.mobile?88:150;}
if(DATA.modal){const bg=track(figma.createRectangle());f.appendChild(bg);bg.name='ModalBackdrop';bg.layoutPositioning='ABSOLUTE';bg.resize(f.width,f.height);bg.x=0;bg.y=0;bg.fills=[{type:'SOLID',color:ink,opacity:0.4}];const m=make(f,DATA.modal);m.layoutPositioning='ABSOLUTE';m.fills=[{type:'SOLID',color:{r:1,g:1,b:1}}];m.x=(f.width-m.width)/2;m.y=(f.height-m.height)/2;}
const issues=[];for(const n of [f,...f.findAllWithCriteria({types:['FRAME']})])for(const c of n.children)if(c.visible&&(c.x<0||c.y<0||c.x+c.width>n.width+1||c.y+c.height>n.height+1))issues.push({parent:n.name,child:c.name,id:c.id,right:c.x+c.width,width:n.width,bottom:c.y+c.height,height:n.height});
return {createdNodeIds:ids,frameId:f.id,name:f.name,width:f.width,height:f.height,overflow:issues};
'''

def main_build():
    build_setup();build_participants();build_analysis();build_reports();build_patterns()
    assert len(ITEMS)==39,len(ITEMS)
    OUT.mkdir(parents=True,exist_ok=True)
    counter={};manifest=[]
    for d in ITEMS:
        if d.get('workspace'):
            sidebar=find(d['workspace'],'Sidebar')
            pc=find(sidebar,'ProjectContext');sc=find(sidebar,'StudyContext')
            project_name=pc['children'][1]['text'];study_name=sc['children'][1]['text']
            d['header']['children'][2]['text']=('Рабочее пространство команды' if project_name=='Не выбран' else 'Проект: '+project_name if study_name=='Не выбрано' else project_name+' / '+study_name)
        group=d['group'];sid,cols,dx,dy=GROUPS[group];index=counter.get(group,0);counter[group]=index+1
        d.setdefault('width',1920);d.setdefault('height',1080);d.update(sectionId=sid,x=80+(index%cols)*dx,y=128+(index//cols)*dy)
        helper=HELPERS.replace("if(d.direction==='HORIZONTAL')n.counterAxisAlignItems='CENTER';","if(d.direction==='HORIZONTAL')n.counterAxisAlignItems=(['Header','ParticipantHeader','Actions','ModalHeader'].includes(d.name)||d.name.startsWith('Table'))?'CENTER':'MIN';")
        # Checkboxes use ordinary text and simple controls, retaining editable low-fi layers.
        code='const DATA='+json.dumps(d,ensure_ascii=False)+';\n'+RENDER_ALL.replace('HELPERS',helper)
        (OUT/f"{d['name']}.js").write_text(code,encoding='utf-8')
        manifest.append({k:d[k] for k in ['name','title','group','sectionId','width','height','kind','trigger','note']})
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'prepared':len(ITEMS),'groups':counter},ensure_ascii=False))

if __name__=='__main__':main_build()
