"""Product Checkbox wrapper around the connected Elastic checkbox, with 12 states."""
import json
import sys
from grow_ui_kit import COMMON

START=COMMON+r'''
await figma.setCurrentPageAsync(page);
figma.skipInvisibleInstanceChildren=false;
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.id,v]));
function resolve(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolve(vars[x.id]):x;}
function paint(k){const v=colors[k],x=resolve(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
const name='UI Kit — checkbox';let board=page.children.find(n=>n.name===name);
'''

BOARD=r'''
if(board)return {boardId:board.id,existing:true};
board=frame(name,page,'VERTICAL',1480,'lg');board.x=20600;board.y=80;fill(board,'background/canvas');spacing(board,'lg','lg');
await text(board,'Title','Checkbox · множественный выбор','medium');
await text(board,'Usage','Колонки: выключен / включён / частично. Строки: Default / Hover / Focus / Disabled.','small','text/secondary');
await text(board,'Behavior','Клик по квадрату или подписи меняет выбор; Space переключает, Tab показывает фокус. Статичные признаки не оформлять как чекбоксы.','small','text/secondary');
return {createdNodeIds:created,boardId:board.id};
'''

VARIANTS=r'''
if(!board)throw Error('Create board first');
const state=__STATE__;const result=[];
for(const [value,id] of [['Off','203:4623'],['On','203:4619'],['Mixed','203:4621']]){
 const name='Value='+value+', State='+state;if(board.findOne(n=>n.type==='COMPONENT'&&n.name===name))continue;
 const source=await figma.getNodeByIdAsync(id);await fonts(source);
 const c=component(name,board,448);c.fills=[];c.strokes=[];c.layoutMode='HORIZONTAL';c.resize(448,32);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='FIXED';c.counterAxisAlignItems='CENTER';
 for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom']){c.setBoundVariable(p,null);c[p]=0;}
 const checkbox=source.createInstance();c.appendChild(checkbox);checkbox.name='Control';await fonts(checkbox);checkbox.resize(448,24);checkbox.layoutSizingHorizontal='FILL';
 const checked=value!=='Off';
 for(const n of [checkbox,...checkbox.findAll()]){
  if(n.type==='TEXT'){fill(n,'text/primary');await n.setTextStyleIdAsync(styles.body.id);n.characters='Включить раздел в отчёт';n.name='Label';n.textAutoResize='HEIGHT';}
  else if('fills'in n){n.fills=[];if('strokes'in n)n.strokes=[];}
 }
 const box=checkbox.findOne(n=>n.type==='RECTANGLE'&&n.width===16&&n.height===16);fill(box,checked?'accent/strong':state==='Hover'?'accent/soft':'background/surface');box.strokes=[paint(checked||state==='Focus'?'accent/strong':'border/control')];box.strokeWeight=1.5;box.strokeAlign='INSIDE';radii(box);
 const glyphs=checkbox.findAll(n=>n.type==='VECTOR');for(const glyph of glyphs)fill(glyph,'text/inverse');
 if(value==='Mixed'){const oldMark=checkbox.findOne(n=>n.type==='RECTANGLE'&&n.name==='Rectangle');oldMark.visible=false;const dash=figma.createRectangle();c.appendChild(dash);created.push(dash.id);dash.name='Mixed mark';dash.layoutPositioning='ABSOLUTE';dash.resize(8,2);dash.x=4;dash.y=15;fill(dash,'text/inverse');}
 if(state==='Focus'){const ring=checkbox.findOne(n=>n.name==='Checkbox');ring.strokes=[paint('accent/strong')];ring.strokeWeight=2;ring.strokeAlign='OUTSIDE';radii(ring);}
 if(state==='Hover')box.strokeWeight=2;
 c.opacity=state==='Disabled'?.4:1;
 result.push({id:c.id,name});
}
return {createdNodeIds:[...new Set(created.concat(result.flatMap(r=>board.findOne(n=>n.id===r.id).findAll().map(n=>n.id))))],variants:result};
'''

FINALIZE=r'''
let set=board.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ProductCheckbox');
if(!set){const variants=board.children.filter(n=>n.type==='COMPONENT');if(variants.length!==12)throw Error('Expected 12 variants');
for(const c of variants){await fonts(c);const control=c.children.find(n=>n.name==='Control');const nested=control.findOne(n=>n.type==='TEXT');const label=nested.clone();c.appendChild(label);created.push(label.id);label.name='Label';label.layoutSizingHorizontal='FILL';label.textAutoResize='HEIGHT';nested.visible=false;control.resize(16,24);control.layoutSizingHorizontal='FIXED';c.setBoundVariable('itemSpacing',dimensions.sm);}
set=figma.combineAsVariants(variants,board);created.push(set.id);set.name='ProductCheckbox';const key=set.addComponentProperty('Label','TEXT','Включить раздел в отчёт');for(const v of set.children){const label=v.children.find(n=>n.type==='TEXT'&&n.name==='Label');label.componentPropertyReferences={characters:key};}}
set.layoutMode='NONE';const states=['Default','Hover','Focus','Disabled'];
for(const v of set.children){v.x=['Off','On','Mixed'].indexOf(v.variantProperties.Value)*472;v.y=states.indexOf(v.variantProperties.State)*64;}
set.resize(1392,240);set.description='Product checkbox: Off, On, Mixed × Default, Hover, Focus, Disabled. Retains the connected Elastic checkbox structure; palette, text style and radius use product tokens. Clickable label and Space toggle are implementation requirements; static selection states in Figma.';
return {createdNodeIds:created,mutatedNodeIds:[set.id,...set.findAll().map(n=>n.id)],setId:set.id,boardId:board.id,variants:set.children.map(n=>({id:n.id,name:n.name,width:n.width,height:n.height})),properties:set.componentPropertyDefinitions};
'''

if __name__=='__main__':
    stage=sys.argv[1]
    payload=BOARD if stage=='board' else FINALIZE if stage=='finalize' else VARIANTS.replace('__STATE__',json.dumps(stage))
    print(json.dumps({'code':START+payload},ensure_ascii=False))
