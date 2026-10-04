"""Record verified toolbar alignment and contextual control fixes."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MARK='<!-- toolbar-controls-review-2026-09-23 -->'
def append(path, text):
    p=ROOT/path;old=p.read_text(encoding='utf-8')
    if MARK not in old:p.write_text(old.rstrip()+'\n\n'+MARK+'\n'+text+'\n',encoding='utf-8')
toolbar='ParticipantsTable: Toolbar=FILL во всех 5 состояниях. Счётчик слева; SearchAndFilters справа: поиск 360×40, два фильтра 168×40, внутренние интервалы 16/8 px. В обоих финальных экземплярах Toolbar и TableSurface имеют одинаковую ширину 1486 px и левый край. Номера страниц 1 из 4 / 1 из 3 сохранены. У пагинации очищены скрытые старые Text-свойства Назад/Далее и явно закреплены Icon only=True, наружный размер 40×40 и Control 32×32 в мастере и экземплярах. Сообщённое пользователем наложение не воспроизвелось в экспорте; после очистки скриншоты и геометрия обоих экземпляров проверены.'
play='ReplayControls: убраны заливки и обводки контейнеров иконок Play/Pause в четырёх вариантах и четырёх финальных экземплярах. Белые glyph и оливковая кнопка сохранены; визуально проверена Пауза 118:120.'
coverage='DataCoverage 86:370: в Complete и Partial действие Посмотреть данные использует библиотечный Style=Empty, без заливки, подчёркнутый текст и arrowRight. Цвет действия связан со status/success/text или status/warning/text. На нейтральном Unavailable сохранена Secondary. Это контекстный паттерн для цветных плашек; общее решение по Tertiary на белом фоне остаётся отдельным. Обновлены два мастера; применённых DataCoverage-инстансов на Final Screens при проверке не обнаружено. Снимок трёх вариантов проверен.'
for slug in ['participants','participants-from-heatmap']:append('ds/screens/'+slug+'.md',toolbar)
append('ds/components.md',toolbar+'\n\n'+play+'\n\n'+coverage)
append('ds/patterns.md',coverage)
append('ds/source.md','Проверены уточнения: верхняя панель ParticipantsTable по ширине таблицы, явные icon-only настройки пагинатора, прозрачные контейнеры иконок Play/Pause, контекстные текстовые действия на цветных DataCoverage. Подробности — ds/components.md. Число наборов и вариантов не изменилось.')
append('directives/directive_component_variants.md','Техническая проверка после правок: minWidth/minHeight нельзя переопределять на INSTANCE — API отклоняет min-size. Для экземпляра применять resize и layoutSizing, ограничения менять только в мастере при необходимости. При замене текстовой кнопки на icon-only проверять также Text-свойство и экземпляры после изменений вложенности; сохранять доступное имя в спецификации. У контейнера иконки fills/strokes должны оставаться пустыми, тематизируется сам glyph, иначе на цветной кнопке появляется квадратная подложка.')
receipt=json.loads((ROOT/'.tmp/toolbar-controls-receipts.json').read_text(encoding='utf-8'))
(ROOT/'ds/screens/toolbar-controls-review.json').write_text(json.dumps({'date':'2026-09-23','receipts':receipt,'verification':{'tables':['210:12295','210:20553'],'toolbarWidth':1486,'pagerWidth':156,'controlsHeight':40,'visibleOverflow':[],'screenshots':['210:12295','210:20553','118:120','86:370']},'prototypeWired':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded toolbar, pagination, playback and tinted status actions.')
