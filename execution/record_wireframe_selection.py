"""Record the explicitly approved five-screen wireframe scope."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCREENS = [
    ('ResultsOverview', 'Обзор результатов: основные цифры, список сценариев и выбор подробного анализа'),
    ('Heatmaps', 'Тепловая карта частоты кликов и режим первого клика'),
    ('Funnel', 'Воронка прохождения и показатели шагов'),
    ('Replay', 'Воспроизведение действий, переходов и введённых данных'),
    ('SuccessCriteria', 'Настройка успеха по URL, кнопке или последовательности'),
]


def main():
    sitemap = (ROOT / 'ia/sitemap.md').read_text(encoding='utf-8')
    for name, _ in SCREENS:
        assert re.search(rf'^\s+{name} \[core\]', sitemap, re.M), name
    content = '''# Wireframes — согласованный набор экранов

Директива: [Sitemap → Low-fi Wireframes](../../directives/directive_wireframes.md).

Фаза 1.1 завершена: пользователь подтвердил все пять предложенных экранов сообщением «хорошо тогда апрув по всем экранам». Replay остаётся в выбранном наборе и объёме MVP. Обсуждение размера записи не утверждает технологию, срок хранения или числовой лимит диска.

| Экран | Назначение | Размер |
| --- | --- | --- |
'''
    for name, purpose in SCREENS:
        content += f'| {name} | {purpose} | Ожидает выбора в фазе 1.2 |\n'
    content += '''
Предлагаемый формат для всех пяти экранов: desktop 1440×1024, исходя из настольного дашборда в брифе. Точный размер ещё не подтверждён пользователем.

Следующее действие: выбрать размер фреймов, затем подготовить структуру ResultsOverview. По директиве структуры экранов согласуются последовательно; текущий апрув относится к выбору экранов. Текстовые структуры и Figma-wireframes пока не созданы. Остальные core-экраны остаются в составе продукта.
'''
    path = ROOT / 'ia/wireframes/README.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding='utf-8') != content:
        raise FileExistsError('Selection already changed; review before replacing.')
    path.write_text(content, encoding='utf-8', newline='\n')
    assert path.read_text(encoding='utf-8') == content
    print('Five-screen selection recorded. Awaiting frame dimensions.')


if __name__ == '__main__':
    main()
