"""Build phase 1.2 after the user's explicit approval of the inventory."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
IA = ROOT / "ia"

# Logical containers are explicitly not additional product screens.
TREE = [
    (0, "Home", "логический корень продукта; коллега начинает со Studies, участник — со своей ссылки"),
    (1, "Login", "вход коллеги в сервис"),
    (1, "Studies", "исследования команды: создать или открыть"),
    (1, "StudySetup", "настройка выбранного исследования: название и режим"),
    (2, "Connection", "подключение живого интерфейса и проверка кода сбора"),
    (2, "Tasks", "текст задания или выбор из списка"),
    (2, "SuccessCriteria", "успех по URL, кнопке или последовательности"),
    (2, "Launch", "готовность, контрольное прохождение и ссылка участникам"),
    (1, "Analysis", "логическая группа результатов выбранного исследования; открывается Heatmaps"),
    (2, "Heatmaps", "тепловая карта частоты кликов и режим первого клика"),
    (2, "Funnel", "воронка прохождения и показатели шагов"),
    (2, "Participants", "участники, попытки и полнота данных"),
    (2, "ParticipantDetails", "деталь выбранного участника и доступ к его записи"),
    (2, "Replay", "воспроизведение действий, переходов и введённых данных"),
    (2, "Signals", "повторные клики, клики без результата, возвраты и паузы"),
    (2, "Report", "состав результатов и экспорт PDF"),
    (1, "Participation", "логическая группа прохождения по приглашению без регистрации"),
    (2, "ParticipantIntro", "инструкция, номер участника и объяснение записи до старта"),
    (2, "TaskBriefing", "текущее задание или инструкция свободного изучения"),
    (2, "ParticipantSession", "работа в тестируемом прототипе с управлением прохождением"),
    (2, "ParticipantFinish", "итог попытки и фактическое состояние передачи данных"),
    (1, "System", "логическая группа общих служебных экранов и состояний"),
    (2, "NotFound", "неизвестный адрес внутри сервиса"),
    (2, "ServiceUnavailable", "сервис временно недоступен"),
]

# One canonical owner per inventory item; reuse is a reference, not a second page.
STATES = [
    ("StudyEmpty", "Studies", "Нет исследований; действие создания первого.", "—"),
    ("ResultsEmpty", "Heatmaps", "Нет поступивших результатов; не рисовать фиктивную карту.", "Другие результаты используют тот же принцип пустого состояния."),
    ("FilterEmpty", "Analysis", "По текущим фильтрам нет данных.", "Heatmaps, Funnel, Participants: единый паттерн, без новых маршрутов."),
    ("ConnectionStatus", "Connection", "Проверка, успешный приём, отсутствие событий или ошибка.", "Launch показывает результат этой же проверки."),
    ("ValidationError", "StudySetup", "Некорректные/незаполненные настройки с объяснением.", "Tasks и SuccessCriteria отображают ошибку у нужного поля."),
    ("SaveStatus", "StudySetup", "Сохранение, сохранено или ошибка.", "Общий статус редактирования внутри настройки."),
    ("StudyStatus", "StudySetup", "Готовность и жизненный цикл выбранного исследования; правила D03 открыты.", "Studies и Launch показывают статус того же исследования."),
    ("FirstClick", "Heatmaps", "Режим той же тепловой карты; граница отсчёта D02 открыта.", "Не отдельный раздел аналитики."),
    ("IncompleteData", "Analysis", "Обнаруженная техническая неполнота отделена от неуспеха задания.", "Participants, ParticipantDetails, Replay и Report показывают относящиеся к ним пропуски."),
    ("ReplayUnavailable", "Replay", "Записи нет или её нельзя получить; причина обозначена.", "ParticipantDetails ссылается на состояние этой же записи."),
    ("ExportStatus", "Report", "PDF формируется, готов или произошла ошибка.", "—"),
    ("UnavailableLink", "ParticipantIntro", "Приглашение невалидно или тест больше недоступен.", "Не заменяется общим NotFound."),
    ("PrototypeUnavailable", "ParticipantSession", "Не открывается тестируемый интерфейс.", "Connection проверяет ту же доступность до приглашений."),
    ("ParticipationStatus", "Participation", "Состояние попытки и передачи, включая невозможность продолжить.", "ParticipantSession и ParticipantFinish отображают актуальное состояние попытки."),
    ("LoadError", "System", "Сбой загрузки конкретных настроек или данных; повтор действия.", "Показывается в месте сбоя, не создаёт отдельную страницу на каждый раздел."),
    ("AccessDenied", "System", "Нет доступа к командной части или данным.", "Не отправляет участника регистрироваться для обычного прохождения."),
    ("Loading", "System", "Обозначение ожидания загрузки без ложного пустого результата.", "Переиспользуется в нужном экране."),
]

EXTENSIONS = [
    ("ReplayTools", "Replay", "Поиск событий, сводка пути, пропуск неактивности.", "F27"),
    ("EditorPreview", "StudySetup", "Панель предпросмотра опыта участника.", "F28"),
    ("StudyReuse", "Studies", "Дублирование исследования или создание из его шаблона.", "F29"),
    ("FilterPresets", "Analysis", "Именованные сохранённые наборы фильтров.", "F30"),
    ("TaskSearch", "Tasks", "Поиск по разросшемуся списку заданий.", "F31"),
    ("AdvancedActions", "Home", "Общие расширенные команды; конкретные действия и поверхности ещё не определены.", "F32"),
]


def main():
    inventory_path = IA / "screens-inventory.md"
    inventory = inventory_path.read_text(encoding="utf-8")
    names_in_inventory = set(re.findall(r"^- \*\*([A-Za-z]+)\*\* —", inventory, re.M))
    containers = {"Home", "Analysis", "Participation", "System"}
    tree_names = [row[1] for row in TREE]
    assert len(tree_names) == len(set(tree_names))
    assert sum(depth == 0 for depth, _, _ in TREE) == 1
    assert max(depth for depth, _, _ in TREE) == 2
    assert all(re.fullmatch(r"[A-Z][A-Za-z]+", name) for name in tree_names)
    placements = set(tree_names) - containers
    for rows in (STATES, EXTENSIONS):
        for name, owner, *_ in rows:
            assert name not in placements
            assert owner in tree_names
            placements.add(name)
    assert placements == names_in_inventory, (placements ^ names_in_inventory)
    assert len(placements) == 43
    tree = "\n".join("  " * depth + f"{name} — {description}" for depth, name, description in TREE)
    content = """# Sitemap продукта

Фаза 1.2. Основание: [инвентаризация](screens-inventory.md), подтверждённая пользователем сообщением **«апрув»** после фазы 1.1, и [PRD](../prd.md). **Статус этой структуры: предложена для согласования.** Подтверждение инвентаризации не считается подтверждением ещё не показанного дерева.

## Дерево экранов и представлений

Один корень, максимум три уровня, отступ — два пробела. Home — логический корень, Analysis/Participation/System — группы, а не новые экраны. Дерево описывает принадлежность, не порядок переходов и не меню с обязательным показом каждого узла.

```text
""" + tree + "\n```\n"
    content += """
## Как читать структуру

- У коллеги начальная рабочая точка — **Studies**. После открытия исследования настройка и анализ сохраняют один и тот же контекст; отдельный Dashboard без подтверждённой задачи не добавлен.
- **StudySetup** объединяет настройку исследования. Connection, Tasks, SuccessCriteria и Launch предложены как его представления; вкладки или пошаговый мастер ещё можно выбрать при проектировании.
- **Analysis** — результаты того же исследования с открытием **Heatmaps**. Тепловая карта остаётся главным представлением; Report относится к результатам, а не к отдельному сервису отчётности.
- **ParticipantDetails** может быть панелью, **Signals** — представлением внутри аналитики/записи, **Report** — экраном или диалогом. Их функциональная принадлежность здесь едина; вид отображения ещё не фиксируется.
- **Participation** доступен по приглашению без входа коллеги. ParticipantSession обозначает работу в чужом тестируемом интерфейсе; способ оболочки прохождения пока открыт.
- Мобильный вариант относится к прохождению участника. Дерево не добавляет мобильный аналитический дашборд, регистрацию участника или разные права PM/дизайнера.

## Состояния и режимы — владельцы в дереве

Таблица является частью sitemap: состояние имеет одного владельца и переиспользуется по ссылке. Эти строки не создают четвёртый уровень страниц или дополнительные пункты меню.

| Состояние / режим | Владелец | Назначение | Переиспользование / ограничение |
| --- | --- | --- | --- |
"""
    for name, owner, purpose, reuse in STATES:
        content += f"| {name} | {owner} | {purpose} | {reuse} |\n"
    content += """
## Кандидаты развития — место в структуре

Это шесть расширений из согласованной инвентаризации и будущих версий PRD. Они не становятся частью первой версии из-за появления в sitemap; базовые функции соответствующих экранов остаются обязательными. Маркеры приоритетов будут добавлены отдельно в фазе 1.3 после согласования дерева.

| Расширение | Владелец | Назначение | PRD |
| --- | --- | --- | --- |
"""
    for name, owner, purpose, feature in EXTENSIONS:
        content += f"| {name} | {owner} | {purpose} | {feature} |\n"
    content += """
## Проверка полноты и границ

- Учтены все **43 позиции** инвентаризации: 18 основных представлений, 17 состояний/режимов, 6 расширений и 2 общих служебных экрана.
- В дереве **24 узла**: 20 экранов/представлений из инвентаризации и 4 явно обозначенных логических узла. Глубина с корнем — **3 уровня**.
- Каждый экран представлен в дереве один раз. Каждое состояние и расширение имеет одного владельца; повторное использование не дублирует владение.
- Связи Heatmaps/Funnel → Participants/ParticipantDetails → Replay предусмотрены PRD, но будут показаны переходами в user flow, а не вторыми копиями страниц.
- Нагрузка, контрольные 20 участников, определения метрик и хранение остаются сквозными требованиями. Неопределённые Login-механизмы, Settings, Onboarding и редактор выводов не добавлены молча; см. [открытые вопросы](open-questions.md).

## Следующее действие

Согласовать структуру дерева и размещение состояний/расширений. Только после явного подтверждения — фаза 1.3, разметка приоритетов. User flow и выбор способа отрисовки ещё впереди; Figma MCP в этой фазе не вызывался.
"""
    old_status = "Статус: **предложено для согласования; подтверждение пользователя ещё не получено**."
    new_status = "Статус: **инвентаризация согласована пользователем сообщением «апрув» после показа фазы 1.1**. Дерево sitemap согласуется отдельно."
    assert old_status in inventory
    old_next = "Согласовать список A и служебные дополнения B: что добавить, убрать или переименовать? До явного подтверждения пользователя фаза 1.2 не начинается. Figma MCP не вызывался, дерево, приоритеты и flow пока не создавались."
    new_next = "Список A и служебные дополнения B согласованы. Предложенная структура следующей фазы сохранена в [sitemap.md](sitemap.md) и ожидает отдельного подтверждения. Приоритеты и user flow ещё не созданы; Figma MCP не вызывался."
    assert old_next in inventory
    updated = inventory.replace(old_status, new_status).replace(old_next, new_next)
    target = IA / "sitemap.md"
    if target.exists():
        raise FileExistsError("Refusing to overwrite sitemap.md")
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
    inventory_path.write_text(updated, encoding="utf-8", newline="\n")
    assert target.read_text(encoding="utf-8") == content
    assert inventory_path.read_text(encoding="utf-8") == updated
    print("Created and verified: ia/sitemap.md")
    print("Recorded phase 1.1 approval in ia/screens-inventory.md")
    print("Validated: 1 root, 3 levels, 43 inventory items covered, unique ownership; phase 1.2 awaits approval")


if __name__ == "__main__":
    main()
