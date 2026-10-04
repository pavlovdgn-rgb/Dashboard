# Аналитические компоненты

| Компонент | Вариантов |
| --- | ---: |
| [SuccessMetric](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=132-574) | 3 |
| [FirstClickTargetRow](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=132-634) | 6 |
| [FirstClickTargets](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=135-778) | 5 |
| [ScenarioRow](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=135-1062) | 6 |
| [ScenarioTable](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=136-715) | 7 |

## Выбор сценария без дублирования · 24 сентября 2026

По указанию пользователя из всех 6 вариантов ScenarioRow и 7 состояний ScenarioTable удалены RowAction и заголовок «Действие». Остались 5 столбцов; освободившееся место занимает название сценария. В Figma проверено наследование всех 7 экземпляров таблицы на финальных экранах, включая скрытые состояния: 5 заголовков, 0 оставшихся RowAction/Header5.

React, Storybook и ResultsOverview используют те же пять столбцов. Выбор работает нажатием на строку, радиокнопкой и стрелками клавиатуры; выбранная строка сохраняет accent/soft. Пустые состояния занимают colspan=5. Повторяемая правка Figma: `execution/remove_scenario_action_column.py`.

Все пять наборов прошли проверку геометрии, цветов, текстовых стилей и отношений ширины полос к долям 14/18, 12/17, 10/15. Числа демонстрационные. Режимы ширины в коллекции Demo data относятся к данным примера, а не к палитре. Семантика единицы первого клика требует отдельного продуктового определения. Последние правила счётчиков и кнопок — в participants-navigation.md.

## Сверка React · 24 сентября 2026

FirstClickTargetRow повторно прочитан из Figma `132:634`, все шесть вариантов. Это самостоятельная выбираемая строка со скруглением `radius/small=4`, а не прямоугольная строка большой таблицы. Высота 88, padding 16, gap 12; иконка bullseye 20×20. Заголовок и счётчик — Inter Medium 16/24, описание — Regular 14/24, доля — Regular 16/24 и text/secondary. Счётчик и доля выровнены вправо в колонках 36/60 с gap 8.

Default без выбора белый, Hover — surface/hover, выбранные варианты — accent/soft. Focus — внутренний контур border/focus 2 px, без внешнего отступа. Нижнего разделителя нет. React приведён к этим исходным значениям; Figma не изменялась. Проверка `execution/check_rows_and_dropdowns.mjs` проверяет шесть состояний, геометрию и выбор клавиатурой.
