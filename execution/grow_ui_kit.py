"""Generate small deterministic Figma payloads for the approved UI kit extension."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMON = r'''
const created=[];
const colors=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.name,v]));
const dimensions={};
for(const [name,key] of Object.entries({'xs':'33cf8d6af437f589eec375f0dba78baab2864cf9','sm':'c6350febff91d7248df73477a27c5387155ac6c2','md':'735270ec262d42d1788ddb9a560e026784d69e90','base':'723a30bab117da7a71b48251ea5a84eb3614f264','lg':'e34de5efd30aef81f5d652fe45dc113b59cc6e1a','xl':'0ace79592609fc26827cadc8feadb56b9e862061','radius':'dd2359cd4743157f5fc30993b8f29368cec946d3'})) dimensions[name]=await figma.variables.importVariableByKeyAsync(key);
const styles={};
for(const [name,key] of Object.entries({body:'055057128653b8e0591ad4af0f3f89ef9b2a5065',medium:'f9812c3b501de2fc60a2086c9d855d94e3bd1950',small:'0ffe9932b31ce3305d4041a590cc8ec20d95f4d2'})){
const s=await figma.importStyleByKeyAsync(key);await figma.loadFontAsync(s.fontName);styles[name]=s;
}
function paint(key){if(!colors[key])throw Error('Missing color '+key);const value=Object.values(colors[key].valuesByMode)[0];return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:value.r,g:value.g,b:value.b}},'color',colors[key]);}
function fill(n,key){n.fills=[paint(key)];}
function radii(n){for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(k,dimensions.radius);}
function spacing(n,gap='sm',pad=null){n.setBoundVariable('itemSpacing',dimensions[gap]);if(pad)for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n.setBoundVariable(k,dimensions[pad]);}
function frame(name,parent,dir='VERTICAL',width=600,pad=null){const n=figma.createAutoLayout(dir);created.push(n.id);n.name=name;n.fills=[];n.resize(width,100);n.primaryAxisSizingMode=dir==='VERTICAL'?'AUTO':'FIXED';n.counterAxisSizingMode=dir==='VERTICAL'?'FIXED':'AUTO';spacing(n,'sm',pad);if(parent)parent.appendChild(n);return n;}
async function text(parent,name,value,style='body',color='text/primary'){
const t=figma.createText();created.push(t.id);t.name=name;await t.setTextStyleIdAsync(styles[style].id);t.characters=value;fill(t,color);parent.appendChild(t);t.layoutSizingHorizontal='FILL';t.textAutoResize='HEIGHT';return t;
}
async function fonts(root){for(const t of root.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);}
function component(name,parent,width=600){const n=figma.createComponent();created.push(n.id);n.name=name;n.layoutMode='VERTICAL';n.resize(width,100);n.primaryAxisSizingMode='AUTO';n.counterAxisSizingMode='FIXED';spacing(n,'md','base');radii(n);fill(n,'background/surface');n.strokes=[paint('border/subtle')];n.strokesIncludedInLayout=false;parent.appendChild(n);return n;}
const page=figma.root.children.find(p=>p.name==='UX-Lab · UI Kit');
'''

FOUNDATION = r'''
if(page)return {existingPageId:page.id};
const p=figma.createPage();created.push(p.id);p.name='UX-Lab · UI Kit';await figma.setCurrentPageAsync(p);
const collection=figma.variables.createVariableCollection('UX-Lab · Heatmap');collection.renameMode(collection.modes[0].modeId,'Light');
const hexes=['#F2F4E9','#E3E8CC','#D3DDAE','#BECF8F','#A7BD70','#8FA653','#788E3C','#62782E','#4C6224','#384D19'];
for(let i=0;i<hexes.length;i++){const h=hexes[i];const v=figma.variables.createVariable('heatmap/intensity/'+(i+1),collection,'COLOR');v.scopes=['FRAME_FILL','SHAPE_FILL'];v.setValueForMode(collection.modes[0].modeId,{r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255});v.setVariableCodeSyntax('WEB','var(--heatmap-intensity-'+(i+1)+')');colors[v.name]=v;}
const foundation=figma.createSection();created.push(foundation.id);foundation.name='Foundation';p.appendChild(foundation);foundation.x=80;foundation.y=80;foundation.resizeWithoutConstraints(720,950);fill(foundation,'background/canvas');
const f=frame('FoundationContent',foundation,'VERTICAL',656,'lg');f.x=32;f.y=48;spacing(f,'lg','lg');
await text(f,'Title','Foundation · UX-Lab','medium');
await text(f,'Source','Elastic UI (Copy) · подключённая библиотека\nЦвета продукта — по выбранному референсу.','small','text/secondary');
await text(f,'Typography','Типографика — импортированные Text Styles','medium');
await text(f,'BodySpecimen','Основной текст · Кириллица: исследование, участник','body');
await text(f,'MediumSpecimen','Подпись действия · Воспроизвести','medium');
await text(f,'SmallSpecimen','Пояснение · Данные неполные','small','text/secondary');
await text(f,'Scale','Отступы: 4 · 8 · 12 · 16 · 24 · 32\nРадиус: 4. Источник — Dimensions Elastic UI.','small','text/secondary');
for(const [key,label] of [['background/canvas','Тёплый фон'],['background/surface','Белая поверхность'],['action/primary','Основное действие'],['accent/soft','Выбранное состояние']]){const row=frame('ColorRow',f,'HORIZONTAL',608,'sm');fill(row,key);radii(row);await text(row,'ColorLabel',label,'body',key==='action/primary'?'text/inverse':'text/primary');}
await text(f,'HeatmapTitle','Шкала интенсивности кликов','medium');
const swatches=frame('HeatmapScale',f,'HORIZONTAL',608);spacing(swatches,'xs');
for(let i=0;i<10;i++){const sw=frame('Intensity'+(i+1),swatches,'VERTICAL',56);sw.resize(56,24);sw.primaryAxisSizingMode='FIXED';fill(sw,'heatmap/intensity/'+(i+1));}
await text(f,'HeatmapNote','Меньше → больше кликов. Шкала для текущей выборки; числовые пороги не заданы.','small','text/secondary');
const ext=figma.createSection();created.push(ext.id);ext.name='UI Kit — extended';p.appendChild(ext);ext.x=880;ext.y=80;ext.resizeWithoutConstraints(1500,1300);fill(ext,'background/canvas');
const wrap=frame('ExtendedComponents',ext,'HORIZONTAL',1436);wrap.x=32;wrap.y=48;wrap.layoutWrap='WRAP';spacing(wrap,'xl');wrap.setBoundVariable('counterAxisSpacing',dimensions.xl);
return {createdNodeIds:created,pageId:p.id,foundationId:foundation.id,sectionId:ext.id,wrapperId:wrap.id,styles:Object.fromEntries(Object.entries(styles).map(([k,v])=>[k,{id:v.id,name:v.name}])),dimensions:Object.fromEntries(Object.entries(dimensions).map(([k,v])=>[k,{id:v.id,name:v.name}])),heatmapCollection:collection.id};
'''

BUILD_COMMON = r'''
if(!page)throw Error('Foundation page missing');await figma.setCurrentPageAsync(page);
const wrapper=page.findOne(n=>n.type==='FRAME'&&n.name==='ExtendedComponents');
const existing=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='__COMPONENT__');if(existing)return {existingSetId:existing.id};
wrapper.primaryAxisSizingMode='FIXED';wrapper.counterAxisSizingMode='AUTO';
const tile=frame('__COMPONENT__Tile',wrapper,'VERTICAL',684);spacing(tile,'md');
await text(tile,'ComponentName','__COMPONENT__','medium');
const variants=[];
function prop(owner,node,name,value){const p=owner.addComponentProperty(name,'TEXT',value);node.componentPropertyReferences={...node.componentPropertyReferences,characters:p};}
async function theme(root,color='text/primary',bg=null){await fonts(root);for(const n of [root,...root.findAll()]){
 if(n.type==='TEXT'){await n.setTextStyleIdAsync(styles.medium.id);fill(n,color);}
 else if('fills'in n&&Array.isArray(n.fills)&&n.fills.length){fill(n,n.type==='VECTOR'||n.type==='BOOLEAN_OPERATION'?color:(bg||'background/surface'));}
 if('strokes'in n&&n.strokes.length)n.strokes=[paint('border/control')];
 if('cornerRadius'in n&&typeof n.cornerRadius==='number'&&n.cornerRadius>0)radii(n);
 if('layoutMode'in n&&n.layoutMode!=='NONE'){
  for(const field of ['itemSpacing','paddingLeft','paddingRight','paddingTop','paddingBottom'])if(n[field]>0){const key=n[field]<=4?'xs':n[field]<=8?'sm':n[field]<=12?'md':n[field]<=16?'base':n[field]<=24?'lg':'xl';n.setBoundVariable(field,dimensions[key]);}
 }
}}
const buttonSet=await figma.importComponentSetByKeyAsync('6a543e9d0f1be76a826caf57c45ccfe45097c0e4');
async function button(parent,label,primary=false){
 const source=buttonSet.children.find(n=>{const v=n.variantProperties;return v.Style===(primary?'Filled':'Default*')&&v.Color==='Neutral'&&v.Size==='Small'&&v.Disabled==='False'&&v.Loading==='False'&&v['Icon only']==='False';});
 if(!source)throw Error('Button variant missing');const n=source.createInstance();parent.appendChild(n);n.name='Action';await fonts(n);n.setProperties({'Text#30956:4':label,'Icon left#30956:3':false,'Icon right#30956:5':false});await theme(n,primary?'text/inverse':'text/primary',primary?'action/primary':'background/surface');fill(n,primary?'action/primary':'background/surface');created.push(n.id);return n;
}
'''

HEATMAP = r'''
const paletteSet=await figma.importComponentSetByKeyAsync('5829898d82fbbefe4a7858252a4670bbe7bd61ad');const palette=paletteSet.children.find(n=>n.variantProperties.Palette==='Color blind');
for(const mode of ['AllClicks','FirstClick']){
 const c=component('Mode='+mode,tile,684);variants.push(c);
 const label=await text(c,'ModeLabel',mode==='AllClicks'?'Тепловая карта · Все клики':'Тепловая карта · Первый клик','medium');
const scale=palette.createInstance();c.appendChild(scale);scale.name='IntensityScale';scale.resize(652,16);await fonts(scale);radii(scale);
 const sw=scale.findAllWithCriteria({types:['RECTANGLE']});for(let i=0;i<sw.length;i++)fill(sw[i],'heatmap/intensity/'+(i+1));
 const ends=frame('ScaleLabels',c,'HORIZONTAL',652);const a=await text(ends,'Low','Меньше кликов','small','text/secondary');const b=await text(ends,'High','Больше кликов','small','text/secondary');b.textAlignHorizontal='RIGHT';
 const sample=await text(c,'SampleBase',mode==='AllClicks'?'84 клика · 18 участников':'18 первых кликов · 18 участников','body');prop(c,sample,'SampleBase',sample.characters);
 const note=await text(c,'DefinitionNote',mode==='AllClicks'?'Для текущей страницы, состояния и выборки.':'Единица отсчёта: требуется определить.','small','text/secondary');prop(c,note,'DefinitionNote',note.characters);
}
'''

REPLAY = r'''
const trackSet=await figma.importComponentSetByKeyAsync('37403251f1ab014a1703d3374882e2a20f701afe');const trackSource=trackSet.children.find(n=>n.variantProperties.Compressed==='False');
for(const coverage of ['Complete','Gap']){
const c=component('Coverage='+coverage,tile,684);variants.push(c);
await text(c,'TimelineLabel','Временная шкала записи','medium');
const trackArea=frame('TimeTrackArea',c,'VERTICAL',652);trackArea.resize(652,32);trackArea.primaryAxisSizingMode='FIXED';
const track=trackSource.createInstance();trackArea.appendChild(track);track.name='TimeTrack';track.resize(652,24);await fonts(track);radii(track);for(const n of track.findAllWithCriteria({types:['RECTANGLE']})){fill(n,'accent/soft');radii(n);}
for(const seconds of [48,138,192]){const marker=figma.createRectangle();created.push(marker.id);trackArea.appendChild(marker);marker.name='EventMarker'+seconds;marker.layoutPositioning='ABSOLUTE';marker.resize(4,16);marker.x=seconds/272*648;marker.y=4;marker.setBoundVariable('width',dimensions.xs);marker.setBoundVariable('height',dimensions.base);fill(marker,'accent/strong');}
if(coverage==='Gap'){const missing=figma.createRectangle();created.push(missing.id);trackArea.appendChild(missing);missing.name='MissingInterval100to125';missing.layoutPositioning='ABSOLUTE';missing.resize(25/272*652,16);missing.x=100/272*652;missing.y=4;missing.setBoundVariable('height',dimensions.base);fill(missing,'status/warning/background');missing.strokes=[paint('status/warning/text')];}
const labels=frame('TimeLabels',c,'HORIZONTAL',652);await text(labels,'Start','00:00','small','text/secondary');const end=await text(labels,'End','04:32','small','text/secondary');end.textAlignHorizontal='RIGHT';
const note=await text(c,'CoverageNote',coverage==='Gap'?'Нет данных: 01:40–02:05 · действия в интервале неизвестны':'Запись доступна на всём интервале','small',coverage==='Gap'?'status/warning/text':'text/secondary');
if(coverage==='Gap'){
const gaps=frame('GapRange',c,'HORIZONTAL',652,'sm');fill(gaps,'status/warning/background');radii(gaps);await text(gaps,'GapLabel','Разрыв записи: 01:40–02:05','small','status/warning/text');
}
const controls=frame('PlaybackActions',c,'HORIZONTAL',652);spacing(controls,'md');
await button(controls,'Воспроизвести',true);
const position=await text(controls,'PositionLabel','02:18 / 04:32','body');prop(c,position,'PositionLabel',position.characters);
await button(controls,'Скорость: 1×');await button(controls,'Вписать');
}
'''

COVERAGE = r'''
const calloutSet=await figma.importComponentSetByKeyAsync('b9aa043b75948779de186d30ca97d54f6a9dc024');
for(const coverage of ['Complete','Partial','Unavailable']){
const c=component('Coverage='+coverage,tile,684);variants.push(c);
const background=coverage==='Complete'?'status/success/background':coverage==='Partial'?'status/warning/background':'background/subtle';
const foreground=coverage==='Complete'?'status/success/text':coverage==='Partial'?'status/warning/text':'text/secondary';
fill(c,background);
const header=frame('StatusHeader',c,'HORIZONTAL',652);spacing(header,'sm');
const callout=calloutSet.children.find(n=>n.variantProperties.Color===(coverage==='Complete'?'Success':coverage==='Partial'?'Warning':'Primary')&&n.variantProperties.Size==='Small');
const iconInstance=callout.findOne(n=>n.type==='INSTANCE'&&n.name==='iInCircle');
const fallbackCallout=calloutSet.children[0];const fallbackIcon=fallbackCallout.findOne(n=>n.type==='INSTANCE'&&n.name==='iInCircle');
const iconMain=await (iconInstance||fallbackIcon).getMainComponentAsync();
const icon=iconMain.createInstance();header.appendChild(icon);icon.name='StatusIcon';icon.resize(16,16);await theme(icon,foreground,background);created.push(icon.id);
const title=await text(header,'StatusLabel',coverage==='Complete'?'Данные полные':coverage==='Partial'?'Данные неполные':'Запись недоступна','medium',foreground);
const detail=await text(c,'DetailText',coverage==='Complete'?'События и запись доступны для анализа.':coverage==='Partial'?'Часть записи отсутствует. Это не означает неуспех задания.':'Причина недоступности уточняется.','small','text/secondary');prop(c,detail,'DetailText'+coverage,detail.characters);
const actions=frame('OptionalAction',c,'HORIZONTAL',652);const btn=await button(actions,coverage==='Unavailable'?'К участнику':'Посмотреть данные');const show=c.addComponentProperty('ShowAction','BOOLEAN',true);actions.componentPropertyReferences={visible:show};
btn.name='ActionLabel';btn.isExposedInstance=true;
}
'''

BUILD_END = r'''
const savedTexts=variants.flatMap(v=>v.findAllWithCriteria({types:['TEXT']}).filter(t=>t.parent.type!=='INSTANCE').map(t=>({id:t.id,value:t.characters})));
const set=figma.combineAsVariants(variants,tile);set.name='__COMPONENT__';set.layoutMode='VERTICAL';set.primaryAxisSizingMode='AUTO';set.counterAxisSizingMode='AUTO';spacing(set,'md');radii(set);set.fills=[];set.strokes=[];set.description='UX-Lab extension. Approved product-specific composition using Elastic UI instances, imported text styles and bound product Variables. Minimal v1 variants; full interactive state matrix is not included.';created.push(set.id);
for(const item of savedTexts){const t=await figma.getNodeByIdAsync(item.id);await figma.loadFontAsync(t.fontName);t.characters=item.value;}
const section=wrapper.parent;section.resizeWithoutConstraints(1500,Math.max(1300,wrapper.height+96));
return {name:set.name,setId:set.id,variants:set.children.map(n=>({id:n.id,name:n.name})),createdNodeIds:[...new Set([...created,...tile.findAll().map(n=>n.id)])],mutatedNodeIds:[wrapper.id,section.id]};
'''

AUDIT = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const report=[];
for(const id of ['83:730','84:713','86:370']){
 const n=await figma.getNodeByIdAsync(id);const issues=[];
 for(const x of [n,...n.findAll()]){
  if(x.type==='TEXT'){
   if(!x.textStyleId)issues.push({id:x.id,issue:'no text style'});
   else {const s=await figma.getStyleByIdAsync(x.textStyleId);for(const p of ['fontFamily','fontSize','fontWeight','lineHeight'])if(!s.boundVariables[p])issues.push({id:x.id,issue:'style unbound '+p});}
  }
  for(const field of ['fills','strokes'])if(field in x&&Array.isArray(x[field]))for(const paint of x[field])if(paint.type==='SOLID'&&!paint.boundVariables?.color)issues.push({id:x.id,issue:'unbound '+field});
  if('layoutMode'in x&&x.layoutMode!=='NONE')for(const p of ['itemSpacing','paddingLeft','paddingTop','paddingRight','paddingBottom'])if(x[p]>0&&!x.boundVariables[p])issues.push({id:x.id,issue:'unbound '+p,value:x[p]});
  if('cornerRadius'in x&&typeof x.cornerRadius==='number'&&x.cornerRadius>0)for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])if(!x.boundVariables[p])issues.push({id:x.id,issue:'unbound '+p});
 }
 report.push({name:n.name,id:n.id,type:n.type,variants:n.children.map(c=>({id:c.id,name:c.name})),properties:n.componentPropertyDefinitions,issues,texts:n.findAllWithCriteria({types:['TEXT']}).map(t=>({id:t.id,name:t.name,text:t.characters,styleId:t.textStyleId}))});
}
return {date:'2026-09-22',fileKey:'1LeVoicxDT7Sl8TpMPs4hr',pageId:'82:3',sectionId:'82:45',foundationId:'82:15',report,heatmapVariables:(await figma.variables.getLocalVariablesAsync('COLOR')).filter(v=>v.name.startsWith('heatmap/')).map(v=>({id:v.id,name:v.name,values:v.valuesByMode,scopes:v.scopes})),passed:report.every(r=>r.issues.length===0)};
'''

def main():
    stage=sys.argv[1] if len(sys.argv)>1 else 'foundation'
    scripts={'foundation': COMMON+FOUNDATION,'audit':AUDIT}
    for name,code in [('HeatmapLegend',HEATMAP),('ReplayControls',REPLAY),('DataCoverage',COVERAGE)]:
        scripts[name]=(COMMON+BUILD_COMMON+code+BUILD_END).replace('__COMPONENT__',name)
    code=scripts[stage]
    out=ROOT/'.tmp/grow-ui-kit'
    out.mkdir(parents=True,exist_ok=True)
    (out/(stage+'.js')).write_text(code,encoding='utf-8')
    print(json.dumps({'code':code},ensure_ascii=False))

if __name__=='__main__':
    main()
