"""Record verified Figma delivery and the user's approval of direct drawing."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
LINK = 'https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id='


def main():
    changes = {
        'ia/flows/README.md': [
            ('Статус: **схемы подготовлены для согласования**, выбор сценариев не означает апрув ещё не показанных переходов.', 'Статус: **согласовано и отрисовано**. После уточнения ResultsOverview пользователь подтвердил перенос всех схем в существующий Dashboard через use_figma сообщением «апрув».'),
            ('Предлагается согласовать все три схемы и пояснения. По фазе 1.4 директивы: «Flow собран в Mermaid. Перед отрисовкой на канвасе — есть что поправить?» После апрува всего текстового пакета отдельно выбирается метод отрисовки (фаза 2.0). В этой фазе вызовов Figma MCP не было.', 'Sitemap и три flow перенесены в Figma Design через use_figma, на отдельную страницу. Скриншоты всех четырёх схем проверены, наложения подписей и пересечения стрелок с блоками исправлены. [Ссылки и проверка](../figma-delivery.md). Текстовые исходники остаются в ia/; при изменениях синхронизировать их с канвасом.'),
        ],
        'ia/sitemap.md': [
            ('Это исправление ранее согласованной структуры; обновлённый flow анализа ожидает согласования вместе с двумя другими flow.', 'Это исправление ранее согласованной структуры; после него пользователь подтвердил перенос sitemap и всех трёх flow в Dashboard.'),
            ('Приоритеты согласованы. Пользователь выбрал все три сценария; [user flows](flows/README.md) подготовлены для согласования в фазе 1.4. До апрува всего текстового пакета Figma MCP не вызывается; в этой фазе вызовов не было.', 'Директива выполнена: sitemap и [три user flow](flows/README.md) согласованы, отрисованы на отдельной странице Dashboard и проверены. [Ссылки на фреймы](figma-delivery.md). При изменениях поддерживать соответствие канваса текстовым исходникам.'),
        ],
        'ia/screens-inventory.md': [
            ('Переходы user flow остаются на согласовании.', 'Затем пользователь подтвердил перенос sitemap и трёх user flow в Dashboard; отрисовка завершена.'),
            ('Три [user flow](flows/README.md) подготовлены и ожидают согласования; Figma MCP в рамках этой директивы не вызывался.', 'Три [user flow](flows/README.md) согласованы и вместе с sitemap отрисованы в Figma. [Готовые фреймы и проверка](figma-delivery.md).'),
        ],
    }
    pending = {}
    for relative, pairs in changes.items():
        path=ROOT/relative
        content=path.read_text(encoding='utf-8')
        for old,new in pairs:
            if new in content and old not in content: continue
            assert content.count(old)==1, relative
            content=content.replace(old,new,1)
        pending[path]=content
    report='''# Sitemap и user flows в Figma

Директива directive_prd_to_sitemap выполнена. Пользователь подтвердил перенос в существующий Dashboard через use_figma после правки входа в результаты на ResultsOverview.

Страница: **UX-Lab · Sitemap & User Flows** (8:2). Формат: редактируемые блоки, текст и векторные стрелки в Figma Design. Номера на стрелках соотносятся с полными условиями справа. Это схемы архитектуры и переходов, не wireframes интерфейса.

| Схема | Фрейм | Проверено |
| --- | --- | --- |
'''
    for title,node,check in [
        ('Sitemap','9-2','25 узлов дерева, 24 связи, 17 состояний/режимов, 6 расширений; приоритеты цветом и текстом'),
        ('Запуск исследования','10-2','7 экранов, 11 переходов'),
        ('Прохождение участником','10-64','4 экрана, 7 переходов'),
        ('Анализ результатов','10-105','9 экранов, 19 переходов; Studies → ResultsOverview'),
    ]:
        report+=f'| {title} | [Открыть]({LINK}{node}) | {check} |\n'
    report+='''
Все четыре фрейма прочитаны обратно и проверены скриншотами. Исправлены высота текста после resize, отступы sitemap, маршрут напрямую к участникам в обход блока Funnel и раздельные петли PDF. Выходов за границы фреймов при проверке не обнаружено. Существующие страницы Page 1 и Greeting не изменялись.

Подготовка: `execution/prepare_figma_ia.py` формирует JS-мост для Plugin API из текущих Markdown/Mermaid. Он не вызывает Figma сам; подготовленные payloads сохраняются в `.tmp/figma-ia/`. Рендерер отказывается создавать повторный фрейм с тем же именем. Генераторы предыдущих фаз сохраняют историю процесса; не запускать их поверх финальных документов без проверки статусов и диффа.

Исходники — `ia/sitemap.md` и `ia/flows/*.mmd`. Изменения структуры сначала вносить в них, затем синхронизировать канвас. Самостоятельные правки в Figma требуют обратной сверки с текстом.

## Контрольные суммы исходников на момент передачи

'''
    for relative in ['ia/sitemap.md','ia/flows/study-launch.mmd','ia/flows/participant-test.mmd','ia/flows/results-analysis.mmd']:
        path=ROOT/relative
        content=pending.get(path,path.read_text(encoding='utf-8'))
        report+=f'- `{relative}`: `{hashlib.sha256(content.encode()).hexdigest()}`\n'
    pending[ROOT/'ia/figma-delivery.md']=report
    for path,content in pending.items():
        path.write_text(content,encoding='utf-8',newline='\n')
        assert path.read_text(encoding='utf-8')==content
    print('Recorded verified delivery, frame links and final IA status.')


if __name__=='__main__':main()
