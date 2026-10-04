"""Sync the inspected ReplayControls update without regenerating older designs."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    if (ROOT / 'ds/replay-variants-status.json').exists():
        from record_replay_variants import main as sync_variants
        sync_variants()
        return
    audit = json.loads((ROOT / '.tmp/replay-reference/audit.json').read_text(encoding='utf-8'))
    assert audit['passed'] and len(audit['replayDimensions']) == 2
    assert all(s['width'] == 48 for c in audit['replayDimensions'] for s in c['speeds'])
    write_json(ROOT / 'ds/grow-ui-kit-audit.json', audit)
    update = {
        'date': '2026-09-22', 'componentId': '84:713',
        'variants': audit['replayDimensions'],
        'features': ['proportional time scale', 'event rings', 'olive playhead',
                     'hatched missing interval', 'seek -5/+5 seconds',
                     'speed 1/1.5/2', 'fit', 'full screen'],
        'bindingsAuditPassed': True,
        'scope': 'UI Kit only; static design, existing low-fi Replay frame unchanged',
        'documentation': 'ds/replay-reference-update.md',
    }
    for name in ['index.json', 'grow-ui-kit-status.json']:
        path = ROOT / 'ds' / name
        data = json.loads(path.read_text(encoding='utf-8'))
        data['replayReferenceUpdate'] = update
        write_json(path, data)
    note = '''# ReplayControls: обновление по референсу

22 сентября 2026. [Компонент в Figma](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=84-713).

Сохранены ComponentSet 84:713 и варианты Complete 84:642 / Gap 84:678. Оба теперь 1360×245. Тёплые поверхности, графитовая кнопка и оливковые элементы используют переменные продукта.

Шкала показывает время пропорционально длительности 04:32, маркеры событий и позицию 02:18. Разрыв 01:40–02:05 выделен штриховкой и пояснением; отсутствие событий не подменяет разрыв данных. Управление: воспроизведение, −5/+5 секунд, скорости 1×/1.5×/2×, вписать, на весь экран. Использованы иконки и Button instances Elastic UI.

Перемотка на пять секунд и полноэкранный режим добавлены в дизайн по прямому запросу пользователя воспроизвести референс. Это спецификация UI, не реализация плеера. Старый low-fi Replay 24:93 этой операцией не перерисован. Демо-ввод не меняет требование брифа видеть введённое содержимое полей.

После исправления обрезания скоростей просмотрен финальный Gap; проверены размеры обоих вариантов и всех шести кнопок скорости (48 px). Аудит трёх наборов компонентов: 0 замечаний к привязкам цветов, Text Styles/типографики, положительных отступов и радиусов. Полная интерактивная матрица не проверялась.

Воспроизведение: execution/restyle_replay_controls.py (timeline → controls), затем аудит execution/grow_ui_kit.py. Для уменьшения импортированного Button нужно переопределить minWidth и использовать resizeWithoutConstraints: обычный resize в этой операции сохранял ширину 112 px. После записи проверять размер повторным чтением и скриншотом.
'''
    (ROOT / 'ds/replay-reference-update.md').write_text(note, encoding='utf-8')
    suffix = '\n\nОбновление ReplayControls от 22 сентября: [шкала по референсу, управление и границы изменений](replay-reference-update.md).\n'
    for name in ['components.md', 'grow-ui-kit-status.md']:
        path = ROOT / 'ds' / name
        text = path.read_text(encoding='utf-8')
        if 'replay-reference-update.md' not in text:
            path.write_text(text.rstrip() + suffix, encoding='utf-8')
    # Validate report cross-links after generation; no external URL requests.
    report = (ROOT / 'reference_dashboard_analysis.md').read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^)]+)\)', report)
    missing = [p for p in links if not p.startswith('https://') and not (ROOT / p).is_file()]
    assert not missing, missing
    print(json.dumps({'replayAuditPassed': True, 'reportLinksChecked': len(links), 'missingLocalLinks': missing}))


if __name__ == '__main__':
    main()
