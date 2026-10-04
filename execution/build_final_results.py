"""Incremental Figma payloads for the approved ResultsOverview composition."""
import json
import sys
from pathlib import Path
from grow_ui_kit import COMMON
from build_analytics_components import THEME

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp/final-results'

BASE = COMMON + THEME + r'''
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.id,v]));
function resolved(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolved(vars[x.id]):x;}
function paint(key){const v=colors[key];if(!v)throw Error('Missing '+key);const x=resolved(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
for(const [k,key]of Object.entries({heading:'a0fb5401c910ccd1871625995412cdd09c8f0c3b',h3:'638cf4b32a8c492fa5e4cd6f99bfe69529e93a3d'})){styles[k]=await figma.importStyleByKeyAsync(key);await figma.loadFontAsync(styles[k].fontName);}
const mutated=[];
function full(n){n.layoutSizingHorizontal='FILL';return n;}
function hug(n){n.primaryAxisSizingMode='AUTO';return n;}
function propKey(s,name){const key=Object.keys(s.componentPropertyDefinitions).find(k=>k.startsWith(name+'#'));if(!key)throw Error('Property '+name);return key;}
async function button(parent,label,kind='Secondary',width=180,iconKey=null,right=false){
 const set=await figma.getNodeByIdAsync('125:450');const master=set.children.find(c=>c.variantProperties.Kind===kind&&c.variantProperties.State==='Default');
 const n=master.createInstance();created.push(n.id);parent.appendChild(n);await fonts(n);n.resize(width,40);n.name=label;
 const ctl=n.findOne(x=>x.type==='INSTANCE'&&x.name==='Control');ctl.setProperties({'Text#30956:4':label,'Icon left#30956:3':false,'Icon right#30956:5':false});
 if(iconKey){const ic=await figma.importComponentByKeyAsync(iconKey);ctl.setProperties(right?{'Icon right#30956:5':true,'⮑  Icon right#31056:0':ic.id}:{'Icon left#30956:3':true,'⮑  Icon left#30964:4':ic.id});}
 await theme(n,kind==='Primary'?'text/inverse':'text/primary',kind==='Primary'?'action/primary':kind==='Secondary'?'background/sidebar':'background/surface');
 if(kind==='Tertiary'){n.fills=[];ctl.fills=[];}return n;
}
const iconKeys={document:'989646b14b75559d38c73e2b550126a5f49c54b6',down:'ad886ce4521200a238ffe46f2c3be231e9925c81',heatmap:'e557d008bea964f44d9f20d2bded7e641d713f34',filter:'3b8f958cff3af9880ab1290cdf44659b29097ea0',users:'297df35096cfdd7b8c88a465d0cd8c485dcda540',flag:'21a80ed21bd18f9bcd29b9c0329a021d22c40065'};
'''

METRIC = r'''
await figma.setCurrentPageAsync(page);
const existing=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SummaryMetric');if(existing)return {existingSetId:existing.id};
let primitives=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name==='UX-Lab · Primitives');if(!primitives){primitives=figma.variables.createVariableCollection('UX-Lab · Primitives');primitives.renameMode(primitives.defaultModeId,'Value');}
let black=(await figma.variables.getLocalVariablesAsync('COLOR')).find(v=>v.name==='black/4%'&&v.variableCollectionId===primitives.id);if(!black){black=figma.variables.createVariable('black/4%',primitives,'COLOR');black.scopes=[];black.setValueForMode(primitives.defaultModeId,{r:0,g:0,b:0,a:0.04});black.setVariableCodeSyntax('WEB','var(--black-4-percent)');}
const collection=await figma.variables.getVariableCollectionByIdAsync(colors['text/primary'].variableCollectionId);
let shadowColor=colors['shadow/color'];if(!shadowColor){shadowColor=figma.variables.createVariable('shadow/color',collection,'COLOR');shadowColor.scopes=['EFFECT_COLOR'];shadowColor.setValueForMode(collection.defaultModeId,{type:'VARIABLE_ALIAS',id:black.id});shadowColor.setVariableCodeSyntax('WEB','var(--shadow-color)');}
let effect=(await figma.getLocalEffectStylesAsync()).find(s=>s.name==='shadow/card');if(!effect){effect=figma.createEffectStyle();effect.name='shadow/card';effect.effects=[figma.variables.setBoundVariableForEffect({type:'DROP_SHADOW',color:{r:0,g:0,b:0,a:0.04},offset:{x:0,y:2},radius:8,spread:0,visible:true,blendMode:'NORMAL'},'color',shadowColor)];}
const sec=figma.createSection();created.push(sec.id);page.appendChild(sec);sec.name='UI Kit — overview metrics';sec.x=10600;sec.y=950;sec.resizeWithoutConstraints(1760,360);fill(sec,'background/canvas');
const doc=frame('SummaryMetric documentation',sec,'VERTICAL',1696);doc.x=32;doc.y=40;await text(doc,'Title','SummaryMetric · Ready / Loading / NoData','heading');await text(doc,'Usage','Показатель исследования: название, значение, пояснение, необязательная ссылка. Цвета и типографика — общая ДС.','small','text/secondary');
const variants=[];const links=[];
for(const state of ['Ready','Loading','NoData']){
const c=component('State='+state,sec,496);spacing(c,'sm','base');c.resize(496,152);c.primaryAxisSizingMode='FIXED';await c.setEffectStyleIdAsync(effect.id);
const title=await text(c,'Label','Участников','body','text/secondary');const val=await text(c,'Value',state==='Ready'?'20':state==='Loading'?'Загрузка…':'Нет данных','heading');const hint=await text(c,'Hint','Уникальных в текущей выборке','small','text/secondary');
const link=await button(c,'Посмотреть участников','Tertiary',228);link.visible=false;
for(const [n,k,value]of[[title,'Label','Участников'],...(state==='Ready'?[[val,'Value',val.characters]]:[]),[hint,'Hint','Уникальных в текущей выборке']])links.push({n,k,value});
links.push({n:link,k:'ShowLink',value:false,bool:true});variants.push(c);
}
const set=figma.combineAsVariants(variants,sec);created.push(set.id);set.name='SummaryMetric';set.x=32;set.y=130;set.layoutMode='HORIZONTAL';set.primaryAxisSizingMode='AUTO';set.counterAxisSizingMode='AUTO';spacing(set,'lg');set.fills=[];set.strokes=[];
const props={};for(const l of links){if(!props[l.k])props[l.k]=set.addComponentProperty(l.k,l.bool?'BOOLEAN':'TEXT',l.value);l.n.componentPropertyReferences={...(l.n.componentPropertyReferences||{}),[l.bool?'visible':'characters']:props[l.k]};}
set.description='Overview KPI. Ready / Loading / NoData; Label, Value, Hint and ShowLink. No trend or inferred success score. Used in screens/results-overview.';
return {id:set.id,variants:set.children.map(n=>({id:n.id,name:n.name})),sectionId:sec.id,effectStyleId:effect.id,shadowVariableId:shadowColor.id,primitiveId:black.id,primitiveCollectionId:primitives.id,fonts:Object.fromEntries(Object.entries(styles).map(([k,s])=>[k,s.fontName])),createdNodeIds:[...new Set(created.concat(sec.findAll().map(n=>n.id)))]};
'''

TABLE = r'''
await figma.setCurrentPageAsync(page);
const set=await figma.getNodeByIdAsync('136:715');await fonts(set);
if(set.children.some(n=>n.name==='State=OverviewUnselected'))return {existingSetId:set.id};
const rows=await figma.getNodeByIdAsync('135:1062');await fonts(rows);
for(const master of rows.children){const first=master.findOne(n=>n.name==='Scenario');first.layoutSizingHorizontal='FILL';const label=first.findOne(n=>n.type==='FRAME');if(label)label.layoutSizingHorizontal='FILL';mutated.push(first.id);}
const metrics=await figma.getNodeByIdAsync('132:574');const variants=[];
const entries=[['Найти товар и добавить в корзину','Поиск → Карточка товара → В корзину','20','16',14,18,2],['Изменить количество товара','Количество товара в мини-корзине','18','15',12,17,1],['Оформить заказ','Контакты, доставка и подтверждение заказа','16','12',10,15,1]];
for(const state of ['OverviewUnselected','OverviewSelected']){
const c=component('State='+state,set,1536);spacing(c,'md','base');c.primaryAxisSizingMode='AUTO';
await text(c,'Title','Сценарии исследования','heading');
const header=full(frame('TableHeader',c,'HORIZONTAL',1504,'base'));spacing(header,'base','base');fill(header,'background/subtle');
for(const [i,label]of ['СЦЕНАРИЙ','НАЧАЛИ','ЗАВЕРШИЛИ','ДОСТИГЛИ ЦЕЛИ','НЕПОЛНЫЕ','ДЕЙСТВИЕ'].entries()){const t=await text(header,'Header'+i,label,'small','text/secondary');if(i>0){t.layoutSizingHorizontal='FIXED';t.resize([0,96,136,200,104,232][i],t.height);t.textAlignHorizontal='CENTER';}}
const body=full(frame('ScenarioRows',c,'VERTICAL',1504));body.itemSpacing=0;
for(let k=0;k<3;k++){const e=entries[k];const selected=state==='OverviewSelected'&&k===2;
const master=rows.children.find(n=>n.variantProperties.Selected===(selected?'True':'False')&&n.variantProperties.State==='Default');const r=master.createInstance();created.push(r.id);body.appendChild(r);await fonts(r);r.name='Scenario '+(k+1);r.resize(1504,112);r.setBoundVariable('paddingTop',dimensions.md);r.setBoundVariable('paddingBottom',dimensions.md);full(r);
r.setProperties({[propKey(rows,'Title')]:e[0],[propKey(rows,'Description')]:e[1],[propKey(rows,'Started')]:e[2],[propKey(rows,'Completed')]:e[3],[propKey(rows,'Incomplete')]:String(e[6])});
const m=r.findOne(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric');m.setProperties({[propKey(metrics,'FractionValue')]:e[4]+' / '+e[5],[propKey(metrics,'PercentValue')]:Math.round(100*e[4]/e[5])+'%',[propKey(metrics,'BaseValue')]:'Оценены '+e[5]+' из '+e[2]});
r.setExplicitVariableModeForCollection('VariableCollectionId:139:593',['139:0','140:0','140:1'][k]);}
await text(c,'DenominatorNote','Демо-данные · Участники могут встречаться в нескольких сценариях. Неполные данные не означают неуспех.','small','text/secondary');
variants.push({id:c.id,name:c.name});}
let y=Math.max(...set.children.filter(n=>!variants.some(v=>v.id===n.id)).map(n=>n.y+n.height))+24;
for(const v of variants){const n=await figma.getNodeByIdAsync(v.id);n.layoutPositioning='AUTO';mutated.push(n.id);}
set.resizeWithoutConstraints(Math.max(set.width,1536),set.height);set.parent.resizeWithoutConstraints(1600,set.parent.height);const sec=set.parent.parent;sec.resizeWithoutConstraints(3000,Math.max(...sec.children.map(n=>n.y+n.height+48)));mutated.push(set.parent.id,sec.id);set.description='Scenario results, including responsive OverviewUnselected and OverviewSelected variants. Overview starts without a selected scenario; selection is independent from success.';
const allIds=created.slice();for(const v of variants){const c=await figma.getNodeByIdAsync(v.id);allIds.push(...c.findAll().map(n=>n.id));}
return {id:set.id,variants,createdNodeIds:[...new Set(allIds)],mutatedNodeIds:mutated};
'''

SHELL = r'''
const target=figma.root.children.find(p=>p.id==='191:847');await figma.setCurrentPageAsync(target);
const existing=target.findOne(n=>n.type==='FRAME'&&n.name==='Screen/ResultsOverview');if(existing)return {existingScreenId:existing.id};
let section=target.children.find(n=>n.type==='SECTION'&&n.name==='Screens');if(!section){section=figma.createSection();created.push(section.id);target.appendChild(section);section.name='Screens';section.x=10560;section.y=160;section.resizeWithoutConstraints(2080,1260);fill(section,'background/canvas');}
const screen=frame('Screen/ResultsOverview',section,'HORIZONTAL',1920);screen.x=80;screen.y=80;screen.resize(1920,1080);screen.primaryAxisSizingMode='FIXED';screen.counterAxisSizingMode='FIXED';screen.itemSpacing=0;screen.clipsContent=true;fill(screen,'background/canvas');
const navMaster=await figma.getNodeByIdAsync('153:1961');await fonts(navMaster);const nav=navMaster.createInstance();created.push(nav.id);screen.appendChild(nav);nav.name='Sidebar';nav.resize(320,1080);
const right=full(frame('Workspace',screen,'VERTICAL',1600));right.layoutSizingVertical='FILL';right.itemSpacing=0;
const header=full(frame('Header',right,'HORIZONTAL',1600));header.resize(1600,64);header.primaryAxisSizingMode='FIXED';header.counterAxisSizingMode='FIXED';header.counterAxisAlignItems='CENTER';header.setBoundVariable('paddingLeft',dimensions.xl);header.setBoundVariable('paddingRight',dimensions.xl);fill(header,'background/surface');
await button(header,'Все проекты','Tertiary',136);await text(header,'CrumbSeparator','/','body','text/secondary').then(t=>{t.layoutSizingHorizontal='FIXED';t.resize(12,24);});await button(header,'Интернет-магазин','Tertiary',200);await text(header,'CurrentStudy','/  Покупка в интернет-магазине','body','text/secondary');await button(header,'Коллега','Tertiary',120);
const main=full(frame('Main',right,'VERTICAL',1600,'xl'));main.layoutSizingVertical='FILL';main.clipsContent=true;main.overflowDirection='VERTICAL';spacing(main,'lg','xl');
const heading=full(frame('PageHeading',main,'HORIZONTAL',1536));heading.counterAxisAlignItems='CENTER';spacing(heading,'base');const title=full(frame('PageTitle',heading,'VERTICAL',1000));await text(title,'Title','Обзор результатов','heading');await text(title,'Subtitle','Сценарии исследования и результаты участников','body','text/secondary');
await button(heading,'Обновить результаты','Secondary',210);await button(heading,'Отчёт PDF','Primary',168,iconKeys.document);
const filters=full(frame('ContextBar',main,'HORIZONTAL',1536));filters.counterAxisAlignItems='CENTER';spacing(filters,'base');await button(filters,'Все устройства','Secondary',204,iconKeys.down,true);await text(filters,'Mode','Режим: задания','body','text/secondary');const freshness=await text(filters,'Freshness','Сбор идёт · обновлено 14:32','small','text/secondary');freshness.layoutSizingHorizontal='FIXED';freshness.resize(320,24);freshness.textAlignHorizontal='RIGHT';
return {screenId:screen.id,sectionId:section.id,mainId:main.id,headerId:header.id,createdNodeIds:[...new Set(created.concat(screen.findAll().map(n=>n.id)))]};
'''

CONTENT_COMMON = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const screen=figma.currentPage.findOne(n=>n.type==='FRAME'&&n.name==='Screen/ResultsOverview');if(!screen)throw Error('Screen missing');
const main=screen.findOne(n=>n.name==='Main');await fonts(screen);
const metricSet=await figma.getNodeByIdAsync('171:1801');const tableSet=await figma.getNodeByIdAsync('136:715');
async function summary(parent,state='Ready',free=false){const row=full(frame('Summary',parent,'HORIZONTAL',1536));spacing(row,'base');const vals=[['Сценариев',free?'Не применимо':'3','В исследовании'],['Участников','20','Уникальных в текущей выборке'],['С неполными данными','2 из 20','Часть записи отсутствует']];for(let k=0;k<3;k++){const m=metricSet.children.find(n=>n.variantProperties.State===state).createInstance();created.push(m.id);row.appendChild(m);await fonts(m);full(m);m.setProperties({[propKey(metricSet,'Label')]:vals[k][0],[propKey(metricSet,'Hint')]:vals[k][2],[propKey(metricSet,'ShowLink')]:state==='Ready'&&k===2});if(state==='Ready')m.setProperties({[propKey(metricSet,'Value')]:vals[k][1]});if(k===2&&state==='Ready')m.findOne(n=>n.name==='Hint').visible=false;}return row;}
async function table(parent,state){const master=tableSet.children.find(n=>n.variantProperties.State===state);const t=master.createInstance();created.push(t.id);parent.appendChild(t);await fonts(t);t.name='ScenarioTable';full(t);t.layoutSizingVertical='HUG';return t;}
function stateWrap(name){const w=full(frame(name,main,'VERTICAL',1536));spacing(w,'lg');return w;}
async function context(parent,selected=false,free=false){const c=full(frame('ScenarioAnalysis',parent,'VERTICAL',1536,'base'));fill(c,'background/surface');c.strokes=[paint('border/subtle')];for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])c.setBoundVariable(k,await figma.variables.getVariableByIdAsync('VariableID:202:3805'));spacing(c,'sm','base');
if(!selected&&!free){await text(c,'Title','Выберите сценарий в списке выше','medium');await text(c,'Hint','Откроются тепловая карта, воронка, участники и сигналы затруднений.','small','text/secondary');return c;}
await text(c,'ContextTitle',free?'Свободное изучение интерфейса':'Выбран сценарий: Оформить заказ','heading');
await text(c,'Criterion',free?'Без заданных целей: анализируйте клики, записи и сигналы затруднений.':'Цель: открыть оформление → заполнить данные → отправить заказ.','body','text/secondary');
const actions=full(frame('AnalysisActions',c,'HORIZONTAL',1504));spacing(actions,'md');for(const [label,key,width]of [['Тепловая карта','heatmap',192],...(free?[]:[['Воронка','filter',148]]),['Участники и записи','users',228],['Сигналы / находки','flag',208]])await button(actions,label,'Secondary',width,iconKeys[key]);if(!free)await button(actions,'Снять выбор','Tertiary',156);
if(!free){await text(c,'DropOff','Наибольшая потеря: 3 из 15 между шагами 1 и 2.','medium');await text(c,'Pages','Страницы с сигналами: Контактные данные — 4 из 15; Доставка — 3 из 15.','small','text/secondary');}return c;}
'''

CONTENT = CONTENT_COMMON + r'''
if(main.children.some(n=>n.name==='State/Ready'))return {existingScreenId:screen.id};
const ready=stateWrap('State/Ready');await summary(ready);await table(ready,'OverviewUnselected');await context(ready);
return {screenId:screen.id,readyId:ready.id,createdNodeIds:[...new Set(created.concat(ready.findAll().map(n=>n.id)))]};
'''

STATES = CONTENT_COMMON + r'''
if(main.children.some(n=>n.name==='State/Selected'))return {existingScreenId:screen.id};
const stateIds={};
const selected=stateWrap('State/Selected');stateIds.Selected=selected.id;await summary(selected);await table(selected,'OverviewSelected');await context(selected,true);selected.visible=false;
for(const state of ['Loading','Error']){const w=stateWrap('State/'+state);stateIds[state]=w.id;if(state==='Loading')await summary(w,'Loading');const t=await table(w,state);t.resize(1536,440);t.layoutSizingHorizontal='FILL';t.layoutSizingVertical='FIXED';const header=t.findOne(n=>n.name==='TableHeader');if(header)header.visible=false;for(const n of t.children)if('layoutSizingHorizontal'in n)n.layoutSizingHorizontal='FILL';w.visible=false;}
for(const state of ['Empty','FilteredEmpty']){const w=stateWrap('State/'+state);stateIds[state]=w.id;const sum=await summary(w,'NoData');sum.children[0].setProperties({[propKey(metricSet,'Label')]:'Сценариев'});const num=sum.children[0].findOne(n=>n.name==='Value');num.characters='3';
await text(w,'StateTitle',state==='Empty'?'Пока нет результатов':'По выбранному устройству нет данных','heading');
const t=await table(w,'OverviewUnselected');const rows=t.findOne(n=>n.name==='ScenarioRows');const metric=await figma.getNodeByIdAsync('132:574');const nodata=metric.children.find(n=>n.variantProperties.Data==='NoData');for(const r of rows.children){const set=await figma.getNodeByIdAsync('135:1062');r.setProperties({[propKey(set,'Started')]:'0',[propKey(set,'Completed')]:'—',[propKey(set,'Incomplete')]:'—'});const m=r.findOne(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric');m.swapComponent(nodata);}
await button(w,state==='Empty'?'Перейти к запуску':'Сбросить фильтры','Secondary',208);w.visible=false;}
const overflow=stateWrap('State/Overflow');stateIds.Overflow=overflow.id;await summary(overflow);const ot=await table(overflow,'OverviewUnselected');const row=ot.findOne(n=>n.name==='Scenario 1');const rowset=await figma.getNodeByIdAsync('135:1062');row.setProperties({[propKey(rowset,'Title')]:'Найти подходящий товар с доставкой в выбранный город и добавить его в корзину',[propKey(rowset,'Description')]:'Проверка длинного названия сценария и переноса текста'});await context(overflow);overflow.visible=false;
const free=stateWrap('State/FreeExploration');stateIds.FreeExploration=free.id;await summary(free,'Ready',true);await context(free,false,true);free.visible=false;
figma.skipInvisibleInstanceChildren=false;
for(const state of ['Empty','FilteredEmpty','Loading']){const w=await figma.getNodeByIdAsync(stateIds[state]);const cards=w.children.find(n=>n.name==='Summary').children;for(let i=0;i<3;i++){await fonts(cards[i]);cards[i].setProperties({[propKey(metricSet,'Hint')]:state==='Loading'?'Показатель появится после загрузки':i===0?'В исследовании':i===1?'В текущей выборке':'Оценка появится после сбора данных'});}if(state!=='Loading')cards[1].findOne(n=>n.name==='Value').characters='0';}
return {screenId:screen.id,stateIds,createdNodeIds:[...new Set(created.concat(Object.values(stateIds).flatMap(id=>figma.getNodeById(id).findAll().map(n=>n.id))))]};
'''

SWITCH = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
figma.skipInvisibleInstanceChildren=false;
const screen=await figma.getNodeByIdAsync('175:614');
const main=screen.findOne(n=>n.name==='Main');const stateName='__STATE__';
const states=main.children.filter(n=>n.name.startsWith('State/'));
if(!states.some(n=>n.name==='State/'+stateName))throw Error('Unknown state '+stateName);
for(const t of screen.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const mode=screen.findOne(n=>n.name==='Mode');mode.characters=stateName==='FreeExploration'?'Режим: свободное изучение':'Режим: задания';
for(const s of states)s.visible=s.name==='State/'+stateName;
const filter=screen.findOne(n=>n.name==='Все устройства');const control=filter.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');control.setProperties({'Text#30956:4':stateName==='FilteredEmpty'?'Мобильное':'Все устройства'});
return {screenId:screen.id,state:stateName,mutatedNodeIds:states.map(n=>n.id).concat([mode.id,control.id])};
'''

def main():
    stage = sys.argv[1]
    code = (BASE + {'metric': METRIC, 'table': TABLE, 'shell': SHELL, 'content': CONTENT, 'states': STATES}[stage]) if stage != 'show' else SWITCH.replace('__STATE__', sys.argv[2])
    TMP.mkdir(parents=True, exist_ok=True)
    (TMP / f'{stage}.js').write_text(code, encoding='utf-8')
    print(json.dumps({'code': code}, ensure_ascii=False))

if __name__ == '__main__':
    main()
