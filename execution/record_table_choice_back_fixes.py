"""Record the final approved direction of the table and navigation refinements."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
marker='<!-- table-choice-back-refinements-2026-09-23 -->'
groups=[
 (['success-criteria','criteria-u-r-l','criteria-button'], 'Тип критерия представлен тремя связанными TaskChoiceCard с Radio и краткими пояснениями. Выбранный вариант обозначен оливковым контуром, маркером и подписью «Выбрано». Группы: 210:8131, 210:9927, 210:10262. Это выбор одного значения, а не три действия. Экспорт SuccessCriteria проверен; логика смены экранов этим изменением не добавлена.'),
 (['results-overview'], 'По уточнению пользователя удалена вложенная рамка TableGrid. В ScenarioTable восстановлено прежнее расположение Title / TableHeader / ScenarioRows / DenominatorNote. Остались общий внешний border/subtle 1 px, shadow/card, более заметная шапка background/sidebar и два горизонтальных разделителя строк. Исправлены Ready, OverviewUnselected и OverviewSelected. Итоговый экспорт экземпляра 175:2683 проверен. Не запускать только refine_scenario_table_surface.py: окончательное уточнение применяется через flatten_scenario_table_surface.py.'),
 (['projects-default','projects'], 'ProjectsTable имеет общий border/subtle 1 px, горизонтальные разделители и shadow/card (исходный стиль: y=2, blur=8, непрозрачность 4%). Чередование фона сохранено. Контейнеры 203:7354 и 207:6525; экспорт первого проверен.'),
 (['heatmaps','heatmaps-first-click','heatmaps-dynamic-state'], 'К текстовой ссылке «К обзору результатов» добавлен связанный библиотечный arrowLeft (95:4), визуально шеврон влево. Заливки нет, цвет accent/strong. Смысл перехода — обзор текущего исследования с сохранением контекста сценария и фильтров. Переходы прототипа и сохранение состояния этим изменением не реализованы. Экспорт HeadingText 205:6728 проверен.'),
]
for names,note in groups:
 for name in names:
  path=root/'ds/screens'/f'{name}.md'
  text=path.read_text(encoding='utf-8')
  if marker not in text:path.write_text(text.rstrip()+'\n\n'+marker+'\n'+note+'\n',encoding='utf-8')
receipt={'scenarioTable':{'set':'136:715','instance':'175:2683','nestedFrameRemoved':True,'rowDividers':True,'shadow':'shadow/card'},'projectTables':['203:7354','207:6525'],'criterionGroups':['210:8131','210:9927','210:10262'],'backLinks':['354:10762','354:10765','354:10768'],'screenshotsReviewed':['210:8131','210:7862','175:2683','172:1877','203:7354','205:6728'],'reactSynchronized':False}
(root/'ds/screens/table-choice-back-fixes.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded final Figma refinements; React sync remains separate.')
