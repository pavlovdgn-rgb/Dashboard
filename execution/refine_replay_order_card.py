"""Separate the demonstration checkout's order summary from its form."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const background=await figma.variables.getVariableByIdAsync('VariableID:67:109');
const border=await figma.variables.getVariableByIdAsync('VariableID:67:111');
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
const padding=await figma.variables.importVariableByKeyAsync('e34de5efd30aef81f5d652fe45dc113b59cc6e1a');
function paint(v){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',v);}
const mutated=[],cards=[];
for(const id of ['209:6694','210:15363','210:19586','210:20123']){
 const n=await figma.getNodeByIdAsync(id);if(n.type!=='FRAME'||n.name!=='OrderPreview')throw Error('Unexpected order block '+id);
 for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 n.fills=[paint(background)];n.strokes=[paint(border)];n.strokeWeight=1;n.strokeAlign='INSIDE';n.strokesIncludedInLayout=false;
 for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(p,radius);
 for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n.setBoundVariable(p,padding);
 n.layoutSizingVertical='HUG';mutated.push(n.id);
 cards.push({id:n.id,width:n.width,height:n.height,padding:n.paddingLeft,radius:n.topLeftRadius,overflow:n.children.filter(c=>c.x<n.paddingLeft-.5||c.x+c.width>n.width-n.paddingRight+.5||c.y+c.height>n.height-n.paddingBottom+.5).map(c=>c.id)});
}
return {mutatedNodeIds:mutated,cards,passed:cards.every(c=>!c.overflow.length)};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
