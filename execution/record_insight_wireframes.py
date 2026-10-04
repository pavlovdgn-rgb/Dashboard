"""Record only verified Figma changes and synchronize their product documentation."""
from pathlib import Path
import json
import re
from update_insight_wireframes import PURPOSE, NEW, EXISTING

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'.tmp/insight-wireframes'
FOLDER=ROOT/'ia/wireframes'
LINK='https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='
DATE='2026-09-22'


def write_json(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def upsert_section(path, marker, body):
    text=path.read_text(encoding='utf-8') if path.exists() else ''
    if marker in text:
        text=text.split(marker)[0].rstrip()
    path.write_text(text.rstrip()+'\n\n'+marker+'\n\n'+body.rstrip()+'\n',encoding='utf-8')


def screen_structure(frame):
    blocks=[]
    for s in frame['sections']:
        blocks.append(f"### {s['name']} · {s['width']:g}×{s['height']:g}\n")
        blocks.extend('- '+t.replace('\n',' / ') for t in s['texts'])
        blocks.append('')
    if frame['overlay']:
        blocks.append('### Правая боковая панель · 736×1080\n')
        blocks.append('Поверх текущего экрана с затемнением фона. Закрытие возвращает в исходный контекст.\n')
        blocks.extend('- '+t.replace('\n',' / ') for t in frame['overlay']['texts'])
    if frame['name']=='FindingSaved':
        blocks.append('### Подтверждение сохранения\n\nВнизу справа: «Находка сохранена», контекст 014 / попытка 1 / 02:18, действия открыть находку или продолжить просмотр.')
    return '\n'.join(blocks)


def main():
    frames=[]
    for i in (0,4,8,12):
        frames.extend(json.loads((TMP/f'audit-{i}.json').read_text(encoding='utf-8')))
    assert len(frames)==16 and all(not f['issues'] for f in frames)
    assert all(f['width']==1920 and f['height']==1080 and f['navCount']==10 for f in frames)
    write_json(FOLDER/'insight-update-audit.json',{'date':DATE,'frames':frames,'passed':True,'scope':'16 changed/new frames; existing unrelated frames not re-audited'})
    rows=[]
    for f in frames:
        name=f['name'];url=LINK+f['id'].replace(':','-')
        rows.append(f"| {name} | {'Новый' if name in NEW else 'Обновлён'} | [Figma]({url}) | {PURPOSE[name]} |")
        structure=screen_structure(f)
        if name in NEW:
            kind='Боковая панель поверх страницы' if name in ('FindingDetails','FindingEditor') else 'Состояние страницы'
            content=f"# {name}\n\n**Статус:** отрисовано и проверено 22 сентября 2026.\n**Размер:** 1920×1080.\n**Тип:** {kind}.\n**Назначение:** {PURPOSE[name]}\n**Figma:** [{name}]({url}).\n\n## Секции\n\n{structure}\n\n"
            content+='## Поведение и границы\n\nОболочка и 10 пунктов меню сохранены. Находки находятся во вкладке раздела сигналов. Сигналы не доказывают причину; выводы и приоритет задаёт исследователь. Данные демонстрационные.\n\n'
            content+='[Правила сохранения, ошибок, фильтров и PDF](insight-update.md). Сбор данных, генерация PDF и интерактивные переходы не реализованы этими макетами.\n'
            (FOLDER/f'{name}.md').write_text(content,encoding='utf-8')
        else:
            body=f"**Отрисовано и проверено.** [{name}]({url}); исходный ID сохранён. {PURPOSE[name]}\n\nЭтот раздел заменяет прежнее описание изменённых блоков. Остальные правила экрана сохраняются.\n\n{structure}\n\n[Общий отчёт и правила](insight-update.md). Данные демонстрационные; интеракции макета не равны реализации."
            upsert_section(FOLDER/f'{name}.md','## Актуальная отрисовка — 22 сентября 2026',body)
    listing='| Экран | Изменение | Ссылка | Что изменено |\n| --- | --- | --- | --- |\n'+'\n'.join(rows)
    path=FOLDER/'insight-update.md'
    current=path.read_text(encoding='utf-8').replace('8 существующих экранов обновляются на прежних ID, добавляются 7 состояний.','Обновлены 8 существующих экранов на прежних ID и добавлены 8 состояний.').replace('Пустой список находок отрисовывается отдельно.','Пустой список находок отрисован отдельно.')
    path.write_text(current,encoding='utf-8')
    upsert_section(path,'## Результат отрисовки',listing+'\n\nПроверены все 16 фреймов: 1920×1080, по 10 пунктов навигации, переполнений дочерних слоёв не обнаружено. Каждый изменённый экран просмотрен на скриншоте. Панель редактора исправлена после проверки: ручной перенос текста Textarea и меньший вертикальный промежуток сохраняют видимость кнопки сохранения.\n\n[Новая секция Figma]('+LINK+'105-2). Скрипты: execution/update_insight_wireframes.py и execution/record_insight_wireframes.py. Live-аудит: insight-update-audit.json.\n\nСоздание находки из записи показано редактором и подтверждением. Вход из карты/воронки сохраняет соответствующий контекст источника; отдельные дубли редактора для каждой точки входа не создавались. Выбор дополнительных доказательств и нескольких попыток обозначен действиями; подробные раскрытые списки отдельно не отрисованы.\n\nСтарые генераторы отражают прежний пакет. Для восстановления текущего состояния после них нужно применить этот update-скрипт; запуск prepare сохраняет уже существующие фреймы по именам. Перед любым повторным прогоном сначала читать текущий канвас.')
    manifest_path=FOLDER/'complete-manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for f in frames:
        item={k:f[k] for k in ('name','id','width','height','sectionId','navCount')}
        old=next((x for x in manifest['frames'] if x['name']==f['name']),None)
        if old:old.update(item)
        else:manifest['frames'].append(item)
    manifest['date']=DATE;manifest['wireframes']=55;manifest['insightUpdate']={'updated':8,'added':8,'audited':16,'report':'insight-update.md'}
    write_json(manifest_path,manifest)
    upsert_section(FOLDER/'complete-delivery.md','## Обновление по инсайтам — 22 сентября 2026','Актуальный набор: **55 экранов и состояний**, плюс SharedPatterns. К прежним 47 добавлены 8 состояний; 8 существующих экранов обновлены на прежних ID. Из 55 — 51 desktop и 4 мобильных. [Изменения, ссылки и границы проверки](insight-update.md). Верхние разделы описывают базовую поставку от 21 сентября; этот раздел фиксирует последующее расширение.\n\nДля перехода из карты используется отдельное состояние ParticipantsFromHeatmap; Participants теперь показывает общий список сценария. Находки доступны внутри раздела сигналов. Кликабельный прототип по-прежнему не собран.')
    upsert_section(ROOT/'prd.md','## Дополнение от 22 сентября 2026 — находки и уточнение анализа', '''**Основание:** пользователь поручил дополнить варфреймы согласно [анализу референса](reference_dashboard_analysis.md). Ниже зафиксированы согласованные изменения дизайна; отрисовка не означает реализацию продукта. [Макеты и проверка](ia/wireframes/insight-update.md).

| ID дополнения | Требование и критерий приёмки UX |
| --- | --- |
| UX-I01 | Сохранить находку из записи, карты либо шага воронки. Название и наблюдение обязательны. Сохранить исследование, сценарий, устройство, участника/попытку и время либо область/шаг; источник можно открыть повторно. |
| UX-I02 | Отделять наблюдение от интерпретации. Поддержать несколько доказательств, ручной приоритет и необязательный критерий повторной проверки. Сигнал не превращается в автоматический диагноз. |
| UX-I03 | Список находок находится во вкладке раздела сигналов, детали/редактирование — в правой панели. Пустое состояние даёт вход к сигналам/записям; сохранение подтверждается и сохраняет контекст. Ошибки не уничтожают ввод; конфликт двух коллег не затирает изменения молча (D08). |
| UX-I04 | Сводка по страницам/состояниям показывает затронутых участников относительно посетивших и отдельные счётчики четырёх сигналов. Переход раскрывает конкретные события и записи. Одинаковые участники между группами не суммируются как уникальные. |
| UX-I05 | Обзор результатов остаётся первым экраном. Для выбранного сценария видны критерий, место подтверждённой потери и вход в углублённый анализ. Показываются статус сбора, время обновления данных и отдельно последнее событие. |
| UX-I06 | Список участников поддерживает фильтры исхода, типа сигнала и полноты. Прямое открытие относится к определённой попытке; несколько попыток требуют выбора. Выборка из карты показана отдельным состоянием и сохраняется. |
| UX-I07 | Режим первого клика дополнен распределением целей по понятным названиям. Правило «правильного первого клика» не назначается автоматически; D02 остаётся открытым. |
| UX-I08 | PDF включает выбранные находки, доказательства, интерпретацию отдельно, критерий повторной проверки и контекст/дату данных. Ссылки на записи сохраняют правила доступа команды. |

Не добавлены автоматические вердикты гипотез, эмоциональные диагнозы, балл трения, AI-правки прототипа или сущность раунда. Новая агрегированная медиана времени до цели отложена до определения методики; время конкретной попытки отображается. Существующий согласованный объём первой версии не сокращён. D02/D03/D04/D08 и техническая реализация хранения доказательств остаются открытыми там, где требуются формулы или архитектурные решения.''')
    flow=ROOT/'ia/flows/results-analysis.mmd'
    value=flow.read_text(encoding='utf-8')
    if 'findingEditor[' not in value:
        value+='''
    signalsByPage["SignalsByPage"]
    signalsPageDetails["SignalsPageDetails"]
    findings["Findings"]
    findingDetails["FindingDetails — боковая панель"]
    findingEditor["FindingEditor — боковая панель"]
    participantsFromHeatmap["ParticipantsFromHeatmap"]
    signals -->|"По страницам"| signalsByPage
    signalsByPage -->|"Выбрать страницу"| signalsPageDetails
    signalsPageDetails -->|"Событие и время"| replay
    signals -->|"Вкладка Находки"| findings
    findings -->|"Открыть находку"| findingDetails
    findingDetails -->|"Открыть доказательство"| replay
    findingDetails -->|"Редактировать"| findingEditor
    replay -->|"Сохранить наблюдение; участник, попытка, время"| findingEditor
    heatmaps -->|"Сохранить наблюдение; область и состояние"| findingEditor
    funnel -->|"Сохранить наблюдение; шаг и выборка"| findingEditor
    findingEditor -->|"Сохранено; вернуться к источнику"| findings
    findings -->|"Включить выбранные находки"| report
    heatmaps -->|"Участники выбранной области"| participantsFromHeatmap
    participantsFromHeatmap -->|"Конкретная попытка"| replay
'''
        value=value.replace('    heatmaps -->|"Участники выбранных кликов"| participants\n','')
        # Return is context-dependent; do not imply that saving always navigates to the list.
        value=value.replace('    findingEditor -->|"Сохранено; вернуться к источнику"| findings','    findingSaved["FindingSaved — подтверждение, исходный экран"]\n    findingEditor -->|"Сохранено; вернуться к источнику"| findingSaved\n    findingSaved -->|"Открыть находку"| findingDetails')
        flow.write_text(value,encoding='utf-8')
    upsert_section(ROOT/'ia/sitemap.md','## Дополнение по инсайтам — 22 сентября 2026','Внутри «Сигналы затруднений»: вкладки «Сигналы» и «Находки». Сигналы имеют режим «По страницам» и детали выбранной страницы; находки — пустое состояние и боковые панели просмотра/редактирования. FindingSaved — подтверждение на исходном экране. ParticipantsFromHeatmap сохраняет выборку карты. Отдельные верхнеуровневые «Гипотезы», «Раунды», «AI-агент» не добавляются. [Актуальные макеты](wireframes/insight-update.md).')
    upsert_section(ROOT/'reference_dashboard_analysis.md','## Реализация рекомендаций в макетах — 22 сентября 2026','После анализа пользователь поручил изменить варфреймы. Обновлены 8 экранов и добавлены 8 состояний. [Результат, ссылки и ограничения](ia/wireframes/insight-update.md). Этот статус заменяет прежние формулировки отчёта о том, что рекомендации ещё не отрисованы; сам анализ сохранён как основание решений.')
    upsert_section(ROOT/'directives/directive_wireframes.md','## Обновление после анализа референса — 22 сентября 2026','Перед правкой читать живой фрейм, сохранять пользовательские изменения и исходные ID. Для этого пакета использовать execution/update_insight_wireframes.py после базовых генераторов и фиксировать результаты execution/record_insight_wireframes.py. Textarea исходной библиотеки требует явного переноса длинного текста; resize корня не гарантирует изменение высоты вложенного Input. Проверять итоговые размеры и доступность нижней кнопки. Актуальный каталог — ia/wireframes/complete-manifest.json и insight-update.md.')
    for path in [FOLDER/'insight-update.md',ROOT/'prd.md']:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if not target.startswith(('http','#')):
                local=path.parent/target.split('#')[0]
                assert local.exists(), str(local)
    print(json.dumps({'updated':len(EXISTING),'new':len(NEW),'totalWireframes':55,'auditPassed':True,'documentationSynced':True}))


if __name__=='__main__':main()
