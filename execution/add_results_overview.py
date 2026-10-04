"""Apply the user's results-dashboard correction to the current IA and sources.

Run after create_user_flows.py. Earlier IA generators describe approval phases;
this guarded revision records the subsequent explicit user correction.
"""

from pathlib import Path
import difflib
import re
import sys

sys.dont_write_bytecode = True
from create_user_flows import validate

ROOT = Path(__file__).resolve().parents[1]
updates = {}
originals = {}


def replace(relative, old, new):
    path = ROOT / relative
    if path not in updates:
        originals[path] = path.read_text(encoding="utf-8")
        updates[path] = originals[path]
    text = updates[path]
    if new in text and old not in text:
        return
    if text.count(old) != 1:
        raise ValueError(f"Expected one matching passage in {relative}: {old[:100]}")
    updates[path] = text.replace(old, new, 1)


OVERVIEW = '''### Обзор результатов — уточнение заказчика

После нажатия «Результаты» у выбранного исследования открывается **ResultsOverview — обзорный дашборд** с основными цифрами по сценариям. Тепловая карта остаётся главным инструментом подробного анализа и открывается по выбору пользователя из обзора. Основание: прямое уточнение заказчика при согласовании user flow; входит в первую версию.

Предлагаемая компоновка: число сценариев и участников исследования, затем список сценариев с основными показателями. Для строки сценария предлагаются название, число начавших, завершивших попытку, достигших цели (число и доля с явным знаменателем), количество участников с неполными данными. Точный набор карточек, формулы и правила включения — предмет проработки D02–D03 и F23; эти предложения не означают согласования всех метрик. Завершение попытки отличается от достижения цели, участники — от попыток; в свободном изучении без цели успешность неприменима.

Из обзора можно выбрать сценарий и открыть тепловую карту, воронку, участников/записи, сигналы затруднений или PDF. Переходы и возврат сохраняют контекст; карта не является обязательным промежуточным экраном. При отсутствии результатов показано пояснение, а не фиктивные нулевые показатели. Уточнение относится к представлению результатов существующих F01, F09–F18, F22–F26, без изменения их приоритетов. Список сценариев не определяет автоматически порядок их выдачи участнику: это остаётся D03.

Предлагаемые проверки: открытие результатов ведёт в ResultsOverview; показатели сценария соответствуют выбранной выборке и определениям F23; переход в подробный анализ и обратно сохраняет сценарий/фильтры; отсутствие цели и неполные данные не отображаются как нулевой успех.

'''


def main():
    # Keep brief and PRD writer templates aligned with their current artifacts.
    brief_old = "Коллеги просматривают тепловые карты частоты кликов, выбирают анализ первого клика, изучают воронки, воспроизводят сессии и выявляют затруднения. Результаты можно экспортировать в PDF. Состав PDF-отчёта пока не определён."
    brief_new = "При открытии результатов выбранного исследования коллега сначала видит обзорный дашборд с основными цифрами по сценариям. Предлагается показать количество и список сценариев с показателями каждого. Из обзора пользователь выбирает тепловую карту, воронку, участников/записи, сигналы затруднений или PDF. Тепловая карта остаётся главным инструментом подробного анализа, но не открывается автоматически первой; режим первого клика находится внутри неё. Точный набор обзорных показателей и состав PDF пока не определены. Основание: уточнение заказчика при согласовании user flow."
    for relative in ("brief.md", "execution/create_ux_testing_brief.py"):
        replace(relative, brief_old, brief_new)
    for relative in ("prd.md", "execution/create_prd.py"):
        replace(relative, "### Основной сценарий primary-персоны\n", OVERVIEW + "### Основной сценарий primary-персоны\n")
        replace(relative, "6. Открыть карту частоты либо первого клика в нужном контексте, сопоставить с воронкой и четырьмя сигналами.", "6. Открыть ResultsOverview с основными цифрами и списком сценариев; выбрать сценарий и перейти к тепловой карте, воронке или сигналам для подробного анализа.")
    # Heatmap importance must not imply the initial results route.
    old = "Это главное представление анализа для выбранной страницы, её состояния и выборки."
    new = "Это главный инструмент подробного анализа выбранной страницы, её состояния и выборки; вход в результаты начинается с обзорного дашборда."
    for relative in ("prd.md", "features_list.md", "mvp_scope.md", "execution/create_scope_prioritization.py", "execution/clarify_heatmap_terms.py"):
        path = ROOT / relative
        text = updates.get(path, path.read_text(encoding="utf-8"))
        if old in text:
            # PRD repeats descriptions in its scope and roadmap tables.
            if path not in updates:
                originals[path] = text
            updates[path] = text.replace(old, new)

    replace("ia/screens-inventory.md", "- **Heatmaps** — Главный экран анализа:", "- **ResultsOverview** — Первый экран результатов исследования: обзор основных цифр по сценариям; предлагается список сценариев с их количеством и показателями, выбор подробного анализа. *Тип: представление; PRD: обзор результатов, F01, F11, F23; основание: уточнение заказчика.*\n- **Heatmaps** — Главный инструмент подробного анализа:")
    replace("ia/screens-inventory.md", "Дерево sitemap согласуется отдельно.", "После согласования фаз 1.1–1.3 пользователь уточнил вход в результаты: добавлен ResultsOverview. Переходы user flow остаются на согласовании.")
    replace("ia/screens-inventory.md", "| F11–F17: поведение и ввод | Funnel, Replay, Signals, IncompleteData |", "| Обзор результатов: уточнение заказчика | ResultsOverview — основные цифры и выбор сценария/анализа |\n| F11–F17: поведение и ввод | Funnel, Replay, Signals, IncompleteData |")

    replace("ia/sitemap.md", "логическая группа результатов выбранного исследования; открывается Heatmaps", "логическая группа результатов выбранного исследования; открывается ResultsOverview")
    replace("ia/sitemap.md", "    Heatmaps [core]", "    ResultsOverview [core] — обзор результатов: основные цифры, список сценариев и выбор подробного анализа\n    Heatmaps [core]")
    replace("ia/sitemap.md", "отдельный Dashboard без подтверждённой задачи не добавлен.", "по уточнению заказчика результаты открываются в ResultsOverview — обзорном дашборде выбранного исследования.")
    replace("ia/sitemap.md", "- **Analysis** — результаты того же исследования с открытием **Heatmaps**. Тепловая карта остаётся главным представлением; Report относится к результатам, а не к отдельному сервису отчётности.", "- **Analysis** — результаты того же исследования с открытием **ResultsOverview**: основные цифры и предлагаемый список сценариев. Из обзора доступны Heatmaps, Funnel, Participants, Signals и Report. Тепловая карта остаётся главным инструментом подробного анализа, открываемым по выбору; Report доступен без обязательного посещения карты.")
    replace("ia/sitemap.md", "| ResultsEmpty [core] | Heatmaps | Нет поступивших результатов; не рисовать фиктивную карту. | Другие результаты используют тот же принцип пустого состояния. |", "| ResultsEmpty [core] | ResultsOverview | Нет поступивших результатов; не показывать фиктивные нулевые показатели. | Heatmaps и другие результаты используют тот же принцип пустого состояния. |")
    replace("ia/sitemap.md", "**43 позиции** инвентаризации: 18 основных представлений", "**44 позиции** инвентаризации: 19 основных представлений")
    replace("ia/sitemap.md", "**24 узла**: 20 экранов/представлений", "**25 узлов**: 21 экран/представление")
    replace("ia/sitemap.md", "## Следующее действие\n", "## Уточнение после разметки приоритетов\n\nПо прямому указанию пользователя добавлен ResultsOverview [core] как первый экран результатов. Подробная аналитика открывается из обзора. Это исправление ранее согласованной структуры; обновлённый flow анализа ожидает согласования вместе с двумя другими flow.\n\n## Следующее действие\n")
    replace("ia/open-questions.md", "Предлагается Heatmaps как основной экран, Funnel/Participants как связанные представления; ParticipantDetails и Signals можно разместить панелями. Утверждение списка не фиксирует эту компоновку.", "Вход решён пользователем: ResultsOverview с основными цифрами по сценариям; Heatmaps открывается по выбору. Список сценариев и его показатели предложены к проработке; точный набор карточек/колонок и размещение ParticipantDetails/Signals остаются открытыми.")

    flow_pairs = [
        ('    studies["Studies"]\n    heatmaps["Heatmaps"]', '    studies["Studies"]\n    resultsOverview["ResultsOverview"]\n    heatmaps["Heatmaps"]'),
        ('    studies -->|"Открыть результаты"| heatmaps', '    studies -->|"Открыть результаты"| resultsOverview\n    resultsOverview -->|"Выбрать сценарий; тепловая карта"| heatmaps\n    resultsOverview -->|"Выбрать сценарий; воронка"| funnel\n    resultsOverview -->|"Открыть участников"| participants\n    resultsOverview -->|"Проверить сигналы затруднений"| signals'),
        ('    heatmaps -->|"Разобрать шаги цели"| funnel\n', ''),
        ('    heatmaps -->|"Проверить сигналы затруднений"| signals\n', ''),
        ('    participants -->|"Вернуться к карте"| heatmaps', '    participants -->|"Вернуться к обзору"| resultsOverview\n    heatmaps -->|"Назад; контекст сохранён"| resultsOverview'),
        ('    heatmaps -->|"Подготовить PDF"| report', '    resultsOverview -->|"Подготовить PDF"| report'),
    ]
    for relative in ("ia/flows/results-analysis.mmd", "execution/create_user_flows.py"):
        for old, new in flow_pairs:
            replace(relative, old, new)
    notes_pairs = [
        ("[results-analysis.mmd](results-analysis.mmd) — 8 экранов.", "[results-analysis.mmd](results-analysis.mmd) — 9 экранов. Вход изменён по прямому уточнению пользователя."),
        ("- Вход — авторизованный коллега открывает результаты из Studies. Главное представление — Heatmaps, **тепловая карта частоты кликов**. «Первый клик» — режим этой же карты, не отдельная страница (D02).", "- Вход — Studies → **ResultsOverview**, обзорный дашборд выбранного исследования с основными цифрами по сценариям. Предложение: общее число сценариев/участников и список сценариев с количеством начавших, завершивших, достигших цели и неполными данными. Точные показатели/формулы ещё уточняются (F23, D03); завершение не равно успеху.\n- Из обзора можно выбрать сценарий и открыть Heatmaps, Funnel, Participants, Signals или Report. **Heatmaps — тепловая карта частоты кликов**, главный инструмент подробного анализа, открываемый по выбору. «Первый клик» — режим этой же карты (D02)."),
        ("- Все переходы сохраняют контекст исследования и выборки. На схеме показан возврат к карте; возврат к исходной воронке или сигналам также должен сохранять источник, фильтры и выбранный шаг/сигнал (F24).", "- Все переходы сохраняют контекст исследования, сценария и выборки. На схеме показан возврат к обзору; возврат к исходной карте, воронке или сигналам также сохраняет источник, фильтры и выбранный шаг/сигнал (F24)."),
        ("- Report доступен из результатов; просмотр replay не является обязательным условием экспорта.", "- Report доступен напрямую из ResultsOverview; просмотр карты или replay не является обязательным условием экспорта."),
    ]
    for relative in ("ia/flows/README.md", "execution/create_user_flows.py"):
        for old, new in notes_pairs:
            replace(relative, old, new)

    sitemap = updates[ROOT / "ia/sitemap.md"]
    tree = re.search(r"```text\n(.*?)\n```", sitemap, re.S).group(1)
    allowed = set(re.findall(r"^\s*([A-Za-z]+) \[core\]", tree, re.M))
    assert len(tree.splitlines()) == len(allowed) == 25
    assert max((len(line) - len(line.lstrip())) // 2 for line in tree.splitlines()) == 2
    assert len(re.findall(r"^- \*\*[A-Za-z]+\*\* —", updates[ROOT / "ia/screens-inventory.md"], re.M)) == 44
    flow = updates[ROOT / "ia/flows/results-analysis.mmd"]
    assert validate(flow, allowed)[0] == 9
    assert 'studies -->|"Открыть результаты"| resultsOverview' in flow
    assert 'studies -->|"Открыть результаты"| heatmaps' not in flow
    for path, content in updates.items():
        if path.suffix == ".py":
            compile(content, str(path), "exec")
    diff = "".join("".join(difflib.unified_diff(originals[path].splitlines(True), content.splitlines(True), fromfile=str(path.relative_to(ROOT)), tofile=str(path.relative_to(ROOT)))) for path, content in updates.items())
    (ROOT / ".tmp").mkdir(exist_ok=True)
    (ROOT / ".tmp/results-overview.diff").write_text(diff, encoding="utf-8")
    for path, content in updates.items():
        path.write_text(content, encoding="utf-8", newline="\n")
        assert path.read_text(encoding="utf-8") == content
    print(f"Updated {len(updates)} documents and writer sources. Verified: 25 sitemap nodes, 44 inventory items, 9 analysis screens. Full diff: .tmp/results-overview.diff")


if __name__ == "__main__":
    main()
