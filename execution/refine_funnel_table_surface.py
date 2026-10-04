"""Remove the nested card treatment from the scenario steps table."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const table=await figma.getNodeByIdAsync('210:7729');
for(const t of table.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
table.strokes=[];await table.setEffectStyleIdAsync('');table.effects=[];
for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])table.setBoundVariable(k,null);
table.cornerRadius=0;
const border=await figma.variables.getVariableByIdAsync('VariableID:67:111');
const paint=figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',border);
const changed=[table.id];
for(const row of table.children.slice(0,-1)){row.strokes=[paint];row.strokeAlign='INSIDE';row.strokeTopWeight=0;row.strokeLeftWeight=0;row.strokeRightWeight=0;row.strokeBottomWeight=1;changed.push(row.id);}
return {mutatedNodeIds:changed,table:{strokes:table.strokes,effects:table.effects,radius:table.cornerRadius},outerPanel:table.parent.id};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
