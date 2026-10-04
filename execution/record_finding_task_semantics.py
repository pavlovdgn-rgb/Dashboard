"""Record verified Figma layout semantics without claiming implemented interactions."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MARKER = '<!-- finding-task-semantics-2026-09-23 -->'
NOTES = {
    'finding-editor.md': '''Приоритет и статус проверки — два экземпляра ProductField (Type=Select), с отдельными подписями и значениями «Не задан» / «Нужно проверить». Ширина каждого 338 px, поля выровнены в одной строке. «Добавить доказательство» — Secondary; альтернативное действие «Добавить к существующей находке» — Tertiary без заливки. Метаданные не оформлены как кнопки. Основное действие «Сохранить находку» сохранено. Экспорт панели проверен: подписи и нижние действия помещаются. Выпадающие варианты и сохранение данных этим изменением не реализованы.''',
    'task-editor.md': '''«Выбрать задание из списка» перенесено из карточки критерия к подписи «Текст для участника» и оформлено Tertiary без заливки. В карточке критерия оставлено одно Secondary-действие «Настроить критерий», пояснение описывает условие успеха: открытие целевой страницы. Карточки имеют независимую высоту по содержимому. Такой же перенос сделан в фоне экрана с открытым списком заданий (workspace 210:9566). Экспорт основной композиции проверен. Эти изменения задают компоновку, не добавляют переходы прототипа.''',
}
for name, note in NOTES.items():
    path = ROOT / 'ds/screens' / name
    value = path.read_text(encoding='utf-8')
    if MARKER not in value:
        path.write_text(value.rstrip() + '\n\n' + MARKER + '\n## Разделение действий и полей\n\n' + note + '\n', encoding='utf-8')

receipt = {
    'fileKey': '1LeVoicxDT7Sl8TpMPs4hr',
    'findingDrawer': '210:19682',
    'findingFields': ['210:19759', '210:19766'],
    'taskWorkspaces': ['210:9243', '210:9566'],
    'taskHeadingRows': ['345:10738', '345:10745'],
    'screenshotsReviewed': ['210:19682', '210:9243'],
    'prototypeInteractionsAdded': False,
}
(ROOT / 'ds/screens/finding-task-semantics.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Recorded verified Figma semantics changes')
