"""Restore the flat ScenarioTable composition while retaining row separators."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=await figma.getNodeByIdAsync('136:715');
const border=await figma.variables.getVariableByIdAsync('VariableID:67:111');
const paint=figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',border);
const shadow=(await figma.getLocalEffectStylesAsync()).find(n=>n.name==='shadow/card');
const changed=[],removed=[],checks=[];
for(const c of set.children){const grid=c.children.find(n=>n.name==='TableGrid');if(!grid)continue;
for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const position=c.children.indexOf(grid),children=[...grid.children];
for(let i=0;i<children.length;i++){c.insertChild(position+i,children[i]);children[i].layoutSizingHorizontal='FILL';changed.push(children[i].id);}
removed.push(grid.id);grid.remove();c.strokes=[paint];c.strokeWeight=1;c.strokeAlign='INSIDE';await c.setEffectStyleIdAsync(shadow.id);changed.push(c.id);
checks.push({id:c.id,state:c.variantProperties.State,children:c.children.map(n=>({id:n.id,name:n.name})),dividers:c.findAll(n=>n.name==='RowDivider').length});}
return {mutatedNodeIds:changed,removedNodeIds:removed,checks};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
