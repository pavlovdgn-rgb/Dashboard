"""Add linked arrowLeft icons to the results overview return links."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const master=await figma.getNodeByIdAsync('95:4');
const gap=await figma.variables.getVariableByIdAsync('VariableID:c6350febff91d7248df73477a27c5387155ac6c2/45334:7');
const created=[],mutated=[];
for(const id of ['205:6730','210:14505','210:14898']){
const t=await figma.getNodeByIdAsync(id);for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
if(t.parent.name==='BackToResults')continue;
const p=t.parent,row=figma.createAutoLayout();row.name='BackToResults';row.layoutMode='HORIZONTAL';row.fills=[];row.primaryAxisSizingMode='AUTO';row.counterAxisSizingMode='AUTO';row.counterAxisAlignItems='CENTER';row.setBoundVariable('itemSpacing',gap);p.insertChild(p.children.indexOf(t),row);
const icon=master.createInstance();icon.name='Back / arrowLeft';row.appendChild(icon);row.appendChild(t);t.textAutoResize='WIDTH_AND_HEIGHT';t.layoutSizingHorizontal='HUG';
for(const v of icon.findAll(n=>n.type==='VECTOR')){if(v.fills.length)v.fills=t.fills;if(v.strokes.length)v.strokes=t.fills;}
created.push(row.id,icon.id,...icon.findAll().map(n=>n.id));mutated.push(t.id,p.id);
}
return {createdNodeIds:created,mutatedNodeIds:mutated,prototypeNavigationAdded:false};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
