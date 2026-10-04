"""Build a reusable task radio-card from existing themed Elastic Radio instances."""
import json
import sys
from grow_ui_kit import COMMON

START=COMMON+r'''
await figma.setCurrentPageAsync(page);
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.id,v]));
function resolve(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolve(vars[x.id]):x;}
function paint(key){const v=colors[key],x=resolve(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
const NAME='UI Kit — task selection';
let board=page.children.find(n=>n.name===NAME);
'''
BOARD=r'''
if(board)return {boardId:board.id,existing:true};
board=frame(NAME,page,'VERTICAL',1440,'lg');board.x=19000;board.y=80;spacing(board,'lg','lg');fill(board,'background/canvas');
await text(board,'Title','TaskChoiceCard · выбор одного задания','medium');
await text(board,'Usage','Selected=False / True × Default / Hover / Focus / Disabled. Колонки: обычная и выбранная. Строки: состояния.','small','text/secondary');
await text(board,'Behavior','В реализации: radiogroup, выбор по всей карточке; стрелки меняют вариант, Space выбирает. Tab показывает отдельный контур фокуса.','small','text/secondary');
return {createdNodeIds:created,boardId:board.id};
'''
VARIANT=r'''
const selected=SELECTED,state=STATE;const name='Selected='+selected+', State='+state;
if(board.findOne(n=>n.type==='COMPONENT'&&n.name===name))return {existing:true,name};
const c=figma.createComponent();created.push(c.id);board.appendChild(c);c.name=name;c.layoutMode='HORIZONTAL';c.resize(672,104);c.primaryAxisSizingMode='FIXED';c.counterAxisSizingMode='AUTO';spacing(c,'base','lg');c.counterAxisAlignItems='MIN';
for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])c.setBoundVariable(p,radius);
fill(c,selected==='True'?'accent/soft':state==='Hover'?'background/sidebar':'background/surface');
c.strokes=[paint(selected==='True'||state==='Focus'?'accent/strong':'border/control')];c.strokeWeight=state==='Focus'||(selected==='True'&&state==='Hover')?3:selected==='True'?2:1;c.strokeAlign=state==='Focus'?'OUTSIDE':'INSIDE';c.strokesIncludedInLayout=false;
const source=await figma.getNodeByIdAsync(selected==='True'?'135:958':'135:856');await fonts(source);const radio=source.clone();created.push(radio.id);c.appendChild(radio);radio.name='Radio';radio.layoutSizingHorizontal='FIXED';radio.layoutSizingVertical='FIXED';
const body=frame('Content',c,'VERTICAL',552);body.layoutSizingHorizontal='FILL';spacing(body,'sm');
const heading=frame('Heading',body,'HORIZONTAL',552);heading.layoutSizingHorizontal='FILL';spacing(heading,'sm');heading.counterAxisAlignItems='CENTER';
const title=await text(heading,'Title','Найти товар','medium',selected==='True'?'accent/strong':'text/primary');
const marker=await text(heading,'SelectedLabel','Выбрано','small','accent/strong');marker.layoutSizingHorizontal='HUG';marker.visible=selected==='True';
const desc=await text(body,'Description','Найдите подходящий товар и откройте его карточку.','body','text/primary');
c.opacity=state==='Disabled'?.4:1;
return {createdNodeIds:[...new Set(created.concat(c.findAll().map(n=>n.id)))],variantId:c.id,name};
'''
FINALIZE=r'''
let set=board.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='TaskChoiceCard');
if(!set){const variants=board.children.filter(n=>n.type==='COMPONENT');if(variants.length!==8)throw Error('Expected 8 variants');set=figma.combineAsVariants(variants,board);created.push(set.id);set.name='TaskChoiceCard';set.layoutMode='VERTICAL';set.layoutMode='NONE';
const title=set.addComponentProperty('Title','TEXT','Найти товар'),description=set.addComponentProperty('Description','TEXT','Найдите подходящий товар и откройте его карточку.');
for(const c of set.children){const t=c.findOne(n=>n.type==='TEXT'&&n.name==='Title'),d=c.findOne(n=>n.type==='TEXT'&&n.name==='Description');t.componentPropertyReferences={characters:title};d.componentPropertyReferences={characters:description};}
}
const states=['Default','Hover','Focus','Disabled'];
for(const c of set.children){c.x=c.variantProperties.Selected==='True'?696:0;c.y=states.indexOf(c.variantProperties.State)*144;}
set.resize(1368,560);set.description='Single-selection task card. Composed from themed Elastic Radio instances. Selected: olive surface, outline, radio and explicit label. Title/Description are text properties. Arrow keys and Space are implementation requirements; prototype interaction is not wired.';
return {createdNodeIds:created,mutatedNodeIds:[set.id,...set.findAll().map(n=>n.id)],setId:set.id,variants:set.children.map(n=>({id:n.id,name:n.name,width:n.width,height:n.height})),properties:set.componentPropertyDefinitions};
'''
if __name__=='__main__':
    stage=sys.argv[1]
    code=BOARD if stage=='board' else FINALIZE if stage=='finalize' else VARIANT.replace('SELECTED',json.dumps(sys.argv[2])).replace('STATE',json.dumps(sys.argv[3]))
    print(json.dumps({'code':START+code},ensure_ascii=False))
