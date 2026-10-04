"""Generate targeted Figma patches and keep the approved modal/navigation in docs."""
from pathlib import Path
import json
from build_wireframes import RENDER, contextual_sidebar
from build_project_wireframes import project_modal, MODAL_JS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/project-wireframes'
HELPERS=RENDER[RENDER.index('await figma.loadFontAsync'):RENDER.index('const title=')]
PAGE="const p=await figma.getNodeByIdAsync('20:2');await figma.setCurrentPageAsync(p);\n"
CHECK=r'''
const issues=[];for(const n of [f,...f.findAllWithCriteria({types:['FRAME']})])for(const c of n.children)if(c.visible&&(c.x<0||c.y<0||c.x+c.width>n.width+1||c.y+c.height>n.height+1))issues.push({id:c.id,parent:n.name,child:c.name});
return {frameId:f.id,createdNodeIds:ids,mutatedNodeIds:changed,removedNodeIds:removed,overflow:issues};
'''
FRAMES={'ResultsOverview':'22:3','Heatmaps':'22:95','Funnel':'24:3','Replay':'24:93','SuccessCriteria':'24:173','Projects':'31:3','Studies':'31:70','StudySetup':'32:3','Launch':'32:94'}

modal=PAGE+HELPERS+"const DATA="+json.dumps({'modal':project_modal()},ensure_ascii=False)+r''';
const f=await figma.getNodeByIdAsync('31:3');
if(f.findAllWithCriteria({types:['FRAME']}).some(n=>n.name==='CreateProjectModal'))throw new Error('Modal exists: inspect before modifying');
for(const n of f.findAllWithCriteria({types:['TEXT']}))for(const seg of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
const removed=[],changed=[];
const old=f.findAllWithCriteria({types:['FRAME']}).find(n=>n.name==='CreateProjectPanel');
if(!old)throw new Error('Original panel missing');
removed.push(old.id,...old.findAll(()=>true).map(n=>n.id));old.remove();
function width(n,w){n.resize(w,n.height);if(n.type==='TEXT')n.textAutoResize='HEIGHT';changed.push(n.id);}
const listing=f.findAllWithCriteria({types:['FRAME']}).find(n=>n.name==='ProjectsList');width(listing,1616);listing.primaryAxisSizingMode='AUTO';
const table=listing.children[0];width(table,1616);table.primaryAxisSizingMode='AUTO';
for(const r of table.children){width(r,1616);r.children.forEach((c,i)=>width(c,[804,244,244,260][i]));}
width(listing.children[1],1616);
'''+MODAL_JS+CHECK
(OUT/'fix-modal.js').write_text(modal,encoding='utf-8')
for name,node in FRAMES.items():
    code=PAGE+HELPERS+'const DATA='+json.dumps(contextual_sidebar(name),ensure_ascii=False)+';\n'+f"const f=await figma.getNodeByIdAsync('{node}');"+r'''
const sidebar=f.findAllWithCriteria({types:['FRAME']}).find(n=>n.name==='Sidebar');
const changed=[sidebar.id],removed=[];
for(const n of sidebar.findAllWithCriteria({types:['TEXT']}))for(const seg of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
for(const n of [...sidebar.children]){removed.push(n.id,...('children' in n?n.findAll(()=>true).map(c=>c.id):[]));n.remove();}
sidebar.itemSpacing=12;sidebar.paddingTop=sidebar.paddingBottom=sidebar.paddingLeft=sidebar.paddingRight=24;
for(const d of DATA.children)make(sidebar,d);
const h=f.children.find(n=>n.name==='Header');const link=h.children[1];
for(const seg of link.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
link.characters='Все проекты';changed.push(link.id);
'''+CHECK
    (OUT/f'nav-{name}.js').write_text(code,encoding='utf-8')

replacements=[
 ('ProjectsList 1016 px','ProjectsList 1616 px'),
 ('CreateProjectPanel 576 px справа, промежуток 24 px. Показано состояние после нажатия «Создать проект»: обязательное название, необязательное описание, действия создать/отмена.', 'CreateProjectModal шириной 640 px по центру экрана поверх списка проектов; белый фон, отступы 32 px. Под ним ModalBackdrop на весь экран: #1A1A1A с непрозрачностью 40%. Вверху заголовок и крестик. Далее обязательное название, необязательное описание и действия «Отмена» / «Создать проект».'),
 ('Отмена закрывает форму без создания. Пока форма закрыта, список может занимать ширину Main.', 'Отмена, крестик и Escape закрывают модалку без создания и возвращают фокус кнопке «Создать проект». Фон недоступен для взаимодействия; фокус остаётся внутри диалога. Список занимает всю ширину Main независимо от модалки.'),
 ('Панель создания с названием и описанием.', 'Модальное окно по центру с названием и описанием.'),
 ('Панель создания проекта, обязательное название', 'Модальное окно создания проекта, обязательное название'),
 ('В Projects показана открытая форма создания;', 'В Projects показана открытая модалка создания по центру с затемнением фона;'),
]
for rel in ['ia/wireframes/Projects.md','execution/record_project_wireframes.py','ia/sitemap.md','ia/screens-inventory.md','ia/wireframes/projects-delivery.md']:
    p=ROOT/rel;text=p.read_text(encoding='utf-8')
    for old,new in replacements:text=text.replace(old,new)
    p.write_text(text,encoding='utf-8',newline='\n')
navdoc='''# Общая навигация wireframes

Уточнение 21 сентября 2026 после замечания пользователя о несогласованных меню. Sidebar одинаковой ширины 240 px на всех девяти экранах. Общий порядок:

1. Рабочее пространство → Все проекты.
2. Проект: название или «Не выбран» → Исследования проекта.
3. Исследование: название или «Не выбрано» → Настройка исследования → Проверка и запуск → Обзор результатов → Тепловая карта → Воронка → Участники → Сигналы затруднений → Отчёт PDF.

Все десять пунктов видны на каждом экране в одинаковом порядке и на одинаковых позициях. До выбора проекта/исследования связанные пункты неактивны (непрозрачность 45%), под меню показано объяснение. Блоки контекста фиксированной высоты сохраняют положение пунктов. Активен пункт текущего экрана; Replay относится к участникам, SuccessCriteria — к настройке исследования. При переходе к результатам открывается обзор. В шапке всех экранов единая ссылка «Все проекты». Это уточнение заменяет прежнее скрытие пунктов.

На экране Projects после «Создать проект» открывается модалка 640 px по центру всего фрейма, с непрозрачным белым фоном и затемнением списка. Боковая форма удалена. Создание успешно ведёт внутрь нового проекта; Отмена/крестик/Escape возвращают к списку без создания. При реализации нужен фокус внутри диалога и его возврат к кнопке открытия. В wireframe эти правила описаны, рабочие интеракции не реализованы.
'''
(ROOT/'ia/wireframes/navigation.md').write_text(navdoc,encoding='utf-8',newline='\n')
for name in FRAMES:
    p=ROOT/f'ia/wireframes/{name}.md';text=p.read_text(encoding='utf-8')
    if '## Единая навигация' not in text:
        text+='\n## Единая навигация\n\nSidebar обновлён по [общей схеме](navigation.md): рабочее пространство, выбранный проект, открытое исследование. Эта схема заменяет прежний перечень пунктов Sidebar выше.\n'
        p.write_text(text,encoding='utf-8',newline='\n')
print('Prepared centered modal patch, nine navigation patches and synchronized sources.')
