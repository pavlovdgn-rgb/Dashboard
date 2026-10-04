"""Record verified Playback variants without regenerating other components."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / 'ds'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def replace(path, old, new):
    text = path.read_text(encoding='utf-8')
    if old in text:
        path.write_text(text.replace(old, new), encoding='utf-8')

def main():
    bulk_path = DS / 'component-variants-audit.json'
    if bulk_path.exists() and read(bulk_path).get('status') == 'complete':
        print(json.dumps({'status': 'complete', 'note': 'Bulk review supersedes this earlier single-component receipt; use finalize_component_variants.py.'}))
        return
    audit = read(ROOT / '.tmp/component-variants/replay-final-audit.json')
    replay = next(c for c in audit['report'] if c['name'] == 'ReplayControls')
    dims = audit['replayDimensions']
    assert audit['passed'] and len(dims) == 4
    assert {c['name'] for c in dims} == {f'Coverage={c}, Playback={p}' for c in ('Complete', 'Gap') for p in ('Paused', 'Playing')}
    assert all((c['width'], c['height'], c['buttonWidth']) == (1360, 245, 155) for c in dims)
    assert all(c['position'].get('characters') == 'PositionLabel#84:2' for c in dims)
    assert all(p['variable'] == 'VariableID:102:94' for c in dims for p in c['playheads'])
    record = {'date': '2026-09-22', 'status': 'complete', 'componentId': replay['id'], 'variants': dims, 'properties': replay['properties'], 'newTokens': [], 'auditPassed': True, 'visualCheckPassed': True}
    write(DS / 'replay-variants-status.json', record)
    write(DS / 'grow-ui-kit-audit.json', audit)
    write(ROOT / '.tmp/component-variants/current.json', audit['report'])
    for filename, key in [('index.json', 'productExtensions'), ('grow-ui-kit-status.json', None)]:
        path = DS / filename
        data = read(path)
        components = data[key]['components'] if key else data['createdComponents']
        target = next(c for c in components if c['name'] == 'ReplayControls')
        target.update({k: replay[k] for k in ('variants', 'properties')})
        data['replayVariantsUpdate'] = record
        if key:
            data[key]['variantCount'] = 9
        else:
            data['variantCount'] = 9
        write(path, data)
    replace(DS / 'components.md', 'всего семь вариантов.', 'всего девять вариантов.')
    replace(DS / 'components.md', '- **Варианты:** Coverage=Complete; Coverage=Gap\n', '- **Варианты:** Coverage: Complete | Gap × Playback: Paused | Playing — 4 ячейки. Размер: 1360×245. Playing — кнопка «Пауза», Paused — «Воспроизвести».\n')
    replace(DS / 'grow-ui-kit-status.md', '**ReplayControls** — 2 варианта', '**ReplayControls** — 4 варианта')
    replace(DS / 'grow-ui-kit-status.md', 'семь вариантов', 'девять вариантов')
    replace(DS / 'foundation.md', 'линия и кружок обоих вариантов', 'линия и кружок всех четырёх вариантов ReplayControls')
    brief = DS / '.tmp/component_variants_ReplayControls.md'
    replace(brief, 'Статус: предложение, ожидает подтверждения.', 'Статус: подтверждено пользователем и выполнено 22 сентября 2026.')
    replace(brief, '## Сейчас', '## До расширения')
    replace(brief, '## Предлагаемая матрица', '## Реализованная матрица')
    replace(brief, '## Вопрос брифа\n\nПодтвердить эти четыре варианта без новых размеров и цветов либо указать другую матрицу.', '## Результат\n\nЧетыре варианта проверены в Figma. Новые ID: Complete/Playing — 118:98; Gap/Playing — 118:168. Старые ID сохранены. Все кнопки Play/Pause имеют ширину 155, PositionLabel связан во всех ячейках. Новых токенов нет.')
    path = DS / 'component-variants-audit.json'
    data = read(path)
    data['status'] = 'partial_complete'
    data['completed'] = ['ReplayControls']
    data['pendingBrief'] = ['HeatmapLegend', 'DataCoverage']
    for c in data['entries']:
        if c['id'] == '84:713':
            c.update(axes={'Coverage': ['Complete', 'Gap'], 'Playback': ['Paused', 'Playing']}, possibleCombinations=4, liveCellCount=4, candidateReasons=[], resolution='Approved matrix completed')
    data['heuristicCandidates'] = sum(bool(c['candidateReasons']) for c in data['entries'])
    write(path, data)
    path = DS / 'component-variants-audit.md'
    text = path.read_text(encoding='utf-8')
    marker = '## Эвристические кандидаты'
    tail = text[text.index(marker):]
    tail = '\n'.join(line for line in tail.splitlines() if not line.startswith('| ReplayControls |'))
    path.write_text('# Component variants — Bulk\n\nСтатус: **частично выполнено**. Подтверждённое расширение ReplayControls завершено: Coverage Complete/Gap × Playback Paused/Playing, 4 варианта 1360×245. Старые ID, красный replay/playhead и PositionLabel сохранены. Привязки и снимки проверены. Новых токенов нет.\n\nКаталог: 207 компонентов; после закрытия ReplayControls остаётся ' + str(data['heuristicCandidates']) + ' эвристических кандидата, а не подтверждённых дефекта. HeatmapLegend и DataCoverage требуют отдельного конкретного брифа; библиотечные компоненты — проверки по использованию. Исходная Elastic UI не изменялась.\n\n' + tail + '\n', encoding='utf-8')
    note = '\n\n## Состояния воспроизведения — 22 сентября 2026\n\nМатрица расширена до Coverage Complete/Gap × Playback Paused/Playing. Четыре варианта 1360×245. Кнопки «Воспроизвести» и «Пауза» одинаковой ширины; соседние контролы не сдвигаются. Восемь фигур ползунка связаны с replay/playhead. PositionLabel доступен во всех вариантах. Новых токенов нет. Проверено визуально и по привязкам.\n'
    path = DS / 'replay-reference-update.md'
    if '## Состояния воспроизведения' not in path.read_text(encoding='utf-8'):
        path.write_text(path.read_text(encoding='utf-8') + note, encoding='utf-8')
    print(json.dumps({'completed': 'ReplayControls', 'variants': 4, 'totalProductVariants': 9, 'auditPassed': True}, ensure_ascii=False))

if __name__ == '__main__':
    main()
