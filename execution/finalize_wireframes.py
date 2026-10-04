"""Record verified Figma wireframes and reconcile local delivery status."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'ia/wireframes'
BASE = 'https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='
SCREENS = {
    'ResultsOverview': ('22-3', 'Обзор результатов'),
    'Heatmaps': ('22-95', 'Тепловая карта'),
    'Funnel': ('24-3', 'Воронка'),
    'Replay': ('24-93', 'Запись сессии'),
    'SuccessCriteria': ('24-173', 'Критерий успеха'),
}

for name, (node, label) in SCREENS.items():
    path = FOLDER / f'{name}.md'
    content = path.read_text(encoding='utf-8')
    status = f'**Статус:** отрисовано и проверено в Figma по общему апруву пользователя. [Открыть экран]({BASE}{node}).'
    content = re.sub(r'^\*\*Статус:\*\*.*$', status, content, flags=re.M)
    content = re.sub(r'## Следующее действие\n[\s\S]*$', '## Результат\n\nВсе пять экранов отрисованы. Ссылки и границы пакета — в [отчёте](figma-delivery.md).\n', content)
    if name == 'ResultsOverview':
        content = content.replace('PageHeading — 88 px', 'PageHeading — 76 px').replace('ContextBar — 56 px', 'ContextBar — 48 px')
        content = content.replace('заголовок 40 px, шапка', 'заголовок 26 px и промежуток 12 px, шапка')
        content = content.replace('выбор строки 48; сценарий 480; начали 144; завершили попытку 200; достигли цели 320; неполные данные 200; действие 224', 'сценарий 480; начали 150; завершили попытку 210; достигли цели 330; неполные данные 210; действие 236; отдельной колонки выбора нет')
        content = content.replace('PageHeading 88 + ContextBar 56 + Summary 112 + таблица 352', 'PageHeading 76 + ContextBar 48 + Summary 112 + таблица 350').replace('= 888 px', '= 866 px')
    if name == 'Heatmaps':
        content = content.replace('PageHeading — 72 px', 'PageHeading — 76 px').replace('ContextBar — 112 px, два ряда по 48 px', 'ContextBar — 104 px, два ряда по 44 px').replace('DataSummary — 56 px', 'DataSummary — 48 px')
        content = content.replace('Справа переключатель двух режимов:', 'В панели карты над снимком переключатель двух режимов:')
        content = content.replace('PageHeading 72 + ContextBar 112 + DataSummary 56', 'PageHeading 76 + ContextBar 104 + DataSummary 48').replace('= 980 px', '= 968 px')
        content = content.replace('Высота MapPanel: 44 + 536 + 48 = 628 px.', 'MapPanel занимает 628 px; внутри: панель 48 px, снимок 500 px, легенда по содержимому и два промежутка по 16 px.')
    if name == 'Funnel':
        content = content.replace('PageHeading — 72 px', 'PageHeading — 76 px').replace('ContextBar — 56 px', 'ContextBar — 48 px').replace('PageHeading 72 + ContextBar 56', 'PageHeading 76 + ContextBar 48').replace('= 944 px', '= 940 px')
        content = content.replace('Заголовок «Шаги сценария» — 40 px.', 'Заголовок «Шаги сценария» — 26 px, затем промежуток 16 px.')
        content = content.replace('и полоса относительного количества дошедших. Числа остаются читаемыми без визуальной полосы; low-fi не задаёт её оформление.', 'и показатели количества дошедших в соседних колонках. Полоса относительного количества остаётся возможным визуальным дополнением; в этом low-fi показаны числа.')
    if name == 'Replay':
        content = content.replace('интерфейса 490 px, временная шкала 80 px, управление 56 px', 'интерфейса 400 px, временная шкала 72 px, управление 48 px')
    if '## Границы отрисованного состояния' not in content:
        content += '\n## Границы отрисованного состояния\n\nВ Figma отрисовано основное заполненное состояние с демонстрационными данными. Переходы, пустые состояния, загрузка и ошибки описаны здесь как спецификация; отдельных фреймов для них и работающих интеракций в данном пакете нет. Геометрия и фактический набор слоёв воспроизводятся скриптом `execution/build_wireframes.py`.\n'
    path.write_text(content, encoding='utf-8', newline='\n')

links = '\n'.join(f'| {label} | [{name}]({BASE}{node}) | 1920×1080 |' for name, (node, label) in SCREENS.items())
report = f'''# Wireframes: результат отрисовки

Файл Dashboard → страница UX-Lab · Wireframes → секция Wireframes — low-fi.

| Экран | Figma | Размер |
| --- | --- | --- |
{links}

Пять редактируемых low-fi экранов: Inter Regular/Medium, белый фон, серые плейсхолдеры, тёмный текст, Auto Layout. Горизонтальное размещение с промежутком 80 px. Ранее созданные sitemap и user flows находятся на своей странице.

Результаты начинаются с обзора цифр и сценариев. Тепловая карта открывается отдельно; представлены режимы всех кликов и первого клика. Слой интенсивности карты обозначен плейсхолдером. Replay показывает восстановленный интерфейс, шкалу времени и события; это макет проигрывателя, не видеофайл и не действующая запись.

Проверены снимки всех пяти экранов, размеры 1920×1080 и геометрия дочерних слоёв: переполнений не обнаружено. Вложенные контейнеры используют Auto Layout. Данные искусственные; результаты исследования не собирались. Основные состояния отрисованы, дополнительные состояния описаны в Markdown. Интерактивный прототип в объём этой отрисовки не входит.

Способ привязки критериев к событиям/элементам — проектное предложение; D01 не закрыт. Определения первого клика, попыток и сигналов, совместимость состояний интерфейса и правила хранения остаются открытыми согласно PRD. Это не отменяет включённые в MVP функции.

Команда пользователя «на все апрув не спрашивай рисуй варфреймы» разрешила завершить пакет без повторных согласований. Генератор: `execution/build_wireframes.py`. Он подготавливает JS для MCP и защищён от повторного создания экрана с тем же именем; перед изменением существующего экрана требуется прочитать его актуальное состояние.
'''
(FOLDER / 'figma-delivery.md').write_text(report, encoding='utf-8', newline='\n')
path = FOLDER / 'README.md'
content = path.read_text(encoding='utf-8').replace('Отрисовка выполняется', 'Отрисовка завершена')
if '## Готовые экраны' not in content:
    content += '\n## Готовые экраны\n\nВсе пять экранов созданы и проверены. [Ссылки на Figma и отчёт проверки](figma-delivery.md).\n'
path.write_text(content, encoding='utf-8', newline='\n')
print('Recorded five verified Figma frames and synchronized delivery status.')
