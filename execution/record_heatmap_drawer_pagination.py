"""Record the verified context, drawer and compact pagination refinements."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MARK='<!-- heatmap-drawer-pagination-2026-09-23 -->'

def append(path, text):
    p=ROOT/path
    old=p.read_text(encoding='utf-8')
    if MARK not in old:
        p.write_text(old.rstrip()+'\n\n'+MARK+'\n'+text.strip()+'\n',encoding='utf-8')

heat='Контекст и выборка объединены в HeatmapOverview: слева страница, сценарий и параметры снимка, справа число кликов/участников, пояснение к выборке и «Как считается». Панель 1536×114, два столбца с разделителем, без потери исходных значений. Применено к Heatmaps, FirstClick и DynamicState; нижний край содержимого 1062 при высоте экрана 1080.'
pager='Пагинация ParticipantsTable/Ready: компактная группа 156×40 справа под таблицей, две icon-only кнопки со стрелками и обычный текст PageCounter. Области нажатия 40×40; Previous — Disabled на первой странице. Мастер 153:702, Footer 153:1050, группа 294:11750, счётчик 294:11751. В финальных экземплярах сохранены «1 из 4» и «1 из 3». Край группы совпадает с правым краем Footer.'
drawer='Закрытие FindingDetails и FindingEditor заменено icon-only крестиком Elastic cross, по образцу модалок, область 40×40. Все четыре закрытия UX-продукта согласованы; собственный NOVA-крестик тестируемого магазина сохраняется. Действия FindingDetails дополнены библиотечными pencil и document. Для реализации: доступные имена и подсказки «Закрыть панель», «Предыдущая страница», «Следующая страница»; клавиатурное закрытие Escape и возврат фокуса. Макеты не подтверждают реализацию этих интеракций.'
for slug in ['heatmaps','heatmaps-first-click','heatmaps-dynamic-state']:append(f'ds/screens/{slug}.md',heat)
for slug in ['participants','participants-from-heatmap']:append(f'ds/screens/{slug}.md',pager)
for slug in ['finding-details','finding-editor']:append(f'ds/screens/{slug}.md',drawer)
append('ds/patterns.md','## Контекст карты, закрытие панелей и пагинация\n\n'+heat+'\n\n'+pager+'\n\n'+drawer)
append('ds/components.md',pager+'\n\n'+drawer)
append('ds/source.md','Последние правки проверены на странице UX-Lab · Final Screens: группировка контекста трёх тепловых карт, единые крестики модалок/панелей, иконки действий находки, компактная пагинация через мастер ParticipantsTable. Цвета и Text Styles связаны с существующими токенами; число локальных наборов/вариантов не изменилось.')
audit=json.loads((ROOT/'.tmp/heatmap-drawer-pagination-audit.json').read_text(encoding='utf-8'))
assert audit['passed'] and audit['screenCount']==55
record={'date':'2026-09-23','heatmapPanels':['292:10340','293:11737','293:11746'],'closeButtons':['207:6616','210:9628','210:19189','210:19685'],'actionButtons':['210:19254','210:19261'],'icons':{'pencil':'294:10340','document':'153:1809','cross':'106:617'},'pagination':{'master':'153:702','group':'294:11750','counter':'294:11751','width':156,'height':40,'tables':{'210:12295':'1 из 4','210:20553':'1 из 3'},'rightInset':0},'checks':{'fullPackBeforeFinalFooterAlignment':{'passed':True,'screenCount':55},'finalFooterAlignment':'verified on both instances, screenshots reviewed; rotated vector local-coordinate bounds are not treated as frame overflow'},'prototypeWired':False}
(ROOT/'ds/screens/heatmap-drawer-pagination-review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded verified Figma refinements and interaction requirements.')
