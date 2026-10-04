"""Synchronize verified audit repairs and logo usage with the local DS registry."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
receipt=json.loads((ROOT/'.tmp/audit-logo-fix-receipt.json').read_text(encoding='utf8'))
assert all(not item['issues'] for item in receipt['legacyFit'])
assert all(len(s['logos'])==1 and s['oldIcons']==0 and s['overflow']==0 for p in receipt['sidebarVerification'] for s in p['sidebars'])
for group in receipt['verification']['tabs']:
    assert sum(c['selected']=='True' for c in group['children'])==1
    assert all(c['w']==180 and c['h']==40 and c['y']==0 for c in group['children'])
assert all(not x['overflows'] and x['emptyVisible']==0 for x in receipt['verification']['geometry'])

def slug(name):return re.sub(r'(?<!^)(?=[A-Z])','-',name.removeprefix('Screen/')).lower()
def append_once(path,marker,body):
    text=path.read_text(encoding='utf8')
    if marker not in text:path.write_text(text.rstrip()+'\n\n'+marker+'\n'+body+'\n',encoding='utf8')

ds=ROOT/'ds';ip=ds/'index.json';idx=json.loads(ip.read_text(encoding='utf8'));components=idx['productExtensions']['components']
used={u['id']:u for u in receipt['verification']['usage']}
for c in components:
    if c['id'] in used:c['usedIn']=sorted('screens/'+slug(s['name']) for s in used[c['id']]['screens'])
logo={'id':'289:13519','name':'Logo','type':'COMPONENT','width':24,'height':24,'usedIn':sorted('screens/'+slug(s['name']) for s in used['289:13519']['screens']), 'source':'User supplied logo; linked instances inside all 10 NavMenu variants', 'colorVariable':'VariableID:67:115','sidebarUsage':{'finalScreens':43,'wireframes':43,'palettePreview':1,'masters':10}}
existing=next((c for c in components if c['id']==logo['id']),None)
if existing:existing.update(logo)
else:components.append(logo)
idx['productExtensions']['auditLogoFixes']='ds/screens/audit-logo-fixes.json'
ip.write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

cp=ds/'components.md';text=cp.read_text(encoding='utf8')
for name,cid in [('ProductTab','128:1055'),('ProductField','203:4474')]:
    c=next(c for c in components if c['id']==cid)
    text=re.sub(r'^- \*\*'+name+r'\*\* `'+re.escape(cid)+r'`:.*$', '- **'+name+'** `'+cid+'`: '+', '.join(c['usedIn'])+'.',text,flags=re.M)
cp.write_text(text,encoding='utf8')
append_once(cp,'<!-- audit-logo-fixes-2026-09-23 -->','''## Исправления аудита и новый логотип

По разрешению пользователя исправлены S1 и D1/D2/D3. ProductTab: 12 экземпляров на 6 экранах; Signals и FindingsEmpty используют ту же прозрачную вкладку с выбранным состоянием. ProductCheckbox usedIn=screens/report (7 экземпляров). У ProductField удалена устаревшая ссылка screens/launch-active. Предыдущие записи выше отражают историю, актуальная сводка использования обновлена.

Logo `289:13519` — предоставленный пользователем одиночный компонент 24×24. Белый вектор связан с text/inverse; исходный рисунок сохранён. Внутри ProductMark 32×32 используется связанный Logo, как в пользовательском образце. Обновлены все 10 вариантов NavMenu; на Final Screens новый знак присутствует во всех 43 сайдбарах. Добавлен также в 43 сайдбара wireframes и 1 palette preview; в узких меню ProductName=FILL. Всего 87 экранных сайдбаров + 10 мастеров, без старой иконки и переполнений Brand.

Итог каталога продукта: 22 набора / 168 вариантов и 1 отдельно зарегистрированный Logo. У девяти SummaryMetric скрыт пустой Detail; рамка Demo click layer 210:15000 уменьшена до 408 px без изменения позиций пятен. Новые сценарии загрузки/ошибок из аудита не отрисовывались. [Проверка](screens/audit-logo-fixes.json).''')
append_once(ds/'foundation.md','<!-- logo-token-2026-09-23 -->','## Логотип\n\nПользовательский Logo 289:13519: вектор связан с существующим text/inverse (VariableID:67:115), цвет визуально сохранён. ProductMark использует существующий фон action/primary. Новые цветовые значения не создавались.')

for s in used['289:13519']['screens']:
    path=ds/'screens'/(slug(s['name'])+'.md')
    assert path.exists(),path
    body='Сайдбар NavMenu наследует пользовательский Logo `289:13519` (24×24 внутри ProductMark 32×32); старый знак заменён в мастере, связь компонента сохранена.'
    if s['name'] in ['Screen/Signals','Screen/FindingsEmpty']:
        body+=' Вкладки Сигналы / Находки заменены на ProductTab 180×40, с явно выбранной текущей вкладкой.'
        t=path.read_text(encoding='utf8')
        t=re.sub(r'(Фактически использованные локальные наборы: [^\n.]+)(\.)',lambda m:m[1]+(', ProductTab' if 'ProductTab' not in m[1] else '')+m[2],t)
        path.write_text(t,encoding='utf8')
    if s['name'] in ['Screen/Funnel','Screen/ParticipantDetails','Screen/ResultsFree']:body+=' У трёх SummaryMetric пустой слой Detail скрыт; полезные подписи сохранены.'
    if s['name']=='Screen/HeatmapsDynamicState':body+=' Техническая рамка слоя кликов приведена к высоте внутренней области; позиции пятен сохранены.'
    append_once(path,'<!-- audit-logo-fixes-2026-09-23 -->','## Исправления после аудита\n\n'+body)

(ds/'screens/audit-logo-fixes.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
report=ROOT/'.tmp/screens_audit_2026-09-23_fixes.md'
report.write_text('''# Исправления после аудита · 23 сентября 2026

Разрешение пользователя: «делай фикс где считаешь нужным и добавь новый лого везде в сайдбар».

- S1 исправлено: 4 экземпляра ProductTab в Signals / FindingsEmpty. Теперь 12 вкладок на 6 экранах, в каждой группе ровно одна выбрана.
- D1/D2/D3 исправлено: ProductTab, ProductCheckbox, ProductField — реестр сверён с Figma.
- Logo 289:13519: 10 мастеров меню и все 87 экранных сайдбаров (43 Final, 43 Wireframes, 1 Palette preview). У всех один связанный логотип, старых иконок в Brand нет; размеры/ширина проверены.
- Скрыты 9 пустых Detail в SummaryMetric. Уточнена высота технической рамки слоя кликов, пятна сохранены.
- Скриншотами проверены финальный сайдбар, узкий Brand и обе исправленные группы вкладок.
- Декор Resize Handle (C1/C2) оставлен: безопасного существующего токена для фаски нет. Неиспользуемые компоненты не удалены.
- Раздел 6 исходного аудита — бриф новых состояний — остаётся отдельной работой; этот фикс не заявляет их готовность.

Исходный аудит сохранён отдельно. Полные IDs изменений и проверки: ds/screens/audit-logo-fixes.json. Исполняемый сборщик: execution/apply_audit_logo_fixes.py.
''',encoding='utf8')
print(json.dumps({'updatedScreens':len(used['289:13519']['screens']),'sidebarCount':87,'masters':10,'tabCount':used['128:1055']['count'],'report':str(report)},ensure_ascii=False))
