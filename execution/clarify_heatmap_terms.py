"""Clarify heatmap terminology in requirements and their source generators."""

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "features_list.md", "prioritization.md", "mvp_scope.md", "prd.md",
    "execution/create_scope_prioritization.py", "execution/create_prd.py",
)
REPLACEMENTS = (
    ("Карта частоты кликов", "Тепловая карта кликов (частота)"),
    ("Карта первого клика", "Тепловая карта — режим «Первый клик»"),
    (
        "Главное представление анализа показывает, куда кликают чаще. Карта относится к выбранной странице и контексту данных.",
        "Цветовой слой поверх изображения тестируемого интерфейса показывает частоту кликов: более интенсивные, тёплые зоны обозначают больше кликов по указанной шкале. Это главный инструмент подробного анализа выбранной страницы, её состояния и выборки; вход в результаты начинается с обзорного дашборда.",
    ),
    (
        "Переключить отображение на первый клик. Границу отсчёта — задание, страница или сессия — требуется определить, а не выбирать неявно.",
        "Режим той же тепловой карты: цветовой слой строится только по первым кликам в выбранной единице отсчёта. Границу отсчёта — задание, страница или сессия — требуется определить, а не выбирать неявно.",
    ),
    ("я хочу видеть карту частоты кликов", "я хочу видеть тепловую карту частоты кликов"),
    (
        "Карта частоты доступна в основном разделе результатов, а не только в выгрузке или скрытом дополнительном анализе.",
        "Тепловая карта доступна в основном разделе результатов: на изображение выбранного состояния интерфейса наложены цветовые зоны частоты кликов с видимой шкалой интенсивности.",
    ),
)


def main():
    edits = {}
    for name in FILES:
        original = (ROOT / name).read_text(encoding="utf-8")
        revised = original
        for old, new in REPLACEMENTS:
            revised = revised.replace(old, new)
        if name.endswith(".py"):
            ast.parse(revised)
        if revised != original:
            edits[name] = revised
    for name, content in edits.items():
        (ROOT / name).write_text(content, encoding="utf-8", newline="\n")
        assert (ROOT / name).read_text(encoding="utf-8") == content
        print("Updated and verified: " + name)
    print(f"Terminology synchronized in {len(edits)} files; feature IDs and priorities preserved")


if __name__ == "__main__":
    main()
