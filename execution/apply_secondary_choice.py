"""Apply approved Secondary A without outline; emit bounded Figma operations."""
import json
import sys

COMMON = r'''
const vars=await figma.variables.getLocalVariablesAsync('COLOR');
const byName=Object.fromEntries(vars.map(v=>[v.name,v]));
const byId=Object.fromEntries(vars.map(v=>[v.id,v]));
function resolved(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolved(byId[x.id]):x;}
function paint(name){const v=byName[name];if(!v)throw Error('Missing token '+name);const x=resolved(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const ids=[];
'''

TOKENS = r'''
const cols=await figma.variables.getLocalVariableCollectionsAsync();
const p=cols.find(c=>c.id==='VariableCollectionId:171:1756'),s=cols.find(c=>c.id==='VariableCollectionId:67:106');
const out=[];
for(const [name,hex] of [['background','#E4E5DC'],['hover','#D8DACD'],['pressed','#CCD0BE']]){
 const pname='neutral/secondary/'+name,sname='action/secondary/'+name;
 let pv=vars.find(v=>v.name===pname&&v.variableCollectionId===p.id)||figma.variables.createVariable(pname,p,'COLOR');
 pv.scopes=[];pv.setVariableCodeSyntax('WEB','var(--neutral-secondary-'+name+')');
 const n=parseInt(hex.slice(1),16);pv.setValueForMode(p.defaultModeId,{r:(n>>16)/255,g:((n>>8)&255)/255,b:(n&255)/255,a:1});
 let sv=vars.find(v=>v.name===sname&&v.variableCollectionId===s.id)||figma.variables.createVariable(sname,s,'COLOR');
 sv.scopes=['FRAME_FILL','SHAPE_FILL'];sv.setVariableCodeSyntax('WEB','var(--action-secondary-'+name+')');
 sv.setValueForMode(s.defaultModeId,{type:'VARIABLE_ALIAS',id:pv.id});
 out.push({name:sname,id:sv.id,primitiveId:pv.id,hex,scopes:sv.scopes,codeSyntax:sv.codeSyntax});
}
return {variableIds:out.flatMap(v=>[v.id,v.primitiveId]),tokens:out};
'''

MASTERS = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=await figma.getNodeByIdAsync('125:450');
for(const n of set.children){if(n.variantProperties.Kind!=='Secondary')continue;await fonts(n);
const state=n.variantProperties.State,c=n.children.find(c=>c.name==='Control');
c.fills=[paint('action/secondary/'+(state==='Hover'?'hover':state==='Pressed'?'pressed':'background'))];c.strokes=[];ids.push(c.id);
}
set.description='ProductButton: Primary / Secondary / Tertiary, 6 states. Secondary approved 2026-09-23: A without outline; semantic action/secondary/background, hover, pressed. Focus ring retained. Selected controls retain accent/soft.';ids.push(set.id);
return {mutatedNodeIds:ids};
'''

BOARD = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const board=await figma.getNodeByIdAsync('237:11659');await fonts(board);
for(const [id,content]of [['237:11661','Выбран A без обводки; применён к Secondary на страницах продукта. D — прежний стиль для сравнения.'],['237:11665','A · Выбран — без контура'],['245:2921','D · Прежний стиль']]){const n=await figma.getNodeByIdAsync(id);n.characters=content;ids.push(n.id);}
const note=board.findOne(n=>n.name==='Decision');note.characters='A — принят. Hover темнее, Focus с контуром. B, C и D сохранены только для сравнения.';ids.push(note.id);
for(const [cardId,label,token]of [['237:11664','Принят: тёплая серая заливка без обводки. Контур появляется при клавиатурном фокусе.','action/secondary/background'],['245:2920','Прежний стиль: очень светлая серая заливка без контура. Исторический образец.','background/sidebar']]){
const card=await figma.getNodeByIdAsync(cardId);const desc=card.findOne(n=>n.name==='OptionDescription');desc.characters=label;ids.push(desc.id);
for(const b of card.findAllWithCriteria({types:['INSTANCE']})){if(b.componentProperties.Kind?.value!=='Secondary')continue;const c=b.children.find(c=>c.name==='Control');c.fills=[paint(token)];c.strokes=[];ids.push(c.id);}}
return {mutatedNodeIds:ids};
'''

SCAN = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(PAGE));figma.skipInvisibleInstanceChildren=false;
const pending=[],exceptions=[],ok=[];
for(const n of figma.currentPage.findAllWithCriteria({types:['INSTANCE']})){
 const p=n.componentProperties;let control,state='Default';
 if(p.Kind?.value==='Secondary'){const m=await n.getMainComponentAsync();if(m?.parent?.id!=='125:450')continue;control=n.children.find(c=>c.name==='Control');state=p.State.value;}
 else if(p.Style?.value==='Default*'&&p.Color?.value==='Neutral'){
 const m=await n.getMainComponentAsync();if(m?.parent?.id!=='84:268')continue;
 let nested=false;for(let x=n.parent;x&&x.type!=='PAGE';x=x.parent)if(x.id==='125:450'||(x.type==='INSTANCE'&&x.componentProperties.Kind)){nested=true;break;}if(nested)continue;control=n;
 }else continue;
 let comparison=false;for(let top=n;top&&top.type!=='PAGE';top=top.parent)if(top.id==='164:1681'||top.id==='237:11659')comparison=true;
 if(comparison){exceptions.push([n.id,'comparison']);continue;}
 const fill=control.fills[0]?.boundVariables?.color?.id;
 if(fill==='VariableID:67:117'&&state!=='Pressed'){exceptions.push([n.id,'selected']);continue;}
 const token='action/secondary/'+(state==='Hover'?'hover':state==='Pressed'?'pressed':'background');
 if(fill!==byName[token].id||control.strokes.length)pending.push([control.id,token]);else ok.push(control.id);
}
return {pageId:PAGE,pending,exceptions,okCount:ok.length};
'''

APPLY = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(PAGE));
for(const [id,token] of ITEMS){const n=await figma.getNodeByIdAsync(id);if(!n)throw Error('Missing '+id);await fonts(n);n.fills=[paint(token)];n.strokes=[];ids.push(n.id);}
return {mutatedNodeIds:ids};
'''

if __name__ == '__main__':
    stage=sys.argv[1]
    code={'tokens':TOKENS,'masters':MASTERS,'board':BOARD,'scan':SCAN,'apply':APPLY}[stage]
    if stage in ('scan','apply'):
        code=code.replace('PAGE',json.dumps(sys.argv[2]))
    if stage=='apply':
        code=code.replace('ITEMS',sys.argv[3])
    print(json.dumps({'code':COMMON+code},ensure_ascii=False))
