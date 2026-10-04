"""Close the authorised, screen-scoped variant review from verified Figma receipts."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DS=ROOT/'ds'
TMP=ROOT/'.tmp/component-variants'
URL='https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def section(p,title,body):
    text=p.read_text(encoding='utf-8') if p.exists() else ''
    if title in text:text=text[:text.index(title)].rstrip()
    p.write_text(text+'\n\n'+title+'\n\n'+body.rstrip()+'\n',encoding='utf-8')

def main():
    source=read(TMP/'bulk-source.json')
    assert len(source)==204 and not any(c.get('missing') for c in source)
    audits=[read(TMP/f'bulk-{n}-audit.json') for n in ['button','nav','tab']]
    assert [len(a['variants']) for a in audits]==[18,8,8]
    assert all(a['passed'] and not a['issues'] for a in audits)
    existing=read(TMP/'bulk-existing-audit.json')
    assert existing['passed'] and [len(c['variants']) for c in existing['report']]==[2,4,3]
    tokens=read(TMP/'bulk-tokens-receipt.json')['tokens']
    extensions={'31735:391399':'ProductButton','14645:214':'ProductNavItem','32617:392183':'ProductTab'}
    screen_terms=['Text field','Textarea','Search field','Select field','Form Control','Checkbox','Radio','Switch','Table','Pagination','Modal','Flyout','Callout','Toast','Badge','Tabs','Filter','Facet','Popover','Panel','Tooltip','Breadcrumb','Steps','Spinner','Progress']
    decisions=[]
    for c in source:
        name=c['name']
        if c['id'] in extensions:
            decision='расширен локально';reason='Недостающие взаимодействия добавлены в '+extensions[c['id']]+', исходный набор сохранён.'
        elif name.startswith('.') or name.startswith('📦') or '💡' in name:
            decision='часть композиции / пример';reason='Используется внутри базового элемента или как пример; отдельная декартова матрица не нужна.'
        elif any(term in name for term in screen_terms):
            decision='переиспользовать';reason='Существующие оси и ячейки покрывают выбранный паттерн экранов; события вложенных контролов не дублируются на контейнере.'
        else:
            decision='без расширения в текущем объёме';reason='Отдельное недостающее состояние этого элемента не следует из текущих экранов; расширение всей библиотеки не является задачей.'
        decisions.append({**c,'decision':decision,'reason':reason})
    for c in existing['report']:
        decisions.append({'id':c['id'],'name':c['name'],'cellCount':len(c['variants']),'decision':'выполнено ранее' if c['name']=='ReplayControls' else 'оставлено по согласованию','reason':'Replay: 2 Coverage × 2 Playback.' if c['name']=='ReplayControls' else 'Не добавлять загрузку/пустоту в легенду и Pending в DataCoverage.'})
    report={'status':'complete','scope':'Screen-scoped bulk review, approved autonomous selection; not a full redesign of Elastic UI','date':'2026-09-22','reviewedOriginalEntries':207,'sourceLiveRead':204,'completed':['ReplayControls','ProductButton','ProductNavItem','ProductTab'],'unchangedByAgreement':['HeatmapLegend','DataCoverage'],'pendingBrief':[],'newVariantCount':34,'totalProductVariantCount':43,'decisions':decisions,'newComponents':audits,'semanticAliases':tokens,'validation':{'bindingsPassed':True,'visualPassed':True,'matricesPassed':True},'limits':['Static Figma states, no event-handling implementation.','Existing low-fi screens were not replaced by final UI.','Original library remains unchanged; selected deprecated version was preserved.']}
    save(DS/'component-variants-audit.json',report)
    counts=Counter(c['decision'] for c in decisions)
    body='# Component variants — выполнено в согласованном объёме\n\n22 сентября 2026. Пользователь согласовал автономное определение состояний для текущих экранов. Прочитаны все 204 исходных элемента в Figma, сверены 3 продуктовых набора и фактически применяемые instances.\n\n'
    body+='## Расширено\n\n| Компонент | Матрица | Результат |\n| --- | --- | --- |\n'
    specs={'ProductButton':'Primary / Secondary / Tertiary × Default / Hover / Pressed / Focus / Disabled / Loading; Small','ProductNavItem':'Selected False / True × Default / Hover / Pressed / Focus','ProductTab':'Selected False / True × Default / Hover / Pressed / Focus; Small'}
    for a in audits:body+=f"| {a['name']} | {specs[a['name']]} | [{len(a['variants'])} вариантов]({URL+a['id'].replace(':','-')}) |\n"
    body+='\nReplayControls ранее расширен до 4 вариантов; HeatmapLegend оставлен с 2, DataCoverage — с 3 по решению пользователя. Всего в продуктовом UI Kit 6 наборов и 43 варианта.\n\n'
    body+='## Почему именно эти изменения\n\nButton применяется в UI Kit и экранах (35 и 88 instances на момент чтения, включая вложенные). У Neutral/Small есть только обычные Empty/Filled/Default ячейки. Наличие Disabled/Loading в общей оси не означает наличие этих комбинаций. Hover, Pressed и Focus добавлены локально вместе с Disabled и Loading.\n\nSide Nav Item нужен общей боковой навигации, Tab — вкладкам сигналов/находок. Selected сохранён отдельной осью, Focus не снимает выделение. Расширения — оболочки с вложенными instances исходной библиотеки; отсоединения не выполнялись.\n\nText field, Textarea, Search и Select уже содержат Focus/Invalid/Disabled. Checkbox и Radio содержат выбор/фокус/блокировку, Table Cell — Hover/Selected/Disabled, Header — сортировку, Pagination — состояния внутренних кнопок. Загрузка результата, ошибка сервера и пустая выборка относятся к контейнеру/SharedPatterns, не к каждой легенде или строке.\n\n'
    body+='## Проверка и границы\n\nПроверены все 34 новые ячейки: уникальность матрицы, сохранение instances, размеры, отсутствие выхода ячеек за набор, привязки fills/strokes, Text Styles, положительных Auto Layout отступов и радиусов. Все три матрицы просмотрены на снимках. Исходные 9 продуктовых вариантов повторно прошли аудит. Это состояния макетов, не работающий проигрыватель и не кликабельный прототип. Перевод всех low-fi экранов в финальный UI не выполнялся.\n\n'
    body+='Созданы 5 semantic aliases на существующую палитру; новых hex нет. Исходная Elastic UI сохранена. Названия и Deprecated-маркеры исходных элементов не менялись.\n\n## Решения по всему каталогу\n\n'
    body+='; '.join(f'{k}: {v}' for k,v in counts.items())+'.\n\n| Элемент | ID | Ячеек | Решение | Основание |\n| --- | --- | --- | --- | --- |\n'
    for c in decisions:body+=f"| {c['name']} | `{c['id']}` | {c['cellCount']} | {c['decision']} | {c['reason']} |\n"
    (DS/'component-variants-audit.md').write_text(body,encoding='utf-8')
    catalog=[]
    for a in audits:
        catalog.append(f"### {a['name']}\n\n- **Назначение:** локальное расширение взаимодействий существующего {'Button' if a['name']=='ProductButton' else 'Side Nav Item' if a['name']=='ProductNavItem' else 'Tab'} Elastic UI; вложенный instance сохраняется.\n- **Варианты:** {specs[a['name']]}. Всего {len(a['variants'])}.\n- **Node ID:** `{a['id']}` · [Figma]({URL+a['id'].replace(':','-')}) · COMPONENT_SET\n- **Привязки и проверка:** смысловые Variables, размеры/радиусы Dimensions, импортированные Text Styles. Аудит и визуальная проверка пройдены. Свойства вложенного Control открыты через exposed instance; текст редактируется в нём.\n")
    section(DS/'components.md','## Расширения состояний по текущим экранам','\n'.join(catalog)+'\nПолный разбор 207 исходных записей: [component-variants-audit.md](component-variants-audit.md). Основная библиотека не изменялась. Новые 3 набора увеличивают каталог до 210 записей.')
    foundation='Пять semantic aliases ссылаются на существующие базовые цвета продукта. Новые цветовые значения не создавались.\n\n| Token | Alias | Figma ID |\n| --- | --- | --- |\n'
    for t in tokens:foundation+=f"| {t['name']} | {t['target']} | `{t['id']}` |\n"
    foundation+='\nFocus — отдельная обводка 2 px, не цвет ошибки; Selected обозначен поверхностью и полосой/подчёркиванием. Disabled — opacity 0.4. Размеры контролов сохранены между состояниями.\n'
    section(DS/'foundation.md','## Состояния взаимодействий — 22 сентября 2026',foundation)
    index=read(DS/'index.json')
    ext=index['productExtensions']
    records=[{k:a[k] for k in ['name','id','properties','variants']}|{'type':'COMPONENT_SET','issues':[]} for a in audits]
    ext['components']=[c for c in ext['components'] if c['name'] not in specs]+records
    ext['variantCount']=43;ext['interactionAliases']=tokens;index['componentVariantsReview']={'status':'complete','report':'ds/component-variants-audit.md','sourceLiveRead':204}
    save(DS/'index.json',index)
    state=read(DS/'grow-ui-kit-status.json');state['createdComponents']=[c for c in state['createdComponents'] if c['name'] not in specs]+records;state['componentCount']=6;state['variantCount']=43;state['interactionAliases']=tokens;state['componentVariantsReview']='complete';save(DS/'grow-ui-kit-status.json',state)
    merged={**existing,'report':existing['report']+audits,'semanticAliases':tokens,'passed':True};save(DS/'grow-ui-kit-audit.json',merged)
    section(DS/'grow-ui-kit-status.md','## Component variants — завершено','Добавлены ProductButton (18), ProductNavItem (8), ProductTab (8). Вместе с HeatmapLegend (2), ReplayControls (4), DataCoverage (3): **6 наборов, 43 варианта**. Все привязки и снимки проверены. [Матрицы в Figma]('+URL+'125-308). [Разбор каталога](component-variants-audit.md).\n\nСкрипты: build_interaction_variants.py, audit_interaction_variants.py, finalize_component_variants.py. Ранние генераторы описывают прежний пакет; перед повторной записью читать текущий канвас.')
    section(DS/'patterns.md','## Локальные расширения Elastic UI','ProductButton, ProductNavItem и ProductTab сохраняют библиотечные instances внутри локальных ComponentSet. Использовать при сборке финальных экранов, когда нужны состояния указателя и клавиатурный фокус в палитре продукта. Навигация остаётся одним уровнем; новые разделы продукта не добавляются. Геометрия наружной рамки Focus отделена от области основного контрола. [Каталог](components.md).')
    print(json.dumps({'status':'complete','reviewed':207,'catalogEntries':210,'productSets':6,'productVariants':43,'newVariants':34,'decisions':counts},ensure_ascii=False))

if __name__=='__main__':main()
