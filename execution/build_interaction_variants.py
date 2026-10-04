"""Build one product interaction extension per Figma call from existing instances."""
import json
import sys
from pathlib import Path
from grow_ui_kit import COMMON, BUILD_COMMON

ROOT=Path(__file__).resolve().parents[1]
THEME=BUILD_COMMON[BUILD_COMMON.index('async function theme'):BUILD_COMMON.index('const buttonSet=')]
TOKENS=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.name,v]));
const col=await figma.variables.getVariableCollectionByIdAsync('VariableCollectionId:67:106');
const ids=[];const tokens=[];
for(const [name,target]of Object.entries({'action/hover':'text/primary','action/pressed':'text/secondary','surface/hover':'background/sidebar','surface/pressed':'accent/soft','border/focus':'accent/strong'})){
 if(!vars[target])throw Error('Missing '+target);
 let v=vars[name];if(!v){v=figma.variables.createVariable(name,col,'COLOR');ids.push(v.id);}
 v.scopes=name==='border/focus'?['STROKE_COLOR']:['FRAME_FILL','SHAPE_FILL'];
 for(const mode of col.modes)v.setValueForMode(mode.modeId,{type:'VARIABLE_ALIAS',id:vars[target].id});
 v.setVariableCodeSyntax('WEB','var(--'+name.replaceAll('/','-')+')');tokens.push({id:v.id,name,target,values:v.valuesByMode});
}
return {createdVariableIds:ids,tokens};
'''
START=COMMON+THEME+r'''
await figma.setCurrentPageAsync(page);
const allVars=await figma.variables.getLocalVariablesAsync('COLOR');
const byId=Object.fromEntries(allVars.map(v=>[v.id,v]));
function resolved(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolved(byId[x.id]):x;}
function paint(key){const value=resolved(colors[key]);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:value.r,g:value.g,b:value.b}},'color',colors[key]);}
const NAME='__NAME__';
let existing=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name===NAME);
if(existing)return {existingSetId:existing.id,name:NAME};
let section=page.findOne(n=>n.type==='SECTION'&&n.name==='UI Kit — interaction states');
if(!section){section=figma.createSection();created.push(section.id);section.name='UI Kit — interaction states';page.appendChild(section);section.x=2480;section.y=80;section.resizeWithoutConstraints(900,1800);fill(section,'background/canvas');}
const wrapper=frame(NAME+'Documentation',section,'VERTICAL',820,'lg');wrapper.x=40;wrapper.y=__Y__;spacing(wrapper,'base','lg');
await text(wrapper,'Title',NAME,'medium');
await text(wrapper,'MatrixNote','__NOTE__','small','text/secondary');
const variants=[];const labels=[];
function cell(name,w,h){const c=figma.createComponent();created.push(c.id);c.name=name;c.layoutMode='HORIZONTAL';c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';c.resize(w,h);spacing(c,'xs','xs');radii(c);c.fills=[];c.strokes=[];c.counterAxisAlignItems='CENTER';wrapper.appendChild(c);variants.push(c);return c;}
function focus(c,state){if(state==='Focus'){c.strokes=[paint('border/focus')];c.strokeWeight=2;c.strokeAlign='OUTSIDE';}}
async function sourceInstance(source,c,w,h,color,bg){const n=source.createInstance();c.appendChild(n);await theme(n,color,bg);n.setBoundVariable('minWidth',null);n.minWidth=w;n.resizeWithoutConstraints(w,h);if(n.layoutMode!=='NONE'){n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';}n.name='Control';created.push(n.id);return n;}
'''
BUTTON=r'''
const src=await figma.importComponentSetByKeyAsync('6a543e9d0f1be76a826caf57c45ccfe45097c0e4');
const sp=await figma.importComponentSetByKeyAsync('664513406eaaaba39b3ea03f657cd7c49987e294');
const spinner=sp.children.find(n=>n.variantProperties.Size==='Small');
for(const state of ['Default','Hover','Pressed','Focus','Disabled','Loading'])for(const kind of ['Primary','Secondary','Tertiary']){
 const style={Primary:'Filled',Secondary:'Default*',Tertiary:'Empty'}[kind];
 const source=src.children.find(n=>{const v=n.variantProperties;return v.Style===style&&v.Color==='Neutral'&&v.Size==='Small'&&v.Disabled==='False'&&v.Loading==='False'&&v['Icon only']==='False';});
 if(!source)throw Error('Base Button missing '+style);
 const c=cell(`Kind=${kind}, State=${state}, Size=Small`,180,40);
 let bg=kind==='Primary'?'action/primary':kind==='Secondary'?'background/sidebar':'background/surface';
 if(state==='Hover')bg=kind==='Primary'?'action/hover':'surface/hover';
 if(state==='Pressed')bg=kind==='Primary'?'action/pressed':'surface/pressed';
 if(kind==='Secondary')bg=state==='Hover'?'action/secondary/hover':state==='Pressed'?'action/secondary/pressed':'action/secondary/background';
 const color=kind==='Primary'?'text/inverse':'text/primary';
 const n=await sourceInstance(source,c,172,32,color,bg);
 n.layoutSizingHorizontal='FILL';
 n.setProperties({'Text#30956:4':state==='Loading'?'Загрузка…':'Продолжить','Icon left#30956:3':state==='Loading','Icon right#30956:5':false});
 if(state==='Loading'){n.setProperties({'⮑  Icon left#30964:4':spinner.id});await theme(n,color,bg);for(const v of n.findAll(x=>x.type==='VECTOR'||x.type==='ELLIPSE'||x.type==='BOOLEAN_OPERATION')){if(v.fills.length)v.fills=[paint(color)];if(v.strokes.length)v.strokes=[paint(color)];}}
 fill(n,bg);n.strokes=[];if(kind==='Tertiary'&&!['Hover','Pressed'].includes(state))n.fills=[];
 if(state==='Disabled')n.opacity=.4;
 focus(c,state);labels.push({node:n.findOne(t=>t.type==='TEXT'&&t.characters===(state==='Loading'?'Загрузка…':'Продолжить')),loading:state==='Loading'});
}
'''
NAV=r'''
const src=await figma.importComponentSetByKeyAsync('7ed7b852338d4112272932beb8b3a742b9eedfd8');
for(const state of ['Default','Hover','Pressed','Focus'])for(const selected of ['False','True']){
 const source=src.children.find(n=>{const v=n.variantProperties;return v['Nested level']==='0'&&v['Has child items?']==='False'&&v['Icon?']==='False'&&v['Active?']===selected;});
 if(!source)throw Error('Base Nav missing');
 const c=cell(`Selected=${selected}, State=${state}`,260,48);
 const bg=selected==='True'||state==='Pressed'?'surface/pressed':state==='Hover'?'surface/hover':'background/surface';
 const color=selected==='True'?'accent/strong':'text/primary';
 const n=await sourceInstance(source,c,252,40,color,bg);fill(n,bg);radii(n);spacing(n,'sm','sm');
 n.minWidth=null;n.layoutSizingHorizontal='FILL';
 const t=n.findOne(t=>t.type==='TEXT');t.characters='Результаты';labels.push({node:t});
 if(selected==='True'){n.strokes=[paint('accent/strong')];n.strokeWeight=2;n.strokeLeftWeight=2;n.strokeRightWeight=0;n.strokeTopWeight=0;n.strokeBottomWeight=0;}
 focus(c,state);
}
'''
TAB=r'''
const src=await figma.importComponentSetByKeyAsync('f979852d8fd397a422c7eb5f93bab7c569662642');
for(const state of ['Default','Hover','Pressed','Focus'])for(const selected of ['False','True']){
 const source=src.children.find(n=>{const v=n.variantProperties;return v.Selected===selected&&v.Disabled==='False'&&v.Size==='Small';});
 if(!source)throw Error('Base Tab missing');
 const c=cell(`Selected=${selected}, State=${state}, Size=Small`,180,40);
 const bg=state==='Pressed'?'surface/pressed':state==='Hover'?'surface/hover':'background/surface';
 const color=selected==='True'?'accent/strong':'text/primary';
 const n=await sourceInstance(source,c,172,32,color,bg);
 n.setProperties({'Text#32618:0':'Сигналы','Append#32617:4':false,'Prepend#32617:6':false});fill(n,bg);
 for(const child of n.findAll(x=>x.type==='RECTANGLE'||x.type==='LINE')){if(child.fills.length)fill(child,selected==='True'?'accent/strong':'border/subtle');if(child.strokes.length)child.strokes=[paint(selected==='True'?'accent/strong':'border/subtle')];}
 n.strokes=selected==='True'?[paint('accent/strong')]:[];if(selected==='True'){n.strokeWeight=2;n.strokeBottomWeight=2;n.strokeLeftWeight=0;n.strokeRightWeight=0;n.strokeTopWeight=0;}
 labels.push({node:n.findOne(t=>t.type==='TEXT'&&t.characters==='Сигналы')});focus(c,state);
}
'''
END=r'''
const set=figma.combineAsVariants(variants,wrapper);created.push(set.id);set.name=NAME;set.layoutMode='HORIZONTAL';set.layoutWrap='WRAP';set.resize(__WIDTH__,100);set.primaryAxisSizingMode='FIXED';set.counterAxisSizingMode='AUTO';spacing(set,'base');set.setBoundVariable('counterAxisSpacing',dimensions.base);set.fills=[];set.strokes=[];set.clipsContent=false;for(const k of ['paddingTop','paddingBottom','paddingLeft','paddingRight'])set[k]=0;
set.description='Product extension of existing Elastic UI instances. Static interaction states; keyboard focus is independent of selected state. Variable-bound product palette. See ds/component-variants-audit.md for usage and scope.';
radii(set);
for(const c of set.children){const control=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');if(!control)throw Error('Missing nested control');control.isExposedInstance=true;}
await text(wrapper,'Usage','__USAGE__','small','text/secondary');
return {name:NAME,id:set.id,sectionId:section.id,documentationId:wrapper.id,createdNodeIds:[...new Set(created.concat(wrapper.findAll().map(n=>n.id)))],variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height})),properties:set.componentPropertyDefinitions};
'''

def build(stage):
    if stage=='tokens':return TOKENS
    config={'button':('ProductButton',40,572,'Колонки: Primary / Secondary / Tertiary. Строки: Default / Hover / Pressed / Focus / Disabled / Loading.','Продолжить','Вложенная кнопка Elastic UI. Loading — статичный индикатор; Disabled — действие недоступно. Размер контрола: 172×32, рамка фокуса снаружи.',BUTTON),'nav':('ProductNavItem',650,536,'Колонки: обычный / выбранный. Строки: Default / Hover / Pressed / Focus.','Результаты','Боковая навигация. Выбранный пункт отмечен фоном и левой полосой; Focus сохраняет выбор. Размер контрола: 252×40.',NAV),'tab':('ProductTab',1110,376,'Колонки: обычная / выбранная. Строки: Default / Hover / Pressed / Focus.','Сигналы','Вкладки сигналов и находок. Выбранная вкладка подчёркнута. Фокус — отдельная рамка. Размер контрола: 172×32.',TAB)}
    name,y,w,note,label,usage,body=config[stage]
    code=START+body+END
    for key,value in {'NAME':name,'Y':str(y),'WIDTH':str(w),'NOTE':note,'LABEL':label,'USAGE':usage}.items():code=code.replace('__'+key+'__',value)
    return code

if __name__=='__main__':
    stage=sys.argv[1];code=build(stage);out=ROOT/'.tmp/component-variants';out.mkdir(parents=True,exist_ok=True);(out/(stage+'.js')).write_text(code,encoding='utf-8');print(json.dumps({'code':code},ensure_ascii=False))
