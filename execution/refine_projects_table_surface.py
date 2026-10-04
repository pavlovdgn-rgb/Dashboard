"""Apply existing border and card-shadow tokens to both ProjectsTable compositions."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const border=await figma.variables.getVariableByIdAsync('VariableID:67:111');
const paint=figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',border);
const shadow=(await figma.getLocalEffectStylesAsync()).find(s=>s.name==='shadow/card');if(!shadow)throw Error('Missing shadow/card');
const changed=[],checks=[];
for(const id of ['203:7354','207:6525']){
 const n=await figma.getNodeByIdAsync(id);for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 n.strokes=[paint];n.strokeWeight=1;n.strokeAlign='INSIDE';await n.setEffectStyleIdAsync(shadow.id);
 for(const row of n.children.slice(0,-1)){row.strokes=[paint];row.strokeAlign='INSIDE';row.strokeTopWeight=0;row.strokeLeftWeight=0;row.strokeRightWeight=0;row.strokeBottomWeight=1;changed.push(row.id);}
 changed.push(n.id);checks.push({id:n.id,border:n.strokes,effect:n.effectStyleId});
}
return {mutatedNodeIds:changed,checks};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
