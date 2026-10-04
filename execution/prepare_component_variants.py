"""Audit the indexed catalog and prepare a concrete first bulk brief.

No Figma writes. A heuristic candidate is not a proven missing UI state.
"""
from pathlib import Path
import json
import re
from math import prod

ROOT=Path(__file__).resolve().parents[1]


def main():
    ds=ROOT/'ds'
    completed=ds/'replay-variants-status.json'
    if completed.exists() and json.loads(completed.read_text(encoding='utf-8')).get('status')=='complete':
        print(json.dumps({'status':'ReplayControls already completed','next':'Prepare a separate brief for the next component; existing approval is preserved.'}))
        return
    index=json.loads((ds/'index.json').read_text(encoding='utf-8'))
    md=(ds/'components.md').read_text(encoding='utf-8')
    live=json.loads((ROOT/'.tmp/component-variants/current.json').read_text(encoding='utf-8'))
    entries=[]
    for c in index['components']+live:
        axes={k:v.get('variantOptions',[]) for k,v in (c.get('properties') or {}).items() if v.get('type')=='VARIANT'}
        state_axes=[k for k in axes if k.lower() in ('state','status','disabled','loading','selected','focused','hover','pressed','paused','open','coverage')]
        size_axes=[k for k in axes if k.lower() in ('size','compressed','density')]
        reasons=[]
        if not state_axes:reasons.append('нет явной оси состояния')
        if not size_axes:reasons.append('нет явной оси размера/плотности')
        theoretical=prod(len(x) for x in axes.values()) if axes else 1
        if theoretical<=2:reasons.append('не более двух комбинаций variant-осей')
        name=c['name']
        entries.append({'name':name,'id':c['id'],'origin':'Dashboard' if c in live else 'Elastic UI','axes':axes,'possibleCombinations':theoretical,'liveCellCount':len(c['variants']) if 'variants' in c else None,'candidateReasons':reasons,'deprecatedMarker':'☠' in name,'internalOrExample':name.startswith('.') or '💡' in name})
    candidates=[x for x in entries if x['candidateReasons']]
    report={'status':'brief_pending','mode':'bulk','catalogEntries':len(entries),'markdownEntries':len(re.findall(r'^### ',md,re.M)),'heuristicCandidates':len(candidates),'liveVerifiedComponents':3,'entries':entries,'note':'Для исходных компонентов прочитан индекс, не выполнен новый полный обход канваса. Произведение осей не доказывает число существующих вариантов.'}
    (ds/'.tmp').mkdir(exist_ok=True)
    (ds/'component-variants-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['| Компонент | Файл | Возможные комбинации осей | Причина проверки |','| --- | --- | --- | --- |']
    rows.extend('| '+x['name']+' | '+x['origin']+' | '+str(x['possibleCombinations'])+' | '+'; '.join(x['candidateReasons'])+' |' for x in candidates)
    summary=f'''# Component variants — первичная проверка Bulk

Статус: **ожидается бриф первого расширения**. В Figma ничего не расширено.

Прочитан каталог: {len(entries)} компонентов (204 Elastic UI + 3 продуктовых). Эвристические кандидаты: {len(candidates)}. Это число проверок, а не число дефектов: статическим элементам не всегда нужны состояния и размеры, а автор библиотеки использует оси Disabled, Loading, Compressed, Open вместо единственного State.

Три набора Dashboard проверены в живом файле: HeatmapLegend — 2, ReplayControls — 2, DataCoverage — 3 варианта. Матрицы совпадают с каталогом. Исходные 204 записи проверены по индексированным свойствам; число реальных ячеек и взаимодействия на уровне nested instances требуют точечной проверки при выборе компонента.

## Очередь

1. **ReplayControls**: предложено добавить Playing к существующему Paused, сохранив оба Coverage. Итог 4 варианта; размеры прежние, цветов не добавляем. [Конкретный бриф](.tmp/component_variants_ReplayControls.md).
2. **HeatmapLegend**: решить, нужны ли легенде состояния отсутствия/загрузки данных или они должны оставаться на уровне карты. Не добавлять их механически из отсутствия State.
3. **DataCoverage**: Complete / Partial / Unavailable уже являются осью состояния. Нужен отдельный продуктовый выбор, требуется ли Pending; hover/focus относятся к вложенной кнопке, не всему сообщению.
4. Библиотечные компоненты: разбирать по фактическому использованию на экранах. Не менять исходную Elastic UI и не размножать полную декартову матрицу только из-за формального срабатывания эвристики.

Новые состояния не утверждены предыдущим апрувом low-fi экранов. Обновление состояния каталога как выполненного и запись на канвас — после согласования конкретной матрицы.

## Эвристические кандидаты

'''+ '\n'.join(rows)+'\n'
    (ds/'component-variants-audit.md').write_text(summary,encoding='utf-8')
    brief='''# ReplayControls — бриф расширения

Статус: предложение, ожидает подтверждения. [Текущий набор](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=84-713).

## Сейчас

Coverage: Complete | Gap. Два варианта 1360×245, кнопка «Воспроизвести», позиция 02:18 / 04:32. Состояние плеера фактически Paused. Сохранены красный replay/playhead #C61E25, оливковые события и штриховка разрыва.

## Предлагаемая матрица

Coverage: Complete | Gap × Playback: Paused | Playing. **4 ячейки всего, +2 новых**. Текущий desktop-размер 1360×245 остаётся единственным; искусственные sm/md/lg не добавляются.

| Имя для каталога | Variant properties в Figma | Изменение |
| --- | --- | --- |
| ReplayControls/Complete/Paused/Desktop | Coverage=Complete, Playback=Paused | Существующий вариант; ID 84:642 сохранить |
| ReplayControls/Gap/Paused/Desktop | Coverage=Gap, Playback=Paused | Существующий вариант; ID 84:678 сохранить |
| ReplayControls/Complete/Playing/Desktop | Coverage=Complete, Playback=Playing | Кнопка «Пауза» с соответствующей иконкой |
| ReplayControls/Gap/Playing/Desktop | Coverage=Gap, Playback=Playing | Кнопка «Пауза», разрыв и пояснение сохранены |

Позиция 02:18 и маркеры не изменяются: это два состояния UI на одной позиции, не анимация. В Gap отсутствующий интервал не заполняется событиями. Остальные кнопки и числовая шкала сохраняются. Поведение самой воспроизводящей реализации за пределами макета.

## Токены

Новые цвета или Semantic-токены для этого расширения **не нужны**: действие использует текущие action/primary и text/inverse; ползунок — replay/playhead, шкала — существующие токены. Иконка паузы подбирается из той же библиотеки; размеры, отступы и стили копируются с существующих bound-компонентов. Новый компактный размер, Loading/Unavailable и интерактивная матрица вложенных контролов не входят в этот первый прогон.

## Проверка

Один набор с четырьмя вариантами, уникальные пары Coverage/Playback. Старые два ID и свойства PositionLabel сохранены. Отсутствие переполнений, правильные надписи и иконки, красный ползунок, корректные привязки. Снимок набора после записи. Каталог обновляется только после успешной проверки.

## Вопрос брифа

Подтвердить эти четыре варианта без новых размеров и цветов либо указать другую матрицу.
'''
    (ds/'.tmp/component_variants_ReplayControls.md').write_text(brief,encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('entries','note')},ensure_ascii=False))


if __name__=='__main__':main()
