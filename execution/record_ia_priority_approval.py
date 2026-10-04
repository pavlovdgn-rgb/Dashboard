"""Record explicit user approval of phase 1.3 without changing the sitemap."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "ia/sitemap.md": [
        (
            "**Статус разметки приоритетов: предложена для отдельного согласования.**",
            "**Статус разметки приоритетов: согласована пользователем сообщением «апрув» после показа фазы 1.3.**",
        ),
        (
            "Согласовать разметку приоритетов. После явного подтверждения — фаза 1.4: сначала выбрать сценарий user flow, затем построить и согласовать Mermaid.",
            "Приоритеты согласованы. Фаза 1.4: ожидается выбор пользователем сценария user flow, затем — построение и согласование Mermaid.",
        ),
    ],
    "ia/screens-inventory.md": [
        (
            "разметка приоритетов подготовлена и ожидает подтверждения.",
            "разметка приоритетов отдельно согласована сообщением «апрув» после фазы 1.3.",
        ),
    ],
}


def main():
    updates = {}
    for relative, pairs in REPLACEMENTS.items():
        path = ROOT / relative
        content = path.read_text(encoding="utf-8")
        for old, new in pairs:
            if new in content and old not in content:
                continue
            if content.count(old) != 1:
                raise ValueError(f"Unexpected approval state: {relative}")
            content = content.replace(old, new, 1)
        updates[path] = content
    for path, content in updates.items():
        path.write_text(content, encoding="utf-8", newline="\n")
        assert path.read_text(encoding="utf-8") == content
    print("Phase 1.3 approval recorded. Phase 1.4 awaits user flow scenario selection.")


if __name__ == "__main__":
    main()
