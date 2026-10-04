"""Keep incomplete-count badges only on unselected scenario rows."""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=await figma.getNodeByIdAsync('135:1062');
const token=await figma.variables.getVariableByIdAsync('VariableID:67:113');
const bg=await figma.variables.getVariableByIdAsync('VariableID:67:109');
const ids=[];
for(const c of set.children){
 const badge=c.findOne(n=>n.name==='IncompleteBadge');
 const t=c.findOne(n=>n.type==='TEXT'&&n.name==='Incomplete');
 if(!badge||!t)throw Error('Missing incomplete count in '+c.id);
 for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 badge.fills=c.variantProperties.Selected==='True'?[]:[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:243/255,g:243/255,b:238/255}},'color',bg)];badge.strokes=[];
 t.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:34/255,g:36/255,b:31/255}},'color',token)];
 ids.push(badge.id,t.id);
}
return {mutatedNodeIds:ids,variants:set.children.length};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE}))
