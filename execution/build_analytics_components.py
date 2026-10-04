"""Compose analytical UI components from approved foundations and library instances."""
import json
import sys
from pathlib import Path
from grow_ui_kit import COMMON, BUILD_COMMON
ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'.tmp/analytics-components'
THEME=BUILD_COMMON[BUILD_COMMON.index('async function theme'):BUILD_COMMON.index('const buttonSet=')]
START=COMMON+THEME+r'''
await figma.setCurrentPageAsync(page);
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.id,v]));
function resolved(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolved(vars[x.id]):x;}
function paint(key){const v=colors[key];if(!v)throw Error('Missing '+key);const x=resolved(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
styles.heading=await figma.importStyleByKeyAsync('a0fb5401c910ccd1871625995412cdd09c8f0c3b');await figma.loadFontAsync(styles.heading.fontName);
const NAME='__NAME__';const existing=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name===NAME);if(existing)return {existingSetId:existing.id,name:NAME};
let section=page.findOne(n=>n.type==='SECTION'&&n.name==='UI Kit — analytics blocks');
if(!section){section=figma.createSection();page.appendChild(section);section.name='UI Kit — analytics blocks';section.x=3500;section.y=80;section.resizeWithoutConstraints(2800,5000);fill(section,'background/canvas');created.push(section.id);}
const doc=frame(NAME+' · specification',section,'VERTICAL',__DOCWIDTH__,'lg');doc.x=__X__;doc.y=__Y__;spacing(doc,'base','lg');
await text(doc,'ComponentTitle',NAME,'heading');await text(doc,'MatrixNote','__NOTE__','small','text/secondary');
const variants=[];const propLinks=[];
function cell(name,w,h,dir='VERTICAL',pad=null){const c=figma.createComponent();created.push(c.id);c.name=name;c.layoutMode=dir;c.resize(w,h);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';spacing(c,'sm',pad);radii(c);fill(c,'background/surface');doc.appendChild(c);variants.push(c);return c;}
function fixed(n,w,h){n.resizeWithoutConstraints(w,h);if('layoutMode'in n&&n.layoutMode!=='NONE'){n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';}return n;}
function focus(c,state){if(state==='Focus'){c.strokes=[paint('border/focus')];c.strokeWeight=2;c.strokeAlign='INSIDE';}}
async function tx(parent,name,value,width,style='body',color='text/primary'){const t=await text(parent,name,value,style,color);t.layoutSizingHorizontal='FIXED';t.resize(width,t.height);t.textAutoResize='HEIGHT';return t;}
function link(node,name,value,kind='TEXT'){propLinks.push({node,name,value,kind});}
const iconKeys={target:'acede4ae5aebac65b1012130f12238ce0975ab60',image:'42e022270b024bb7c555a9da44ccad19c84e29b6',size:'28f003b8bdae6531af0a23cd0813d04d3a59590c',other:'086003b1e86d893d5a9f1ecc5b046f82f4220cf1',error:'b299c92ed07007bec43ed862fdb8eec5c228617b',search:'5bfb4b57a80e37badc23da1c6d13febb165d37a6',info:'249f36e0388fb7334418d80d6a6f56a12b734c1b'};
const icons={};async function icon(parent,key,color='text/secondary',size=20){if(!icons[key])icons[key]=await figma.importComponentByKeyAsync(iconKeys[key]);const i=icons[key].createInstance();parent.appendChild(i);await theme(i,color);i.resize(size,size);i.name='Icon';created.push(i.id);return i;}
async function button(parent,label,kind='Secondary'){const s=await figma.getNodeByIdAsync('125:450');const base=s.children.find(c=>c.variantProperties.Kind===kind&&c.variantProperties.State==='Default');const n=base.createInstance();parent.appendChild(n);await fonts(n);n.findOne(x=>x.type==='INSTANCE'&&x.name==='Control').setProperties({'Text#30956:4':label});created.push(n.id);return n;}
function propKey(set,prefix){const k=Object.keys(set.componentPropertyDefinitions).find(k=>k.startsWith(prefix+'#'));if(!k)throw Error('Missing property '+prefix);return k;}
function skeleton(parent,w,h){const n=frame('Skeleton',parent,'HORIZONTAL',w);fixed(n,w,h);fill(n,'border/subtle');radii(n);return n;}
async function stateMessage(c,status,width,subject){const box=frame('StateMessage',c,'VERTICAL',width);spacing(box,'base');await icon(box,status==='Error'?'error':status==='FilteredEmpty'?'search':'info',status==='Error'?'status/error/text':'text/secondary',24);
const title={Loading:'Загружаем данные',Empty:'Пока нет данных',FilteredEmpty:'Ничего не найдено',Error:'Не удалось загрузить данные'}[status];
await tx(box,'StateTitle',title,width,'medium');await tx(box,'StateDescription',{Loading:'Показатели появятся после загрузки.',Empty:subject==='targets'?'Первые клики появятся после прохождения теста участниками.':'Результаты сценариев появятся после начала тестирования.',FilteredEmpty:'Измените фильтры или сбросьте их, чтобы увидеть результаты.',Error:'Попробуйте ещё раз. Настройки исследования сохранены.'}[status],width,'body','text/secondary');
if(status==='Loading'){skeleton(box,width,16);skeleton(box,width*.72,16);skeleton(box,width*.86,16);}else if(status==='Error')await button(box,'Повторить');else if(status==='FilteredEmpty')await button(box,'Сбросить фильтры');}
'''
METRIC=r'''
const ps=await figma.importComponentSetByKeyAsync('1e71a04d04075b1538692698958e06344b92bce5');
const source=ps.children.find(c=>c.variantProperties.Size==='Medium* - 8px'&&c.variantProperties.Color==='Primary'&&c.variantProperties.Label==='False');
for(const state of ['Value','Zero','NoData']){const c=cell('Data='+state,200,88);spacing(c,'xs');
const top=frame('MetricHeading',c,'HORIZONTAL',200);spacing(top,'sm');
const fraction=await tx(top,'Fraction',state==='Value'?'14 / 18':state==='Zero'?'0 / 18':'—',132,'medium');
const pct=await tx(top,'Percent',state==='Value'?'78%':state==='Zero'?'0%':'—',60,'medium','accent/strong');pct.textAlignHorizontal='RIGHT';
link(fraction,'Fraction'+state,fraction.characters);link(pct,'Percent'+state,pct.characters);
const bar=source.createInstance();c.appendChild(bar);await theme(bar,'accent/strong','border/subtle');bar.name='SuccessBar';fixed(bar,200,8);bar.isExposedInstance=true;
const track=bar.findOne(n=>n.name==='Progress Bar');fixed(track,200,8);fill(track,'border/subtle');
bar.setBoundVariable('minHeight',null);bar.minHeight=8;bar.setBoundVariable('maxHeight',null);bar.maxHeight=8;fixed(bar,200,8);c.fills=[];
const inner=bar.findOne(n=>n.name==='Inner');inner.visible=false;
const trackWrap=frame('SuccessTrack',c,'HORIZONTAL',200);c.insertChild(c.children.indexOf(bar),trackWrap);fixed(trackWrap,200,8);trackWrap.itemSpacing=0;trackWrap.appendChild(bar);const ratio=figma.createRectangle();trackWrap.appendChild(ratio);ratio.name='RatioFill';ratio.layoutPositioning='ABSOLUTE';ratio.resize(200*14/18,8);ratio.x=0;ratio.y=0;fill(ratio,'accent/strong');radii(ratio);created.push(ratio.id);
for(const t of bar.findAllWithCriteria({types:['TEXT']}))t.visible=false;
if(state!=='Value')ratio.visible=false;if(state==='NoData')trackWrap.visible=false;
const base=await tx(c,'AssessmentBase',state==='NoData'?'Нет оценённых попыток':'Оценены 18 из 20',200,'small','text/secondary');link(base,'Base'+state,base.characters);
}
'''
TARGET_ROW=r'''
for(const selected of ['False','True'])for(const state of ['Default','Hover','Focus']){
const c=cell(`Selected=${selected}, State=${state}`,512,88,'HORIZONTAL','base');spacing(c,'md','base');c.counterAxisAlignItems='CENTER';fill(c,selected==='True'?'accent/soft':state==='Hover'?'surface/hover':'background/surface');focus(c,state);
const i=await icon(c,'target',selected==='True'?'accent/strong':'text/secondary',20);link(i,'TargetIcon',icons.target.id,'INSTANCE_SWAP');
const labels=frame('TargetLabels',c,'VERTICAL',332);spacing(labels,'xs');
const title=await tx(labels,'TargetTitle','Добавить в корзину',332,'medium');link(title,'Title','Добавить в корзину');
const subtitle=await tx(labels,'TargetDescription','Основное действие страницы',332,'small','text/secondary');link(subtitle,'Description','Основное действие страницы');
const metrics=frame('TargetMetrics',c,'HORIZONTAL',104);spacing(metrics,'sm');metrics.counterAxisAlignItems='CENTER';
const n=await tx(metrics,'Count','6',36,'medium');n.textAlignHorizontal='RIGHT';link(n,'Count','6');const pct=await tx(metrics,'Share','33%',60,'body','text/secondary');pct.textAlignHorizontal='RIGHT';link(pct,'Share','33%');
}
'''
TARGETS=r'''
const rows=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='FirstClickTargetRow');if(!rows)throw Error('Target row required');
for(const state of ['Ready','Loading','Empty','FilteredEmpty','Error']){
const c=cell('State='+state,560,640,'VERTICAL','lg');spacing(c,'base','lg');c.strokes=[paint('border/subtle')];
await tx(c,'Title','Цели первого клика',512,'heading');await tx(c,'Sample',state==='Ready'?'18 участников · 18 первых кликов':'Выбранный сценарий',512,'body','text/secondary');
if(state==='Ready'){
const entries=[['Добавить в корзину','Основное действие страницы','6','33%','target'],['Изображение товара','Галерея фотографий','5','28%','image'],['Выбор размера','Переключатель S / M / L','4','22%','size'],['Другие области','Крошки, заголовок, пустые области','3','17%','other']];
const list=frame('Targets',c,'VERTICAL',512);spacing(list,'xs');
for(let k=0;k<entries.length;k++){const [title,desc,count,share,ic]=entries[k];const base=rows.children.find(n=>n.variantProperties.Selected===(k===0?'True':'False')&&n.variantProperties.State==='Default');const row=base.createInstance();list.appendChild(row);await fonts(row);if(!icons[ic])icons[ic]=await figma.importComponentByKeyAsync(iconKeys[ic]);row.setProperties({[propKey(rows,'Title')]:title,[propKey(rows,'Description')]:desc,[propKey(rows,'Count')]:count,[propKey(rows,'Share')]:share,[propKey(rows,'TargetIcon')]:icons[ic].id});await theme(row.children.find(n=>n.type==='INSTANCE'),k===0?'accent/strong':'text/secondary');row.name='Target '+(k+1);created.push(row.id);}
const action=await button(c,'Выделить все зоны','Tertiary');const info=await tx(c,'SelectionNote','Выбрана область для просмотра на карте.',512,'small','text/secondary');
}else await stateMessage(c,state,512,'targets');
}
'''
SCENARIO_ROW=r'''
const radios=await figma.importComponentSetByKeyAsync('ebcbecc6d9b52e46bcb32c4582d219d4044dd8f7');const ms=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SuccessMetric');if(!ms)throw Error('Metric required');
for(const selected of ['False','True'])for(const state of ['Default','Hover','Focus']){
const c=cell(`Selected=${selected}, State=${state}`,1360,136,'HORIZONTAL','base');spacing(c,'base','base');c.counterAxisAlignItems='CENTER';fill(c,selected==='True'?'accent/soft':state==='Hover'?'surface/hover':'background/surface');focus(c,state);
const info=frame('Scenario',c,'HORIZONTAL',480);spacing(info,'md');info.counterAxisAlignItems='CENTER';
const radio=radios.children.find(n=>n.variantProperties.Label==='False'&&n.variantProperties.Checked===selected&&n.variantProperties.State==='Default').createInstance();info.appendChild(radio);await theme(radio,'accent/strong','background/surface');fixed(radio,16,16);radio.name='ScenarioSelection';
const copy=frame('ScenarioCopy',info,'VERTICAL',452);spacing(copy,'xs');const t=await tx(copy,'ScenarioTitle','Найти товар и добавить в корзину',452,'medium');link(t,'Title',t.characters);const d=await tx(copy,'ScenarioDescription','Поиск → Карточка товара → Клик «В корзину»',452,'small','text/secondary');link(d,'Description',d.characters);
const started=await tx(c,'Started','20',96,'medium');started.textAlignHorizontal='CENTER';link(started,'Started','20');const completed=await tx(c,'Completed','16',136,'medium');completed.textAlignHorizontal='CENTER';link(completed,'Completed','16');
const metric=ms.children.find(n=>n.variantProperties.Data==='Value').createInstance();c.appendChild(metric);metric.name='SuccessMetric';metric.isExposedInstance=true;
const partial=frame('Partial',c,'VERTICAL',104);partial.counterAxisAlignItems='CENTER';const badge=frame('IncompleteBadge',partial,'VERTICAL',40,'xs');badge.fills=selected==='True'?[]:[paint('background/sidebar')];radii(badge);const v=await tx(badge,'Incomplete','2',32,'small','text/primary');v.textAlignHorizontal='CENTER';link(v,'Incomplete','2');
const action=frame('RowAction',c,'VERTICAL',232);action.counterAxisAlignItems='CENTER';await button(action,selected==='True'?'Выбран':'Выбрать сценарий',selected==='True'?'Tertiary':'Secondary');
}
'''
TABLE=r'''
const rows=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ScenarioRow');const metrics=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SuccessMetric');if(!rows||!metrics)throw Error('Rows and metrics required');
for(const state of ['Ready','Loading','Empty','FilteredEmpty','Error']){
const c=cell('State='+state,1408,920,'VERTICAL','lg');spacing(c,'base','lg');c.strokes=[paint('border/subtle')];
await tx(c,'Title','Результаты по сценариям',1360,'heading');await tx(c,'Subtitle','Выберите сценарий, чтобы подробнее изучить результаты.',1360,'body','text/secondary');
const header=frame('TableHeader',c,'HORIZONTAL',1360,'base');spacing(header,'base','base');fill(header,'background/subtle');
const widths=[480,96,136,200,104,232],heads=['СЦЕНАРИЙ','НАЧАЛИ','ЗАВЕРШИЛИ','ДОСТИГЛИ ЦЕЛИ','НЕПОЛНЫЕ','ДЕЙСТВИЕ'];
for(let i=0;i<heads.length;i++){const t=await tx(header,'Header'+i,heads[i],widths[i],'small','text/secondary');if(i>0)t.textAlignHorizontal='CENTER';}
if(state==='Ready'){
const body=frame('ScenarioRows',c,'VERTICAL',1360);body.itemSpacing=0;
const entries=[['Найти товар и добавить в корзину','Поиск → Карточка товара → Клик «В корзину»','20','16',14,18,2],['Изменить количество товара','Изменение количества в мини-корзине','18','15',12,17,1],['Оформить заказ','Контакты, доставка и подтверждение заказа','16','12',10,15,1]];
for(let k=0;k<entries.length;k++){const [title,desc,started,completed,success,assessed,partial]=entries[k];const row=rows.children.find(n=>n.variantProperties.Selected===(k===0?'True':'False')&&n.variantProperties.State==='Default').createInstance();body.appendChild(row);await fonts(row);row.setProperties({[propKey(rows,'Title')]:title,[propKey(rows,'Description')]:desc,[propKey(rows,'Started')]:started,[propKey(rows,'Completed')]:completed,[propKey(rows,'Incomplete')]:String(partial)});
const m=row.findOne(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric');m.setProperties({[propKey(metrics,'FractionValue')]:success+' / '+assessed,[propKey(metrics,'PercentValue')]:Math.round(success/assessed*100)+'%',[propKey(metrics,'BaseValue')]:'Оценены '+assessed+' из '+started});const inner=m.findOne(n=>n.name==='RatioFill');inner.resizeWithoutConstraints(200*success/assessed,8);row.name='Scenario '+(k+1);created.push(row.id);}
await tx(c,'DenominatorNote','Демонстрационные данные. Счётчики — попытки; доля успеха рассчитана по оценённым попыткам. Неполные данные не равны неуспеху.',1360,'small','text/secondary');
const context=frame('SelectedScenarioContext',c,'VERTICAL',1360,'base');spacing(context,'sm','base');fill(context,'background/subtle');radii(context);await tx(context,'ContextTitle','Выбран сценарий: найти товар и добавить в корзину',1328,'medium');const actions=frame('AnalysisActions',context,'HORIZONTAL',1328);spacing(actions,'md');for(const label of ['Тепловая карта','Воронка','Участники и записи','Сигналы'])await button(actions,label,'Secondary');
}else await stateMessage(c,state,1360,'table');
}
'''
END=r'''
const set=figma.combineAsVariants(variants,doc);created.push(set.id);set.name=NAME;set.layoutMode='__DIR__';set.resize(__SETWIDTH__,100);set.primaryAxisSizingMode='__PRIMARY__';set.counterAxisSizingMode='__COUNTER__';if(set.layoutMode==='HORIZONTAL')set.layoutWrap='WRAP';spacing(set,'lg');set.setBoundVariable('counterAxisSpacing',dimensions.lg);set.fills=[];set.strokes=[];radii(set);set.clipsContent=false;for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])set[p]=0;
const props={};for(const l of propLinks){if(!props[l.name])props[l.name]=set.addComponentProperty(l.name,l.kind,l.value);l.node.componentPropertyReferences={...(l.node.componentPropertyReferences||{}),[l.kind==='INSTANCE_SWAP'?'mainComponent':'characters']:props[l.name]};}
set.description='Reusable analytics block for the UX testing dashboard. Uses bound product colours, imported Elastic UI text styles and nested instances. Demonstration counts, not live data. Selection and data completeness are independent from task success. See ds/analytics-components.md.';
section.resizeWithoutConstraints(section.width,Math.max(5000,...section.children.map(n=>n.y+n.height+48)));
return {name:NAME,id:set.id,sectionId:section.id,documentationId:doc.id,properties:set.componentPropertyDefinitions,variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height})),createdNodeIds:[...new Set(created.concat(doc.findAll().map(n=>n.id)))]};
'''
CONFIG={
 'metric':('SuccessMetric',40,40,740,648,'HORIZONTAL','FIXED','AUTO','Value / Zero / NoData. Доля успеха и база расчёта — разные значения.',METRIC),
 'target_row':('FirstClickTargetRow',40,350,600,512,'VERTICAL','AUTO','FIXED','Selected False / True × Default / Hover / Focus. Выбор области не означает успех задания.',TARGET_ROW),
 'scenario_row':('ScenarioRow',700,40,1440,1360,'VERTICAL','AUTO','FIXED','Selected False / True × Default / Hover / Focus. Счётчики не смешивают завершение, успех и полноту.',SCENARIO_ROW),
 'targets':('FirstClickTargets',40,1200,1200,1144,'HORIZONTAL','FIXED','AUTO','Ready / Loading / Empty / FilteredEmpty / Error. Иконки — библиотечные instances.',TARGETS),
 'table':('ScenarioTable',1300,1200,1480,1408,'VERTICAL','AUTO','FIXED','Ready / Loading / Empty / FilteredEmpty / Error. Прогресс = успешные / оценённые попытки.',TABLE)
}
def build(stage):
 name,x,y,dw,sw,di,primary,counter,note,body=CONFIG[stage];code=START+body+END
 for k,v in {'NAME':name,'X':x,'Y':y,'DOCWIDTH':dw,'SETWIDTH':sw,'DIR':di,'PRIMARY':primary,'COUNTER':counter,'NOTE':note}.items():code=code.replace('__'+k+'__',str(v))
 return code
if __name__=='__main__':
 TMP.mkdir(parents=True,exist_ok=True);code=build(sys.argv[1]);(TMP/(sys.argv[1]+'.js')).write_text(code,encoding='utf-8');print(json.dumps({'code':code},ensure_ascii=False))
