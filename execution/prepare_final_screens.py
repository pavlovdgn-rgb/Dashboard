"""Prepare a reviewable first-screen composition and queue from local evidence.

Does not modify Figma or mark any screen as built or approved.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "ds/screens"

MAP = """# ResultsOverview — карта финального экрана

Статус: на согласовании; финальный экран ещё не создан. Основание — локальные спецификации и реестр; актуальное состояние Figma проверяется после согласования.

Источник: wireframe `22:3`, Dashboard `1LeVoicxDT7Sl8TpMPs4hr`. Назначение: первый экран результатов с цифрами и выбором сценария. Тепловая карта открывается отдельным действием.

Final Screen Node ID: —

## Композиция

`Screen/ResultsOverview`, 1920 × 1080, секция Screens. Sidebar 320 px; Main занимает остаток. Auto Layout; Main padding 32, промежутки 24, внутри блоков 16/8 px — через Variables. Секции FILL × HUG; длинный контент прокручивается.

| Блок | Содержимое и компонент |
| --- | --- |
| Sidebar | NavMenu `153:2777`, Active=Overview; все разделы текущего исследования |
| Header | Кликабельные хлебные крошки проекта/исследования; коллега |
| Заголовок | «Обзор результатов», статус сбора, время обновления, «Обновить результаты», «Отчёт PDF» |
| Фильтры | Устройство: все / компьютер / мобильное; режим исследования; сброс фильтра |
| Сводка | 3 × новый SummaryMetric: сценариев 3; участников 20; с неполными данными 2 из 20 + переход к участникам |
| Сценарии | ScenarioTable `136:715`, ScenarioRow `135:1062`, SuccessMetric `132:574`; 3 строки, заголовок «Завершили» |
| Анализ сценария | Цель, потеря на шаге, страницы с сигналами; кнопки карты, воронки, участников/записей, сигналов/находок и снятия выбора |

Кнопки — ProductButton `125:450`; подписи и стрелки — настоящие иконки Elastic UI: document, arrowDown, heatmap, filter, users, flag. Фильтр собирается из существующих контролов Elastic UI, без отдельной имитации поля.

## Данные и поведение

Демо: строки «Найти товар…» — 20 / 16 / 14 из 18 (78%); «Изменить количество» — 18 / 15 / 12 из 17 (71%); «Оформить заказ» — 16 / 12 / 10 из 15 (67%). Неполные: 2 / 1 / 1; участников между строками не суммируем.

Первый вход — без выбора. Дополнительное состояние показывает выбранное «Оформить заказ»: цель — открыть оформление → заполнить данные → отправить заказ; потеря — 3 из 15 между шагами 1 и 2. Это демонстрационные данные. Фильтр и сценарий сохраняются при переходах. PDF открывает выбор состава отчёта. Правило повторных попыток D03 остаётся открытым.

## Доработки перед сборкой

Предлагаю добавить в UI-кит SummaryMetric: название, значение, пояснение, необязательная ссылка; Ready / Loading / NoData. Заливка background/surface, текст text/primary и text/secondary, граница border/subtle, Text Styles библиотеки. На экране три инстанса.

ScenarioTable адаптировать по ширине, высоту сделать по содержимому; добавить состояние без выбранной строки. Сохранить существующие варианты и их внешний вид. Подробности выбранного сценария дополнить по актуальному wireframe. Осмысленное наполнение — сводка, три сценария, контекст анализа; проверка заполнения ≥60% при отрисовке.

## Состояния и оформление

Загрузка, ошибка с повтором, отсутствие результатов, пустой фильтр, отсутствие выбора, длинные названия и свободное изучение — переключаемые скрытые блоки. Неполнота данных показана отдельно от успеха. Без наблюдений — «Нет данных», без сценариев в свободном режиме — «Не применимо».

Текущая тёплая нейтральная палитра и оливковые акценты; secondary-кнопки и активная строка сохраняются. Все цвета, отступы и радиусы — Variables; тексты — Text Styles. В каталоге нет подтверждённых продуктовых Effect Styles. Предложение: добавить shadow/card (0, 2, blur 8, spread 0; цвет через alias к чёрному Primitive, opacity 4%) для карточек сводки; новый стиль проверить после подключения к Figma.

Проверка после сборки: скриншот 1920 × 1080, переносы и границы, инстансы вместо копий, привязки токенов, состояния и контраст текста.
"""


def create_once(path: Path, text: str) -> None:
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise RuntimeError(f"Refusing to overwrite edited artifact: {path}")
    else:
        path.write_text(text, encoding="utf-8")


def main() -> None:
    manifest = json.loads((ROOT / "ia/wireframes/complete-manifest.json").read_text(encoding="utf-8"))
    frames = [f for f in manifest["frames"] if f["name"] != "SharedPatterns"]
    assert len({f["id"] for f in frames}) == len(frames), "Duplicate wireframe IDs"
    DEST.mkdir(parents=True, exist_ok=True)
    create_once(DEST / "results-overview.md", MAP)
    queue = "# Очередь final_screens\n\nИсточник: локальный complete-manifest.json. Наличие финальных экранов в Figma пока не проверено; существующие экраны будут пропущены после проверки. Это очередь исходников и состояний, а не отчёт о готовности.\n\n"
    queue += "| № | Исходник | Node ID | Размер | Статус |\n| --- | --- | --- | --- | --- |\n"
    for i, frame in enumerate(frames, 1):
        status = "Карта на согласовании" if frame["name"] == "ResultsOverview" else "Не начат"
        queue += f"| {i} | {frame['name']} | {frame['id']} | {frame['width']} × {frame['height']} | {status} |\n"
    create_once(DEST / "queue.md", queue)
    create_once(DEST / "_index.md", "# Screens index\n\nФинальные экраны этим прогоном ещё не созданы.\n\n- [ResultsOverview](results-overview.md) — карта на согласовании, первый экран результатов.\n- [Очередь](queue.md) — исходники и состояния из актуального локального реестра.\n")
    print(json.dumps({"wireframes": len(frames), "map": "ds/screens/results-overview.md", "figma_modified": False, "approval": "pending"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
