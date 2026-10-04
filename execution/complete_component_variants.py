"""Reproducible scope, payload generation and records for the authorised bulk review."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'.tmp/component-variants'
DS=ROOT/'ds'

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def source_code(offset=0):
    ids=[c['id'] for c in read(DS/'index.json')['components']][offset:offset+35]
    return "await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('23678:450'));const rows=[];for(const id of "+json.dumps(ids)+"){const n=await figma.getNodeByIdAsync(id);if(!n){rows.push({id,missing:true});continue;} rows.push({id:n.id,name:n.name,key:n.key,type:n.type,axes:Object.fromEntries(Object.entries(n.componentPropertyDefinitions).filter(([k,v])=>v.type==='VARIANT').map(([k,v])=>[k,v.variantOptions])),cellCount:n.type==='COMPONENT_SET'?n.children.length:1});}return rows;"

def brief():
    text='''# Component variants — согласованный автономный прогон

Разрешение: пользователь согласился с предложением определять и добавлять необходимые состояния без отдельных подтверждений, затем повторил «делайц».

HeatmapLegend: оставить Mode AllClicks/FirstClick. DataCoverage: оставить Complete/Partial/Unavailable. ReplayControls: ранее выполненные 4 ячейки сохранить.

Проверка Button показала Disabled/Loading в общей библиотеке, но у Neutral/Small нет соответствующих ячеек; Hover/Focus/Pressed отсутствуют. Навигации и вкладкам недостаёт состояний указателя и клавиатурного фокуса. Расширения делаются локальными оболочками с вложенными instances исходной Elastic UI; исходный файл и существующие экраны не заменяются.

| Расширение | Матрица | Ячеек | Применение |
| --- | --- | --- | --- |
| ProductButton | Kind Primary/Secondary/Tertiary × State Default/Hover/Pressed/Focus/Disabled/Loading | 18 | Создать, сохранить, повторить, экспорт, вторичные действия; Small 32 px как у применяемой основы |
| ProductNavItem | Selected False/True × State Default/Hover/Pressed/Focus | 8 | Боковая навигация всех экранов, один уровень и существующая ширина панели |
| ProductTab | Selected False/True × State Default/Hover/Pressed/Focus | 8 | Вкладки сигналов и находок, режимы анализа; Disabled остаётся в исходной библиотеке |

Кнопка: Default — обычное действие; Hover — изменение поверхности; Pressed — усиление выбранной поверхности; Focus — наружная рамка с сохранением базовой заливки; Disabled — недоступное действие, не Loading; Loading — неподвижный индикатор и текст «Загрузка…», без изменения размера. Это макеты состояний, не работающая логика.

Навигация и вкладка: Selected независимо от Focus; выбранное положение не пропадает при клавиатурном фокусе. Фиксированные геометрия и размеры во всех состояниях. Иконки и подписи берутся из исходного компонента.

Новые semantic-имена alias на существующую палитру: action/hover → text/primary; action/pressed → text/secondary; surface/hover → background/sidebar; surface/pressed → accent/soft; border/focus → accent/strong. Новых hex и размеров палитры нет. Focus обозначается рамкой, selected — фоном/подчёркиванием.

Один ComponentSet за write-вызов. Проверить количество ячеек, вложенные instances, заливки/обводки/типографику/отступы, изображения и отсутствие наложений. Поля, выбор, сортировка и статические контейнеры переиспользуют уже имеющиеся состояния; глубокая модернизация всей Elastic UI не входит в этот прогон.
'''
    (DS/'.tmp/component_variants_bulk.md').write_text(text,encoding='utf-8')
    return {'brief':'ds/.tmp/component_variants_bulk.md','additions':{'ProductButton':18,'ProductNavItem':8,'ProductTab':8}}

if __name__=='__main__':
    TMP.mkdir(parents=True,exist_ok=True)
    if sys.argv[1]=='source': print(json.dumps({'code':source_code(int(sys.argv[2]) if len(sys.argv)>2 else 0)}))
    elif sys.argv[1]=='brief': print(json.dumps(brief(),ensure_ascii=False))
