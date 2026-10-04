"""Build three requested review drafts using only approved sitemap screens."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FLOWS = {
    "study-launch": '''flowchart TD
    login["Login"]
    studies["Studies"]
    studySetup["StudySetup"]
    connection["Connection"]
    tasks["Tasks"]
    successCriteria["SuccessCriteria"]
    launch["Launch"]
    login -->|"Вход выполнен"| studies
    studies -->|"Создать исследование"| studySetup
    studySetup -->|"Название и режим сохранены"| connection
    connection -->|"Ошибка или нет событий"| connection
    connection -->|"Подключено; режим заданий"| tasks
    connection -->|"Подключено; свободное изучение"| launch
    tasks -->|"Текст введён или выбран"| successCriteria
    successCriteria -->|"Цель сохранена"| launch
    launch -->|"Проблема подключения"| connection
    launch -->|"Ошибка цели задания"| successCriteria
    launch -->|"Проверено; скопировать ссылку"| launch
''',
    "participant-test": '''flowchart TD
    participantIntro["ParticipantIntro"]
    taskBriefing["TaskBriefing"]
    participantSession["ParticipantSession"]
    participantFinish["ParticipantFinish"]
    participantIntro -->|"Ссылка недоступна"| participantIntro
    participantIntro -->|"Инструкция прочитана; начать"| taskBriefing
    taskBriefing -->|"Задание или свободное изучение"| participantSession
    participantSession -->|"Прототип недоступен; повторить"| participantSession
    participantSession -->|"Прохождение завершено"| participantFinish
    participantSession -->|"Не могу продолжить"| participantFinish
    participantFinish -->|"Обновить статус передачи"| participantFinish
''',
    "results-analysis": '''flowchart TD
    studies["Studies"]
    resultsOverview["ResultsOverview"]
    heatmaps["Heatmaps"]
    funnel["Funnel"]
    participants["Participants"]
    participantDetails["ParticipantDetails"]
    replay["Replay"]
    signals["Signals"]
    report["Report"]
    studies -->|"Открыть результаты"| resultsOverview
    resultsOverview -->|"Выбрать сценарий; тепловая карта"| heatmaps
    resultsOverview -->|"Выбрать сценарий; воронка"| funnel
    resultsOverview -->|"Открыть участников"| participants
    resultsOverview -->|"Проверить сигналы затруднений"| signals
    heatmaps -->|"Частота или первый клик"| heatmaps
    heatmaps -->|"Участники выбранных кликов"| participants
    funnel -->|"Участники выбранного шага"| participants
    signals -->|"Участники выбранного сигнала"| participants
    participants -->|"Выбрать участника"| participantDetails
    participantDetails -->|"Открыть запись"| replay
    replay -->|"Запись недоступна"| replay
    replay -->|"Назад; контекст сохранён"| participantDetails
    participantDetails -->|"Вернуться к выборке"| participants
    participants -->|"Вернуться к обзору"| resultsOverview
    heatmaps -->|"Назад; контекст сохранён"| resultsOverview
    resultsOverview -->|"Подготовить PDF"| report
    report -->|"Сформировать и скачать PDF"| report
    report -->|"Ошибка экспорта; повторить"| report
''',
}

NOTES = '''# User flows: три сценария

Фаза 1.4 [директивы](../../directives/directive_prd_to_sitemap.md). Пользователь выбрал **все три** предложенных сценария. Статус: **схемы подготовлены для согласования**, выбор сценариев не означает апрув ещё не показанных переходов.

Основания: [PRD](../../prd.md), [sitemap](../sitemap.md), [персоны](../../personas.md). Все узлы — согласованные экраны `[core]`; логические группы и новые страницы не добавлены. Петля обозначает действие/состояние в текущем экране, а не автоматический бесконечный повтор. Это предложенные переходы, а не реализованный интерфейс.

## 1. Запуск исследования

[study-launch.mmd](study-launch.mmd) — 7 экранов. Основной пользователь: дизайнер; PM имеет те же права. PRD: F01–F06, F19, F21, F25; решения D01, D03, D06, D08–D10.

- Авторизованный коллега начинает со Studies. Способ входа в Login не фиксируется (D08).
- В StudySetup выбираются название и режим. Connection даёт код/инструкцию и показывает фактический приём контрольных событий, доступность прототипа и ошибки. При ошибке переход дальше не изображён как успешный.
- Задание вводится или выбирается из списка; его текст не превращается в цель автоматически. В SuccessCriteria отдельно настраивается URL, кнопка или цепочка событий (D01).
- Свободное изучение идёт в Launch без обязательного задания и критерия успеха. Инструкция этого режима должна быть показана участнику; отдельный редактор инструкции не утверждается.
- В Launch проводится контрольное прохождение через сценарий participant-test и проверка результата. Ссылка для приглашений копируется после проверки готовности; отправляет её сама команда. Контрольная попытка не считается одним из 20 реальных участников: правило маркировки/исключения предлагается уточнить в D03.
- Сохранение не равно готовности. ValidationError и SaveStatus показываются у соответствующих полей/действий; при ошибке данные не объявляются сохранёнными. Состояние черновика, публикация, закрытие ссылки и редактирование действующего теста остаются D03.

## 2. Прохождение участником

[participant-test.mmd](participant-test.mmd) — 4 экрана. Пользователь: участник с ПК или мобильного устройства; вход по приглашению без Login. PRD: F03, F06–F08, F17, F20; решения D03, D07, D09–D10.

- Вход — полученная ссылка → ParticipantIntro. При недоступной ссылке показывается UnavailableLink и объяснение; перейти к заданию нельзя. Номер участника назначается автоматически.
- До сбора поведения показывается объяснение записи действий и всего введённого содержимого без маскирования. Механика информирования остаётся D07; номер не делает содержимое анонимным.
- TaskBriefing показывает текст задания или инструкцию свободного изучения. ParticipantSession — работа в тестируемом интерфейсе; способ оболочки не выбран.
- Недоступность прототипа показывается как PrototypeUnavailable с возможностью повторить открытие или закончить с невозможностью продолжить. Это не автоматический провал задания.
- «Прохождение завершено» обозначает конец попытки по будущим правилам D03; достижение цели само по себе не задаёт здесь принудительный выход. Успех задания, завершение попытки и полнота передачи — разные показатели. Свободное изучение без цели не получает оценку «неуспех».
- ParticipantFinish показывает фактическое состояние передачи: ожидание, подтверждённый результат или обнаруженная неполнота. Повтор/буферизация передачи не обещаются до D09; перезагрузка не считается новой попыткой автоматически. Число заданий и переход к следующему заданию требуют правил D03 и не добавлены как утверждённая функция.

## 3. Анализ результатов и PDF

[results-analysis.mmd](results-analysis.mmd) — 9 экранов. Вход изменён по прямому уточнению пользователя. Пользователи: дизайнер и PM с равными правами. PRD: F09–F18, F22–F26; решения D02–D05, D09, D11.

- Вход — Studies → **ResultsOverview**, обзорный дашборд выбранного исследования с основными цифрами по сценариям. Предложение: общее число сценариев/участников и список сценариев с количеством начавших, завершивших, достигших цели и неполными данными. Точные показатели/формулы ещё уточняются (F23, D03); завершение не равно успеху.
- Из обзора можно выбрать сценарий и открыть Heatmaps, Funnel, Participants, Signals или Report. **Heatmaps — тепловая карта частоты кликов**, главный инструмент подробного анализа, открываемый по выбору. «Первый клик» — режим этой же карты (D02).
- До интерпретации выбираются исследование, задание/режим, страница/состояние и устройство. Несовместимые состояния и размеры не объединяются молча. Рядом с показателями видны числитель, знаменатель и полнота данных.
- От карты или шага воронки открывается связанная выборка участников, затем деталь и запись. В Signals доступны все четыре сигнала: повторные клики, клики без результата, возвраты, длительные паузы. Переход Signals → Participants предложен для проверки сигнала по записям, без обязательного автопоиска момента.
- Funnel применим к настроенной цели и шагам; отсутствие цели в свободном режиме не создаёт фиктивную воронку. Можно сразу перейти к карте, участникам или PDF.
- Все переходы сохраняют контекст исследования, сценария и выборки. На схеме показан возврат к обзору; возврат к исходной карте, воронке или сигналам также сохраняет источник, фильтры и выбранный шаг/сигнал (F24).
- Replay воспроизводит клики, прокрутку, переходы и введённое содержимое. ReplayUnavailable показывает отсутствие записи; обнаруженные пропуски видны в Participants, ParticipantDetails и Replay. Участник с неполными данными не исчезает и не считается неуспешным автоматически.
- Report доступен напрямую из ResultsOverview; просмотр карты или replay не является обязательным условием экспорта. До генерации понятны область данных и состав PDF (D11). ExportStatus различает формирование, готовность и ошибку; повтор выполняется по действию пользователя. PDF сохраняет контекст, числа и ограничения данных.
- ResultsEmpty, FilterEmpty, Loading и LoadError отображаются внутри соответствующих представлений. Пустая выборка не даёт фиктивную карту или вывод; общие состояния не превращены в отдельные экраны в этих трёх основных сценариях.

## Проверка и следующий шаг

Скрипт `execution/create_user_flows.py` проверяет ограниченный используемый синтаксис: `flowchart TD`, объявления/ссылки узлов, точное совпадение имён с деревом sitemap, достижимость и лимит 12 узлов. Это структурная проверка исходников, не проверка рендера Mermaid/Figma.

Предлагается согласовать все три схемы и пояснения. По фазе 1.4 директивы: «Flow собран в Mermaid. Перед отрисовкой на канвасе — есть что поправить?» После апрува всего текстового пакета отдельно выбирается метод отрисовки (фаза 2.0). В этой фазе вызовов Figma MCP не было.
'''


def validate(source, allowed):
    lines = source.splitlines()
    assert lines[0] == "flowchart TD"
    nodes, edges = {}, []
    for line in lines[1:]:
        node = re.fullmatch(r'    ([a-z][A-Za-z0-9]*)\["([A-Za-z]+)"\]', line)
        edge = re.fullmatch(r'    ([a-z][A-Za-z0-9]*) -->\|"([^"\n]+)"\| ([a-z][A-Za-z0-9]*)', line)
        if node:
            key, name = node.groups()
            assert key not in nodes and name in allowed
            nodes[key] = name
        elif edge:
            edges.append((edge[1], edge[3]))
        else:
            raise ValueError(f"Unsupported flow syntax: {line}")
    assert 1 <= len(nodes) <= 12
    assert len(set(nodes.values())) == len(nodes)
    assert all(a in nodes and b in nodes for a, b in edges)
    reached = {next(iter(nodes))}
    while True:
        updated = reached | {b for a, b in edges if a in reached}
        if updated == reached:
            break
        reached = updated
    assert reached == set(nodes)
    return len(nodes), len(edges)


def main():
    sitemap_path = ROOT / "ia/sitemap.md"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    tree = re.search(r"```text\n(.*?)\n```", sitemap, re.S).group(1)
    allowed = set(re.findall(r"^\s*([A-Za-z]+) \[core\]", tree, re.M))
    files = {}
    for name, source in FLOWS.items():
        counts = validate(source, allowed)
        files[ROOT / "ia/flows" / f"{name}.mmd"] = source
        print(f"{name}: {counts[0]} screens, {counts[1]} transitions; structure verified")
    files[ROOT / "ia/flows/README.md"] = NOTES
    for path, content in files.items():
        if path.exists() and path.read_text(encoding="utf-8") != content:
            raise FileExistsError(f"Refusing to overwrite edited artifact: {path}")
    old = "Приоритеты согласованы. Фаза 1.4: ожидается выбор пользователем сценария user flow, затем — построение и согласование Mermaid."
    new = "Приоритеты согласованы. Пользователь выбрал все три сценария; [user flows](flows/README.md) подготовлены для согласования в фазе 1.4."
    assert sitemap.count(old) == 1 or new in sitemap
    inventory_path = ROOT / "ia/screens-inventory.md"
    inventory = inventory_path.read_text(encoding="utf-8")
    old_inventory = "User flow ещё не создан; Figma MCP в рамках этой директивы не вызывался."
    new_inventory = "Три [user flow](flows/README.md) подготовлены и ожидают согласования; Figma MCP в рамках этой директивы не вызывался."
    assert inventory.count(old_inventory) == 1 or new_inventory in inventory
    files[sitemap_path] = sitemap.replace(old, new, 1)
    files[inventory_path] = inventory.replace(old_inventory, new_inventory, 1)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        assert path.read_text(encoding="utf-8") == content
    print("Saved 3 Mermaid drafts and notes; sitemap/inventory status updated. Awaiting review.")


if __name__ == "__main__":
    main()
