"""Apply phase 1.3 priorities after explicit approval of the sitemap structure."""

from pathlib import Path
import difflib
import re
import sys

sys.dont_write_bytecode = True
from create_sitemap import TREE, STATES, EXTENSIONS

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "ia/sitemap.md"
    original = path.read_text(encoding="utf-8")
    assert not re.search(r"\[(?:core|v2|later)\]", original), "Priority phase already applied; review existing file"
    old_status = "Фаза 1.2. Основание: [инвентаризация](screens-inventory.md), подтверждённая пользователем сообщением **«апрув»** после фазы 1.1, и [PRD](../prd.md). **Статус этой структуры: предложена для согласования.** Подтверждение инвентаризации не считается подтверждением ещё не показанного дерева."
    new_status = "Фаза 1.3. [Инвентаризация](screens-inventory.md) согласована после фазы 1.1; структура и размещение состояний/расширений согласованы отдельным сообщением пользователя **«апрув»** после фазы 1.2. Основания приоритетов: [PRD](../prd.md) и [MoSCoW](../prioritization.md). **Статус разметки приоритетов: предложена для отдельного согласования.**"
    assert old_status in original
    result = original.replace(old_status, new_status)
    legend = """## Обозначения приоритетов

- `[core]` — первая версия: Must из PRD и согласованные служебные состояния основного сценария.
- `[v2]` — ближайшее развитие: Should, кандидаты **v1.1 в PRD**. Здесь v2 — маркер директивы «следующий релиз», а не переименование версии PRD.
- `[later]` — бэклог: Could, кандидаты **v2.0 в PRD**; выпуск и сроки не обещаны.

Все основные экраны, тепловая карта с первым кликом, воронка, запись, четыре сигнала и PDF остаются в первой версии. Логические группы наследуют `[core]` от основного сценария; это не дополнительные функции. Приоритет расширения не понижает приоритет его родительского экрана.

"""
    result = result.replace("## Дерево экранов и представлений\n", legend + "## Дерево экранов и представлений\n", 1)
    for depth, name, description in TREE:
        old = "  " * depth + f"{name} — {description}"
        new = "  " * depth + f"{name} [core] — {description}"
        assert result.count(old) == 1
        result = result.replace(old, new, 1)
    for name, *_ in STATES:
        old = f"| {name} |"
        assert result.count(old) == 1
        result = result.replace(old, f"| {name} [core] |", 1)
    future = {"F27": "v2", "F28": "v2", "F29": "v2", "F30": "later", "F31": "later", "F32": "later"}
    for name, owner, purpose, feature in EXTENSIONS:
        old = f"| {name} |"
        assert result.count(old) == 1
        result = result.replace(old, f"| {name} [{future[feature]}] |", 1)
    old_future = "Маркеры приоритетов будут добавлены отдельно в фазе 1.3 после согласования дерева."
    assert old_future in result
    result = result.replace(old_future, "Приоритеты расширений следуют MoSCoW: F27–F29 — [v2], F30–F32 — [later].")
    old_next = "Согласовать структуру дерева и размещение состояний/расширений. Только после явного подтверждения — фаза 1.3, разметка приоритетов. User flow и выбор способа отрисовки ещё впереди; Figma MCP в этой фазе не вызывался."
    assert old_next in result
    result = result.replace(old_next, "Согласовать разметку приоритетов. После явного подтверждения — фаза 1.4: сначала выбрать сценарий user flow, затем построить и согласовать Mermaid. До апрува всего текстового пакета Figma MCP не вызывается; в этой фазе вызовов не было.")
    # Removing tags must restore the exact approved structure and ownership.
    strip = lambda text: re.sub(r" \[(?:core|v2|later)\]", "", text)
    old_tree = re.search(r"```text\n(.*?)\n```", original, re.S).group(1)
    new_tree = re.search(r"```text\n(.*?)\n```", result, re.S).group(1)
    assert strip(new_tree) == old_tree
    assert len(new_tree.splitlines()) == 24
    assert max((len(line) - len(line.lstrip())) // 2 for line in new_tree.splitlines()) == 2
    original_rows = [line for line in original.splitlines() if line.startswith("| ")]
    revised_rows = [strip(line) for line in result.splitlines() if line.startswith("| ")]
    assert original_rows == revised_rows
    assert len(re.findall(r"^\| \w+ \[core\] \|", result, re.M)) == 17
    assert len(re.findall(r"^\| \w+ \[v2\] \|", result, re.M)) == 3
    assert len(re.findall(r"^\| \w+ \[later\] \|", result, re.M)) == 3
    inventory_path = ROOT / "ia/screens-inventory.md"
    inventory = inventory_path.read_text(encoding="utf-8")
    old_inventory = "Список A и служебные дополнения B согласованы. Предложенная структура следующей фазы сохранена в [sitemap.md](sitemap.md) и ожидает отдельного подтверждения. Приоритеты и user flow ещё не созданы; Figma MCP не вызывался."
    new_inventory = "Список A и служебные дополнения B согласованы. Структура [sitemap.md](sitemap.md) отдельно согласована пользователем; разметка приоритетов подготовлена и ожидает подтверждения. User flow ещё не создан; Figma MCP в рамках этой директивы не вызывался."
    assert old_inventory in inventory
    updated_inventory = inventory.replace(old_inventory, new_inventory)
    changes = "".join(difflib.unified_diff(original.splitlines(True), result.splitlines(True), fromfile="ia/sitemap.md (phase 1.2 approved)", tofile="ia/sitemap.md (phase 1.3 proposed)"))
    temp = ROOT / ".tmp"
    temp.mkdir(exist_ok=True)
    (temp / "sitemap-priorities.diff").write_text(changes, encoding="utf-8", newline="\n")
    path.write_text(result, encoding="utf-8", newline="\n")
    inventory_path.write_text(updated_inventory, encoding="utf-8", newline="\n")
    assert path.read_text(encoding="utf-8") == result
    print("Updated: ia/sitemap.md; phase 1.2 approval recorded, priorities await phase 1.3 approval")
    print("Verified: 24 core tree nodes, 17 core states, 3 next-release and 3 backlog extensions")
    print("Approved hierarchy, descriptions and canonical owners unchanged; full diff: .tmp/sitemap-priorities.diff")


if __name__ == "__main__":
    main()
