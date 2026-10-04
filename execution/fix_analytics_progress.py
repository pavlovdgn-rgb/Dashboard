"""Apply stable instance geometry overrides to the library progress bar."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SuccessMetric');
const changed=[],created=[];
const color=(await figma.variables.getLocalVariablesAsync('COLOR')).find(v=>v.name==='accent/strong');const radius=await figma.variables.importVariableByKeyAsync('dd2359cd4743157f5fc30993b8f29368cec946d3');
figma.skipInvisibleInstanceChildren=false;
for(const c of set.children){
 for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 c.fills=[];changed.push(c.id);
 const bar=c.children.find(n=>n.type==='INSTANCE');
 bar.setBoundVariable('minHeight',null);bar.minHeight=8;bar.setBoundVariable('maxHeight',null);bar.maxHeight=8;bar.resizeWithoutConstraints(200,8);changed.push(bar.id);
 const inner=bar.findOne(n=>n.name==='Inner');inner.visible=false;changed.push(inner.id);
 const index=c.children.indexOf(bar);const track=figma.createAutoLayout('HORIZONTAL');c.insertChild(index,track);track.name='SuccessTrack';track.resize(200,8);track.primaryAxisSizingMode='FIXED';track.counterAxisSizingMode='FIXED';track.fills=[];track.itemSpacing=0;track.appendChild(bar);track.visible=c.variantProperties.Data!=='NoData';bar.visible=true;
 const fill=figma.createRectangle();track.appendChild(fill);fill.name='RatioFill';fill.layoutPositioning='ABSOLUTE';fill.resize(200*14/18,8);fill.x=0;fill.y=0;fill.visible=c.variantProperties.Data==='Value';const value=Object.values(color.valuesByMode)[0];fill.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:value.r,g:value.g,b:value.b}},'color',color)];for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])fill.setBoundVariable(k,radius);created.push(track.id,fill.id);
}
return {mutatedNodeIds:changed,createdNodeIds:created};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
