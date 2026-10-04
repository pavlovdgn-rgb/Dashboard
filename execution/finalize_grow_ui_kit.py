"""Record verified Figma components without rewriting the source library scan."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def section(path,marker,content):
    text=path.read_text(encoding='utf-8')
    text=text.split(marker)[0].rstrip()+'\n\n'+marker+'\n\n'+content.rstrip()+'\n'
    path.write_text(text,encoding='utf-8')

def main():
    audit=json.loads((ROOT/'.tmp/grow-ui-kit/live-audit.json').read_text(encoding='utf-8'))
    assert audit['passed'] and all(not r['issues'] for r in audit['report'])
    assert {r['name']:len(r['variants']) for r in audit['report']}=={'HeatmapLegend':2,'ReplayControls':2,'DataCoverage':3}
    url=f"https://www.figma.com/design/{audit['fileKey']}/Dashboard?node-id="
    descriptions={
        'HeatmapLegend':'Легенда интенсивности кликов с режимом, базой выборки и пояснением единицы отсчёта.',
        'ReplayControls':'Управление записью сессии: время, воспроизведение, скорость, вписать и обозначение разрывов.',
        'DataCoverage':'Полнота данных участника: полные, неполные и недоступная запись; отдельно от успеха задания.',
    }
    records=[]
    paragraphs=['Дополнения созданы 22 сентября 2026 в **Dashboard**, файл `'+audit['fileKey']+'`. Это слой продукта поверх исходных 204 элементов Elastic UI. [UI Kit — extended]('+url+'82-45). Все три — COMPONENT_SET, всего семь вариантов.']
    for r in audit['report']:
        variants='; '.join(v['name'] for v in r['variants'])
        paragraphs.append(f"### {r['name']}\n\n- **Назначение:** {descriptions[r['name']]}\n- **Варианты:** {variants}\n- **Node ID:** `{r['id']}` · [Figma]({url+r['id'].replace(':','-')}) · COMPONENT_SET\n- **Привязки:** импортированные Text Styles Elastic UI, Variables размеров и радиусов; смысловые цвета продукта.\n- **Аудит:** пройден; raw SOLID без привязки, непривязанных положительных padding/gap/radius и текстов без стиля не обнаружено.")
        records.append({k:r[k] for k in ('name','id','type','variants','properties')})
    paragraphs.append('DataCoverage: редактируемые DetailTextComplete / DetailTextPartial / DetailTextUnavailable разделены по состояниям, чтобы текст одного варианта не заменял остальные. ShowAction управляет видимостью; ActionLabel раскрывает текстовое свойство вложенного Button. Кнопки остаются instances, не detached.')
    paragraphs.append('Границы: минимальные варианты, без полной матрицы hover/focus/disabled/loading и без реализации плеера. Основной Button исходной версии имеет Deprecated-маркер; версия Borealis не подменялась. Служебная .Button Group / Button всё ещё не опубликована; для расширения она не требуется. Числа в примерах демонстрационные.')
    section(ROOT/'ds/components.md','## Дополнения продукта — Данные и управление анализом','\n\n'.join(paragraphs))
    index=json.loads((ROOT/'ds/index.json').read_text(encoding='utf-8'))
    index['productExtensions']={'fileKey':audit['fileKey'],'pageId':audit['pageId'],'sectionId':audit['sectionId'],'foundationId':audit['foundationId'],'components':records,'heatmapVariables':audit['heatmapVariables'],'auditPassed':True,'date':audit['date']}
    dump(ROOT/'ds/index.json',index)
    dump(ROOT/'ds/grow-ui-kit-audit.json',audit)
    status={'status':'complete','approved':list(descriptions),'sourceFileKey':index['fileKey'],'targetFileKey':audit['fileKey'],'libraryConnected':True,'componentCount':3,'variantCount':7,'sectionId':audit['sectionId'],'foundationId':audit['foundationId'],'createdComponents':records,'auditPassed':True,'completed':audit['date'],'remainingScope':'Full interactive state matrix and final screen assembly are separate tasks.'}
    dump(ROOT/'ds/grow-ui-kit-status.json',status)
    (ROOT/'ds/grow-ui-kit-status.md').write_text('# UI Kit extension — выполнено\n\nElastic UI (Copy) подключена к Dashboard. Импорт основных компонентов, существующих Text Styles и Variables подтверждён. Служебная .Button Group / Button не опубликована; вместо неё использован основной Button той же версии.\n\n[Открыть UI Kit — extended]('+url+'82-45) · [Foundation]('+url+'82-15).\n\n'+ '\n'.join(f"- **{r['name']}** — {len(r['variants'])} варианта, аудит ✓, [Figma]({url+r['id'].replace(':','-')})." for r in audit['report'])+'\n\nПроверены тип ComponentSet, семь вариантов, Text Styles и их типографические Variables, привязки цветов, положительных отступов и четырёх радиусов. Макеты просмотрены визуально. Воспроизводимые скрипты: execution/grow_ui_kit.py и execution/finalize_grow_ui_kit.py. Новые Text Styles не создавались.\n\nЭто компоненты для макетов, не работающий сборщик событий или проигрыватель. D02 (единица первого клика) остаётся открытым. Полная интерактивная матрица и сборка финальных экранов — отдельные задачи.\n',encoding='utf-8')
    section(ROOT/'ds/foundation.md','## Foundation продукта в Dashboard — 2026-09-22',
      '[Foundation]('+url+'82-15) находится рядом с UI Kit — extended на странице UX-Lab · UI Kit. Исходный снимок Elastic UI выше сохранён.\n\nИспользуются импортированные Body Copy/Regular, Body Copy/Medium, Fine Print/Regular (Inter); новых Text Styles не создано. Их fontFamily, fontSize, fontWeight и lineHeight связаны с Variables. Размеры импортированы из Dimensions: 4, 8, 12, 16, 24, 32; радиус Radius/Small — 4. Цвета — существующая палитра продукта.\n\nДобавлена отдельная коллекция UX-Lab · Heatmap: 10 semantic-переменных heatmap/intensity/1…10, режим Light, scopes FRAME_FILL и SHAPE_FILL, WEB code syntax. Шкала светлый → тёмный оливковый — проектное решение для легенды. Алгоритм агрегации, числовые пороги и шкала реальных данных не утверждены. Полные значения и Node ID сохранены в productExtensions файла index.json и grow-ui-kit-audit.json.\n\nЭто целевая основа трёх дополнений; полный перенос или модернизация всех 204 исходных элементов не выполнялись.')
    palette=json.loads((ROOT/'ds/product-palette.json').read_text(encoding='utf-8'))
    for v in audit['heatmapVariables']:
        rgba=next(iter(v['values'].values()))
        palette['colors'][v['name']]='#'+''.join(f'{round(rgba[k]*255):02X}' for k in ('r','g','b'))
    palette['heatmapScale']='Separate sequential intensity scale; illustrative legend, numerical thresholds remain undefined'
    dump(ROOT/'ds/product-palette.json',palette)
    section(ROOT/'ds/product-palette.md','## Шкала карты — 2026-09-22','Для HeatmapLegend добавлены отдельные semantic Variables heatmap/intensity/1…10. Это последовательная шкала светлый → тёмный оливковый, не шкала успеха/ошибки. Значения в product-palette.json; привязки подтверждены в grow-ui-kit-audit.json. Шкала используется в компоненте легенды, алгоритм и числовые пороги будущей карты остаются открытыми.')
    draft=ROOT/'ds/.tmp/grow_ui_kit_draft.md'
    d=draft.read_text(encoding='utf-8');d=re.sub(r'^Статус:.*$', 'Статус: согласовано и выполнено 2026-09-22. Актуальный результат — ds/grow-ui-kit-status.md; ниже сохранены исходные описания и предпосылки.',d,count=1,flags=re.M);draft.write_text(d,encoding='utf-8')
    directive=ROOT/'directives/directive_grow_ui_kit.md'
    d=directive.read_text(encoding='utf-8');d=re.sub(r'^> Проверка в текущем проекте:.*$', '> Выполнено 2026-09-22: Elastic UI (Copy) подключена к Dashboard, три компонента созданы и проверены. Состав уже согласован. Результат: ds/grow-ui-kit-status.md. При повторе использовать существующие Node ID и не создавать дубли.',d,count=1,flags=re.M)
    d+='\n\n## Проверенные особенности текущего инструмента\n\n- Служебные компоненты с точкой в имени могут оставаться UNPUBLISHED даже после публикации основной библиотеки. Проверять конкретные ключи; при наличии использовать основной компонент той же версии.\n- Импортировать remote-компонент по key в каждом вызове перед использованием: временный ID без materialized instance может не разрешаться в следующем вызове.\n- Для SOLID в overrides instances задавать fallback RGB, полученный из той же Variable, и сохранять VARIABLE_ALIAS: иначе screenshot может показывать чёрный fallback. Это не отвязка цвета от токена.\n- Нельзя ставить componentPropertyReferences на текст внутри instance. Раскрывать существующее вложенное свойство через isExposedInstance.\n- Одинаковое текстовое свойство набора может синхронизировать default между вариантами. Для различающихся пояснений использовать отдельные свойства и проверять screenshot каждого состояния.\n- После combineAsVariants проверять четыре радиуса самого набора: Figma по умолчанию может поставить непривязанный радиус 5.\n'
    directive.write_text(d,encoding='utf-8')
    catalog=(ROOT/'ds/components.md').read_text(encoding='utf-8')
    names=re.findall(r'^### (.+)$',catalog,re.M)
    assert all(names.count(name)==1 for name in descriptions)
    assert len(names)==207
    print(json.dumps({'components':3,'variants':7,'catalogEntries':len(names),'catalogLines':len(catalog.splitlines()),'auditPassed':True,'url':url+'82-45'},ensure_ascii=False))

if __name__=='__main__': main()
