"""Record the verified table, timeline, comparison, and alignment refinements."""
import json
from pathlib import Path
from record_final_pack import append_once, read, write

ROOT=Path(__file__).resolve().parents[1]
DS=ROOT/'ds'
data=read(ROOT/'.tmp/final-pack/refinements.json')
check=read(ROOT/'.tmp/final-pack/project-count-check.json')
assert data['audit']['passed'] and check['passed']
assert not data['registry']['comparison']['issues']
index=read(DS/'index.json')
for update in data['registry']['components']:
    component=next(c for c in index['productExtensions']['components'] if c['id']==update['id'])
    component.update(update)
index['productExtensions']['secondaryContrastComparison']={'id':'237:11659','status':'comparison only; not applied to product masters','options':['gray fill and outline','outline only','olive fill and outline']}
write(DS/'index.json',index)
status=read(DS/'grow-ui-kit-status.json')
status['createdComponents']=index['productExtensions']['components']
write(DS/'grow-ui-kit-status.json',status)
audit=data['audit']
audit['visuallyReviewedScreens']=read(DS/'screens/final-pack-audit.json').get('visuallyReviewedScreens',[])
audit['postChecks']={'projectCountAlignment':check,'comparison':data['registry']['comparison']}
write(DS/'screens/final-pack-audit.json',audit)
write(DS/'screens/refinements-audit.json',data|{'projectCountAlignment':check})
append_once(DS/'components.md','<!-- review-refinements-2026-09-23 -->','''
## Уточнения после просмотра экранов · 23 сентября 2026

- ResearchTableRow: боковые отступы содержимого всех 28 вариантов — 16 px, через существующую переменную Dimensions. У 12 таблиц строка примыкает к следующей. ControlChecklist, ParticipantTasks, ExploredPages, PageEvents получили radius/surface=12 и clipping.
- ParticipantsTable: во всех 5 состояниях TableHeader и ParticipantRows/StateMessage объединены в TableSurface с radius/surface=12 и тонким контуром border/subtle. Заголовок background/sidebar, строки примыкают; у отдельных строк radius=0, высота 80 px, тонкий нижний разделитель. Иконки участников без белых подложек. Общая высота компонента HUG.
- ReplayControls: позиции маркеров и подписей масштабируются через отдельные абсолютные якоря. Круги сохраняют 16×16 px, линия ползунка — 2 px. Подписи времени сохраняют ширину 60 px; крайние закреплены слева/справа. Все четыре варианта исправлены; проверены узкие экземпляры 1124.5 px, последний таймкод 04:32 виден полностью.
- Счётчик проектов выровнен с центром внутреннего поля поиска, без учёта Label. ProjectsDefault и фон модального Projects исправлены; ошибка центра 0 px.

[Отдельная примерка Secondary](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=237-11659): A — серый фон и контур; B — прозрачный фон и контур; C — оливковый фон и контур. По 3 подложки на вариант, 9 связанных экземпляров ProductButton. Это предложения; утверждённые мастера кнопок не изменены. Цвета взяты из существующих токенов для сравнения; финальное семантическое соответствие выбирается после решения пользователя.
''')
append_once(ROOT/'directives/directive_final_screens.md','<!-- table-marker-refinements-2026-09-23 -->','''
### Геометрия таблиц и временной шкалы

Скруглять общий контейнер таблицы и включать clipping; отдельным строкам radius=0, gap=0. Заголовок и строки должны быть внутри одного TableSurface. Для ячеек использовать горизонтальный padding 16 px.
Не применять SCALE непосредственно к кругам, линии playhead или текстам таймкодов. Масштабировать якорь положения; дочерние маркеры и текст сохраняют фиксированную геометрию. В Auto Layout якорь должен иметь layoutPositioning=ABSOLUTE, иначе все маркеры складываются в поток.
Счётчик рядом с полем выравнивать по высоте Control, а не по полному полю вместе с Label. Скрипты: refine_table_surfaces.py, unify_participants_table.py, fix_replay_marker_scaling.py, align_project_count.py. Примерка Secondary: compare_secondary_contrast.py, отдельно от финальных экранов.
''')
append_once(DS/'screens/control-result.md','<!-- table-surface-refinement -->','Таблица ControlChecklist: единый контур со скруглением 12 px, clipping; ячейки с боковыми отступами 16 px, строки без зазоров.')
for name in ['participants','participants-from-heatmap']:
    append_once(DS/f'screens/{name}.md','<!-- participant-table-refinement -->','ParticipantsTable обновлён через мастер: единый TableSurface для заголовка и строк, радиус 12 px, контур, тонкие горизонтальные разделители и зебра; строки 80 px без отдельных скруглений.')
for name in ['projects-default','projects']:
    append_once(DS/f'screens/{name}.md','<!-- search-count-alignment -->','Счётчик «3 проекта · доступ у обоих коллег» выровнен по вертикальному центру Control поля поиска; Label поля в выравнивании не участвует.')
print('Recorded table surfaces, replay geometry, 9 comparison samples, and search-count alignment.')
