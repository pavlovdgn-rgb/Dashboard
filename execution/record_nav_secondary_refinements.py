"""Save verified menu spacing, contrast and surface proposals without applying a choice."""
import json
from pathlib import Path
from check_scenario_row_contrast import contrast
ROOT=Path(__file__).resolve().parents[1]
ds=ROOT/'ds'
result={'navMenu':{'id':'153:2777','variants':10,'paddingInline':12,'iconGap':8,'iconWidth':20,'menuWidth':320,'text':'#626E32','selectedBackground':'#ECEEDC','contrast':contrast('#626E32','#ECEEDC'),'geometryIssues':0},'dropdownButtons':{'scope':'UX-Lab · UI Kit','replacedFilterControls':10,'textArrowCharactersRemaining':0,'icon':'arrowDown'},'secondaryProposals':{'boardId':'164:1681','status':'awaiting user selection','options':{'A':{'id':'164:1685','background':'border/subtle'},'B':{'id':'164:1746','background':'background/sidebar','border':'border/control'},'C':{'id':'164:1803','background':'accent/soft','border':'accent/strong'}},'recommended':'B','appliedToMasters':False}}
(ds/'nav-secondary-refinements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ds/'participants-navigation.md'
text=path.read_text(encoding='utf-8')
heading='## Уточнение отступов, шевронов и подложек'
addition='''## Уточнение отступов, шевронов и подложек

NavMenu: внутренние боковые отступы всех строк — 12 px (Dimensions/md), расстояние до иконки — 8 px. Вложенный контрол занимает оставшуюся ширину; минимальная ширина снята через null. Текст #626E32 на фоне #ECEEDC: 4,6973:1, соответствует минимуму 4,5:1 для обычного текста. Проверены все 10 вариантов, переполнений нет.

Во всех 10 кнопках фильтров ParticipantsTable текстовый треугольник заменён на instance arrowDown. В UI Kit не осталось текстовых треугольников раскрытия. «Выбрать попытку» содержит layers + arrowDown.

[Три предложения подложек Secondary](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=164-1681): A — плотный серый; B — серый с контуром (рекомендация); C — оливковый с контуром. Сравнение на белой, светлой и активной оливковой поверхности. Варианты представлены как локальные overrides связанных instances; ни один не применён к мастерам.

Воспроизводимые правки: fix_nav_menu_padding.py, replace_dropdown_text_arrows.py, propose_secondary_surfaces.py. Учтённое ограничение API: minWidth=0 недопустим, для снятия минимума используется null.
'''
if heading in text:text=text.split(heading)[0].rstrip()+'\n\n'+addition
else:text=text.rstrip()+'\n\n'+addition
path.write_text(text,encoding='utf-8')
idxpath=ds/'index.json';idx=json.loads(idxpath.read_text(encoding='utf-8'))
idx['productExtensions']['navSecondaryRefinements']='ds/nav-secondary-refinements.json'
idxpath.write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
