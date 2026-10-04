"""Rebuild approved wireframe content using linked UI-kit components.

Each screen payload is executed separately. Sources are a read-only compact export
of the current Figma wireframes, not the earlier, superseded generator output.
"""
import json
import re
import sys
from pathlib import Path
from build_final_results import BASE

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'.tmp/final-pack'
SOURCES=json.loads((TMP/'sources.json').read_text(encoding='utf-8'))

SETUP=r'''
figma.skipInvisibleInstanceChildren=false;
const surfaceRadius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
function surface(n){n.strokesIncludedInLayout=false;fill(n,'background/surface');n.strokes=[paint('border/subtle')];for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(k,surfaceRadius);}
function property(set,k){return Object.keys(set.componentPropertyDefinitions).find(x=>x.startsWith(k+'#'));}
async function instance(id,parent,name,width){const master=await figma.getNodeByIdAsync(id);if(!master)throw Error('Missing master '+id);await fonts(master);const n=master.createInstance();created.push(n.id);parent.appendChild(n);n.name=name;await fonts(n);n.resize(width,n.height);return n;}
'''

FIELDS=r'''
await figma.setCurrentPageAsync(page);
const prior=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ProductField');if(prior)return {setId:prior.id,existing:true};
const source=await figma.importComponentSetByKeyAsync('c9bc49b3e9b9c85ac1d72917b84d94320ff84577');
const sec=figma.createSection();page.appendChild(sec);created.push(sec.id);sec.name='UI Kit — forms';sec.x=12600;sec.y=80;sec.resizeWithoutConstraints(2200,2700);fill(sec,'background/canvas');
const variants=[],links=[];
for(const type of ['Text','Textarea','Select','Search','Password'])for(const state of ['Default','Focus','Invalid','Disabled']){
 const c=component('Type='+type+', State='+state,sec,480);c.strokes=[];c.fills=[];c.paddingLeft=0;c.paddingRight=0;c.paddingTop=0;c.paddingBottom=0;for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])c.setBoundVariable(k,null);
 const label=await text(c,'Label','Название','small','text/secondary');links.push({n:label,k:'Label',type:'TEXT',value:'Название'});
 const sample=source.children.find(n=>{const v=n.variantProperties;return v.Type===type&&v.Compressed==='False'&&v.State===(state==='Default'?'Filled':state)&&v['Prepend / Append']==='None'&&v.Icon===(type==='Select'?'Right':['Search','Password'].includes(type)?'Left':'None')&&v.Loading==='False'&&v.Clearble==='False';});if(!sample)throw Error('Source field '+type+' '+state);
 const input=sample.createInstance();c.appendChild(input);created.push(input.id);input.name='Control';await theme(input,state==='Disabled'?'text/secondary':'text/primary','background/surface');input.resize(480,type==='Textarea'?112:40);full(input);radii(input);
 for(const n of [input,...input.findAll()])if('strokes'in n&&n.strokes.length)n.strokes=[paint(state==='Invalid'?'status/error/text':state==='Focus'?'border/focus':'border/control')];
 const val=input.findOne(n=>n.type==='TEXT'&&n.visible);await val.setTextStyleIdAsync(styles.body.id);val.characters='Значение';val.name='InputValue';
 const help=await text(c,'Help',state==='Invalid'?'Проверьте значение поля':'Пояснение к полю','small',state==='Invalid'?'status/error/text':'text/secondary');help.visible=state==='Invalid';links.push({n:help,k:'Help',type:'TEXT',value:'Пояснение к полю'});links.push({n:help,k:'ShowHelp',type:'BOOLEAN',value:false});variants.push(c);
}
const set=figma.combineAsVariants(variants,sec);set.name='ProductField';set.x=32;set.y=48;created.push(set.id);set.layoutMode='HORIZONTAL';set.layoutWrap='WRAP';set.resize(2100,2500);set.primaryAxisSizingMode='FIXED';set.counterAxisSizingMode='AUTO';spacing(set,'lg');set.setBoundVariable('counterAxisSpacing',dimensions.lg);
const keys={};for(const l of links){if(!keys[l.k])keys[l.k]=set.addComponentProperty(l.k,l.type,l.value);l.n.componentPropertyReferences={...(l.n.componentPropertyReferences||{}),[l.type==='BOOLEAN'?'visible':'characters']:keys[l.k]};}
set.description='Product form field. Reuses the selected Elastic UI generation, with local semantic colors. Text / Textarea / Select / Search / Password, Default / Focus / Invalid / Disabled. Source legacy marker remains documented; no silent migration to Borealis.';
return {setId:set.id,name:set.name,variants:set.children.map(n=>({id:n.id,name:n.name})),createdNodeIds:[...new Set(created.concat(sec.findAll().map(n=>n.id)))]};
'''

ROWS=r'''
await figma.setCurrentPageAsync(page);
const prior=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ResearchTableRow');if(prior)return {setId:prior.id,existing:true};
const source=await figma.importComponentByKeyAsync('f4f1e5fb207951d41838bf017236a474d33cbd13');
const sec=figma.createSection();page.appendChild(sec);created.push(sec.id);sec.name='UI Kit — research tables';sec.x=14900;sec.y=80;sec.resizeWithoutConstraints(1750,4500);fill(sec,'background/canvas');
const variants=[],links=[];
for(const count of [2,3,4,5,6,7,8])for(const state of ['Default','Zebra','Selected','Header']){
 const c=component('Columns='+count+', State='+state,sec,1536);c.layoutMode='HORIZONTAL';c.resize(1536,state==='Header'?48:80);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';c.strokes=[];c.cornerRadius=0;for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])c.setBoundVariable(k,null);for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom']){c.setBoundVariable(k,null);c[k]=0;}c.itemSpacing=0;c.setBoundVariable('itemSpacing',null);fill(c,state==='Selected'?'accent/soft':state==='Header'?'background/sidebar':state==='Zebra'?'background/subtle':'background/surface');
 for(let i=0;i<count;i++){
  const cell=source.createInstance();c.appendChild(cell);created.push(cell.id);cell.name='Cell'+i;await theme(cell,'text/primary');cell.fills=[];for(const d of cell.findAll())if(d.type!=='TEXT'&&'fills'in d)d.fills=[];
  const border=cell.findOne(n=>n.name==='Border bottom');if(border)border.visible=false;
  cell.resize(1536/count,c.height);cell.layoutSizingVertical='FILL';const label=cell.findOne(n=>n.type==='TEXT');await label.setTextStyleIdAsync(styles[state==='Header'?'small':'body'].id);fill(label,state==='Header'?'text/secondary':'text/primary');label.characters='Значение';label.textAutoResize='HEIGHT';label.name='CellValue';
 }
 variants.push(c);
}
const set=figma.combineAsVariants(variants,sec);set.name='ResearchTableRow';set.x=48;set.y=48;created.push(set.id);set.layoutMode='VERTICAL';set.primaryAxisSizingMode='AUTO';set.counterAxisSizingMode='FIXED';spacing(set,'base');set.resize(1536,set.height);
const keys={};for(const l of links){if(!keys[l.k])keys[l.k]=set.addComponentProperty(l.k,l.type,l.value);l.n.componentPropertyReferences={characters:keys[l.k]};}set.description='Research data row composed of linked Elastic Table Cell instances. Column widths adapt to each table; zebra, header and selected surfaces use semantic tokens. For participant rows use ParticipantRow instead.';
return {setId:set.id,name:set.name,variants:set.children.map(n=>({id:n.id,name:n.name})),createdNodeIds:[...new Set(created.concat(sec.findAll().map(n=>n.id)))]};
'''

RENDER=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const existing=figma.currentPage.findOne(n=>n.type==='FRAME'&&n.name==='Screen/'+SPEC.n);if(existing)return {screenId:existing.id,name:SPEC.n,existing:true};
const fieldSet=await figma.getNodeByIdAsync(FIELD_ID),rowSet=await figma.getNodeByIdAsync(ROW_ID),metricSet=await figma.getNodeByIdAsync('171:1801');
const section=await figma.getNodeByIdAsync('175:613');
function strings(n){return n.v!==undefined?[n.v]:(n.c||[]).flatMap(strings);}
function find(n,name){if(n.n===name)return n;for(const c of n.c||[]){const r=find(c,name);if(r)return r;}return null;}
function space(n){return n<=4?'xs':n<=8?'sm':n<=12?'md':n<=16?'base':n<=24?'lg':'xl';}
const used=new Set();
async function use(id,parent,name,width){used.add(id);return instance(id,parent,name,width);}
async function fitReplay(n){
 const inner=n.width-n.paddingLeft-n.paddingRight;
 for(const c of n.children){if(!('width'in c))continue;const old=c.width;const ratio=inner/old;
  
  c.layoutSizingHorizontal='FILL';c.resize(inner,c.height);
 }
 
 n.primaryAxisSizingMode='AUTO';return n;
}
async function action(parent,label,width,primary=false){const filter=/^(Сценарий:|Устройство:|Страница:|Состояние:|Исход:|Сигнал:|Данные:|Все статусы|Все исходы|Все данные|Скорость:)/.test(label);const b=await button(parent,label,primary?'Primary':'Secondary',Math.max(64,width),filter?iconKeys.down:null,filter);used.add('125:450');return b;}
async function dataRow(s,parent,w,index){const count=(s.c||[]).length;if(count<2||count>8)return null;const header=s.n==='TableHeader';const selected=strings(s).join(' ').includes('Выбранный');const state=header?'Header':selected?'Selected':index%2===0?'Zebra':'Default';const master=rowSet.children.find(n=>n.variantProperties.Columns===String(count)&&n.variantProperties.State===state);const row=await use(master.id,parent,s.n,w);const props={};for(let i=0;i<count;i++)props[property(rowSet,'Cell'+i)]=strings(s.c[i]).join('\n');let widths=s.c.map(x=>x.w||100);const sum=widths.reduce((a,b)=>a+b,0);let height=header?48:Math.max(80,Math.min(112,s.h));row.resize(w,height);for(let i=0;i<count;i++){const cell=row.children[i];cell.layoutSizingHorizontal='FIXED';cell.resize(w*widths[i]/sum,height);cell.layoutSizingVertical='FILL';const label=cell.findOne(n=>n.type==='TEXT');label.characters=strings(s.c[i]).join('\n');label.textAutoResize='HEIGHT';const inner=cell.findOne(n=>n.name==='Cell');if(inner){inner.resize(cell.width,height);inner.layoutSizingVertical='FILL';inner.counterAxisAlignItems='CENTER';}const val=strings(s.c[i]).join(' ');if(!header&&i===count-1&&/Открыть|Результаты|Выбрать|Продолжить|Изменить/.test(val)){fill(label,'accent/strong');await label.setTextStyleIdAsync(styles.medium.id);}}return row;}
async function render(s,parent,w,index=0){
 if(['PlayerControls','ReplayCursor','HeatLayer'].includes(s.n)||s.t==='VECTOR')return null;
 const val=strings(s).join('\n');
 if(s.n==='ParticipantsTable'){const n=await use('153:702',parent,s.n,w);n.layoutSizingVertical='HUG';return n;}
 if(s.n==='Timeline')return fitReplay(await use(SPEC.n==='ReplayIncomplete'?'84:678':'84:642',parent,'ReplayControls',w));
 if(s.n==='Metric'){
  const n=await use('171:1764',parent,'SummaryMetric',w);const ts=strings(s);n.setProperties({[property(metricSet,'Label')]:ts[0]||'Показатель',[property(metricSet,'Value')]:ts[1]||'—',[property(metricSet,'Hint')]:ts[2]||'',[property(metricSet,'Detail')]:'',[property(metricSet,'ShowBadge')]:false,[property(metricSet,'ShowProgress')]:false,[property(metricSet,'ShowLink')]:false});n.resize(w,144);return n;
 }
 if(s.n==='Action'&&val==='Отправить заказ'&&parent.name==='FormPreview'){const b=await action(parent,val,w,true);const ctl=b.children.find(n=>n.name==='Control');ctl.fills=[paint('demo/storefront/action')];return b;}
 if(s.n==='Action'||s.n==='SaveObservation'||s.n==='CloseButton')return action(parent,val,w,/^(Создать|Запустить|Сохранить|Начать|Отправить|Продолжить|Войти|Скачать)/.test(val));
 if(s.n==='Field'||s.n==='FormField'||s.n==='Input'){
  const ts=strings(s);let label=s.n==='Input'?'':ts[0]||'Поле',value=s.n==='Input'?ts.join('\n'):ts.slice(1).join('\n');
  const type=/парол/i.test(label)?'Password':/Найти|Поиск/i.test(label)?'Search':/Режим|Тип условия|Статус|Устройство|Сценарий/.test(label)?'Select':s.h>110||/Описание|Текст задания|Наблюдение/.test(label)?'Textarea':'Text';
  const master=fieldSet.children.find(n=>n.variantProperties.Type===type&&n.variantProperties.State==='Default');const n=await use(master.id,parent,'Field/'+label,w);n.setProperties({[property(fieldSet,'Label')]:label,[property(fieldSet,'ShowHelp')]:false});n.findOne(x=>x.name==='InputValue').characters=value||'Введите значение';if(!label)n.findOne(x=>x.name==='Label').visible=false;n.layoutSizingVertical='HUG';return n;
 }
 if(s.n==='TableHeader'||/^TableRow\d/.test(s.n)){const n=await dataRow(s,parent,w,index);if(n)return n;}
 if(s.t==='TEXT'){
  if(/^Участники 1–4 из 16/.test(s.v)&&find(SPEC,'ParticipantsTable'))return null;
  if(/^Меньше кликов →/.test(s.v)){const n=await use(SPEC.n==='HeatmapsFirstClick'?'83:712':'83:694',parent,'HeatmapLegend',w);const sample=n.findOne(x=>x.type==='TEXT'&&x.name==='SampleBase');if(sample)sample.characters=SPEC.n==='HeatmapsFirstClick'?'18 первых кликов · 18 участников':'98 кликов · 18 участников';return n;}
  return text(parent,s.n,s.v,s.sz>=24?'heading':s.m?'medium':s.sz<=15?'small':'body',s.sz<=15?'text/secondary':'text/primary');
 }
 if(s.t==='INSTANCE')return action(parent,val,w);
 if(s.t==='RECTANGLE')return null;
 const dir=s.d==='HORIZONTAL'?'HORIZONTAL':'VERTICAL';
 const n=frame(s.n,parent,dir,w);n.clipsContent=false;
 const isTable=/Table$/.test(s.n)||(s.c||[]).filter(c=>/^TableRow\d/.test(c.n)).length>1;const isSurface=isTable||!!s.b||/Panel$|EmptyState|Notice|TaskOne|TaskTwo|StepOne|StepTwo|StepThree|RuleSummary|ReportPreview|ReportSettings|FindingDrawer/.test(s.n);
 const pad=s.n==='OrderPreview'?24:isTable?0:isSurface?(w<450?16:24):s.p?Math.min(s.p,24):0;
 if(pad)spacing(n,'base',space(pad));else spacing(n,space(s.g||8));
 if(isSurface){surface(n);const effect=(await figma.getLocalEffectStylesAsync()).find(e=>e.name==='shadow/card');if(effect)await n.setEffectStyleIdAsync(effect.id);}
 else if(s.f){fill(n,'background/subtle');radii(n);}
 if(s.n==='OrderPreview'){surface(n);fill(n,'background/sidebar');spacing(n,'lg','lg');}
 if(isTable){n.setBoundVariable('itemSpacing',null);n.itemSpacing=0;n.clipsContent=true;}let children=(s.c||[]).filter(x=>!['PlayerControls','ReplayCursor','HeatLayer'].includes(x.n)&&x.t!=='VECTOR');
 const inner=w-2*pad;
 if(dir==='HORIZONTAL'){
  n.counterAxisAlignItems=/Heading|Actions|Toolbar|Context|Navigation/.test(s.n)?'CENTER':'MIN';
  const total=children.reduce((a,c)=>a+(c.w||100),0);const avail=inner-Math.max(0,children.length-1)*n.itemSpacing;
  for(let i=0;i<children.length;i++){const c=children[i];let cw=Math.max(48,avail*(c.w||100)/total);if(children.length===1)cw=inner;const rendered=await render(c,n,cw,i);if(rendered){rendered.layoutSizingHorizontal='FIXED';rendered.resize(cw,rendered.height);}}
 }else for(let i=0;i<children.length;i++){const c=children[i];const rendered=await render(c,n,inner,i);if(rendered)full(rendered);}
 if(s.n==='ProductImage'){n.minHeight=180;fill(n,'accent/soft');const ic=await figma.importComponentByKeyAsync('42e022270b024bb7c555a9da44ccad19c84e29b6');const pic=ic.createInstance();n.insertChild(0,pic);created.push(pic.id);await theme(pic,'accent/strong');pic.resize(48,48);n.primaryAxisAlignItems='CENTER';n.counterAxisAlignItems='CENTER';}
 if(s.n==='PrototypePlaceholder'&&SPEC.n.startsWith('Heatmaps')){
  const overlay=frame('Demo click layer',n,'HORIZONTAL',inner);overlay.layoutPositioning='ABSOLUTE';overlay.resize(inner,Math.max(160,n.height-40));overlay.x=pad;overlay.y=pad;overlay.fills=[];overlay.clipsContent=false;
  for(const [x,y,size,a] of [[.7,.74,74,.3],[.73,.79,44,.4],[.28,.42,44,.2],[.64,.36,36,.2],[.79,.68,40,.3]]){const e=figma.createEllipse();overlay.appendChild(e);created.push(e.id);e.name='Illustrative click density';e.layoutPositioning='ABSOLUTE';e.resize(size,size);e.x=inner*x;e.y=overlay.height*y;fill(e,'heatmap/intensity/8');e.opacity=a;}
 }
 return n;
}
const mobile=SPEC.w<600,participant=!find(SPEC,'Main');
const screen=frame('Screen/'+SPEC.n,section,'HORIZONTAL',SPEC.w);screen.resize(SPEC.w,SPEC.h);screen.primaryAxisSizingMode='FIXED';screen.counterAxisSizingMode='FIXED';screen.itemSpacing=0;screen.clipsContent=true;fill(screen,'background/canvas');screen.x=80+(POSITION%5)*2080;screen.y=80+Math.floor(POSITION/5)*1260;
let main;
if(!participant){
 const navMap={Projects:'153:1609',ProjectsDefault:'153:1609',ProjectsEmpty:'153:1609',Studies:'153:1637',StudiesEmpty:'153:1637'};
 const navID=navMap[SPEC.n]||(/Heatmap/.test(SPEC.n)&&!/^Participants/.test(SPEC.n)?'153:2097':SPEC.n==='Funnel'?'153:2233':/Replay|ParticipantDetails|^Participants|FindingEditor|FindingSaved/.test(SPEC.n)?'153:2369':/^Signals|^Finding/.test(SPEC.n)?'153:2505':/^Report/.test(SPEC.n)?'153:2641':/^Launch|ConnectionError|ControlResult/.test(SPEC.n)?'153:1825':/^Results/.test(SPEC.n)?'153:1961':'153:1677');
 const nav=await use(navID,screen,'Sidebar',320);nav.resize(320,SPEC.h);
 const workspace=full(frame('Workspace',screen,'VERTICAL',1600));workspace.layoutSizingVertical='FILL';workspace.itemSpacing=0;
 const header=full(frame('Header',workspace,'HORIZONTAL',1600,'xl'));header.resize(1600,64);header.counterAxisSizingMode='FIXED';header.counterAxisAlignItems='CENTER';header.paddingTop=0;header.paddingBottom=0;header.setBoundVariable('paddingTop',null);header.setBoundVariable('paddingBottom',null);fill(header,'background/surface');await text(header,'Breadcrumb',/^Projects/.test(SPEC.n)?'Рабочее пространство команды':'Все проекты  /  Интернет-магазин'+(/^Studies/.test(SPEC.n)?'':'  /  Покупка в интернет-магазине'),'small','text/secondary');const colleague=await text(header,'Account','Коллега','small','text/secondary');colleague.layoutSizingHorizontal='FIXED';colleague.resize(100,24);colleague.textAlignHorizontal='RIGHT';
 main=full(frame('Main',workspace,'VERTICAL',1600,'xl'));main.layoutSizingVertical='FILL';main.clipsContent=true;main.overflowDirection='VERTICAL';spacing(main,'lg','xl');
 const original=find(SPEC,'Main');for(let i=0;i<original.c.length;i++){const n=await render(original.c[i],main,1536,i);if(n)full(n);}
}else{
 screen.layoutMode='VERTICAL';const head=full(frame('ParticipantHeader',screen,'HORIZONTAL',SPEC.w,'base'));head.resize(SPEC.w,64);head.counterAxisSizingMode='FIXED';fill(head,'background/surface');await text(head,'Brand','UX-Lab','medium');
 const body=full(frame('ParticipantBody',screen,'VERTICAL',SPEC.w,mobile?'base':'xl'));body.layoutSizingVertical='FILL';body.counterAxisAlignItems='CENTER';body.clipsContent=true;body.overflowDirection='VERTICAL';
 const src=SPEC.c.find(c=>c.n==='ParticipantContent')||SPEC.c.find(c=>c.n!=='ParticipantHeader');main=await render(src,body,mobile?358:Math.min(src.w||800,1100));
}
for(const overlay of SPEC.c.filter(c=>!participant&&c.a&&!['ParticipantContent'].includes(c.n)&&c.t!=='RECTANGLE')){
 const wrap=frame(overlay.n,screen,'VERTICAL',overlay.w);wrap.layoutPositioning='ABSOLUTE';wrap.resize(SPEC.w,SPEC.h);wrap.x=0;wrap.y=0;wrap.primaryAxisSizingMode='FIXED';wrap.counterAxisSizingMode='FIXED';wrap.primaryAxisAlignItems='CENTER';wrap.counterAxisAlignItems='CENTER';wrap.fills=[];const dim=frame('ModalScrim',wrap,'HORIZONTAL',SPEC.w);dim.layoutPositioning='ABSOLUTE';dim.resize(SPEC.w,SPEC.h);dim.primaryAxisSizingMode='FIXED';dim.counterAxisSizingMode='FIXED';dim.x=0;dim.y=0;fill(dim,'text/primary');dim.opacity=.35;
 const drawer=overlay.n==='FindingOverlay'?find(overlay,'FindingDrawer'):null;
 if(drawer){wrap.counterAxisAlignItems='MAX';const n=await render(drawer,wrap,736);n.resize(736,SPEC.h);n.primaryAxisSizingMode='FIXED';n.clipsContent=true;n.overflowDirection='VERTICAL';}
 else {const n=await render(overlay,wrap,Math.min(overlay.w,720));surface(n);}
}
section.resizeWithoutConstraints(10480,Math.max(section.height,screen.y+screen.height+80));
return {screenId:screen.id,name:SPEC.n,sourceId:SOURCE_ID,usedComponentIds:[...used],width:screen.width,height:screen.height,createdNodeIds:[...new Set(created.concat(screen.findAll().map(n=>n.id)))],mutatedNodeIds:[section.id]};
'''

def slug(name):
    return re.sub(r'(?<!^)(?=[A-Z])','-',name).lower()

def main():
    stage=sys.argv[1]
    if stage=='maps':
        manifest=json.loads((ROOT/'ia/wireframes/complete-manifest.json').read_text(encoding='utf-8'))
        ids={f['name']:f['id'] for f in manifest['frames']}
        def walk(n):
            yield n
            for c in n.get('c',[]):yield from walk(c)
        for s in SOURCES:
            if s['n']=='ResultsOverview':continue
            nodes=list(walk(s));m=next((n for n in nodes if n['n']=='Main'),s)
            lines=[f"# Screen/{s['n']}","",'Статус: composition map; сборка разрешена пользователем для всего пакета без повторного апрува.',"",f"Источник: [wireframe](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id={ids[s['n']].replace(':','-')}). Размер {s['w']} × {s['h']}. Целевая страница: UX-Lab · Final Screens (191:847).","",'## Композиция',""]
            for c in m.get('c',[]):lines.append(f"- {c['n']}: утверждённые тексты и действия из актуального wireframe.")
            lines+=['','## Компоненты и оформление','','NavMenu и ProductButton; ProductField для полей; ResearchTableRow с ячейками Elastic для таблиц. ParticipantsTable, ReplayControls, HeatmapLegend и SummaryMetric используются для соответствующих аналитических блоков. Контейнеры — Auto Layout; цвета и геометрия — Variables, тексты — Text Styles. Радиус крупных поверхностей 12 px. Secondary использует утверждённый A без контура и токены action/secondary/*. Вопрос Tertiary остаётся отложенным.','','## Проверка','','После сборки: видимый скриншот, ширина, переносы, привязки и сохранность текста. Данные демонстрационные. Состояния empty/error/mobile представлены отдельными экранами исходного пакета. Кликабельные связи не считаются готовыми без отдельной проверки.']
            (ROOT/'ds/screens'/f'{slug(s["n"])}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        print(json.dumps({'maps':len(SOURCES)-1}));return
    if stage in ['fields','rows']:code=BASE+SETUP+{'fields':FIELDS,'rows':ROWS}[stage]
    else:
        name=sys.argv[2];s=next(s for s in SOURCES if s['n']==name);manifest=json.loads((ROOT/'ia/wireframes/complete-manifest.json').read_text(encoding='utf-8'));source=next(f for f in manifest['frames'] if f['name']==name)
        ids=json.loads((TMP/'components.json').read_text(encoding='utf-8'))
        pre=f'const SPEC={json.dumps(s,ensure_ascii=False)};const POSITION={SOURCES.index(s)};const SOURCE_ID={json.dumps(source["id"])};const FIELD_ID={json.dumps(ids["field"])};const ROW_ID={json.dumps(ids["row"])};\n'
        code=BASE+SETUP+pre+RENDER
    (TMP/f'{stage}-{sys.argv[2] if len(sys.argv)>2 else "components"}.js').write_text(code,encoding='utf-8')
    print(json.dumps({'code':code},ensure_ascii=False))

if __name__=='__main__':main()
