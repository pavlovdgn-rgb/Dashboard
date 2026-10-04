"""Final table composition: heading and note outside the sole table surface."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=await figma.getNodeByIdAsync('136:715');
const vars=await figma.variables.getLocalVariablesAsync();
const paint=name=>figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:1,g:1,b:1}},'color',vars.find(v=>v.name===name));
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
const gap=await figma.variables.getVariableByIdAsync('VariableID:723a30bab117da7a71b48251ea5a84eb3614f264/45334:3');
const shadow=(await figma.getLocalEffectStylesAsync()).find(s=>s.name==='shadow/card');
const created=[],changed=[],checks=[];
for(const c of set.children){
 for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const header=c.findOne(n=>n.name==='TableHeader'),body=c.findOne(n=>n.name==='ScenarioRows'||n.name==='StateMessage');
 if(!header||!body)throw Error('Missing table content: '+c.id);
 let grid=c.children.find(n=>n.name==='TableSurface');
 if(!grid){grid=figma.createAutoLayout();created.push(grid.id);grid.name='TableSurface';grid.layoutMode='VERTICAL';grid.primaryAxisSizingMode='AUTO';grid.counterAxisSizingMode='FIXED';grid.itemSpacing=0;c.insertChild(c.children.indexOf(header),grid);grid.layoutSizingHorizontal='FILL';grid.appendChild(header);grid.appendChild(body);}
 c.fills=[];c.strokes=[];await c.setEffectStyleIdAsync('');c.effects=[];
 for(const k of ['paddingLeft','paddingTop','paddingRight','paddingBottom']){c.setBoundVariable(k,null);c[k]=0;}
 for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])c.setBoundVariable(k,null);
 c.cornerRadius=0;c.clipsContent=false;c.setBoundVariable('itemSpacing',gap);
 grid.fills=[paint('background/surface')];grid.strokes=[paint('border/subtle')];grid.strokeWeight=1;grid.strokeAlign='INSIDE';grid.setBoundVariable('cornerRadius',radius);grid.clipsContent=true;await grid.setEffectStyleIdAsync(shadow.id);
 header.layoutSizingHorizontal='FILL';body.layoutSizingHorizontal='FILL';header.fills=[paint('background/sidebar')];
 if(body.name==='ScenarioRows'){const rows=body.children.filter(n=>n.type==='INSTANCE');rows.forEach((r,i)=>{r.fills=[paint(r.variantProperties.Selected==='True'?'accent/soft':i%2?'background/subtle':'background/surface')];changed.push(r.id);});}
 changed.push(c.id,grid.id,header.id,body.id);
 checks.push({id:c.id,state:c.variantProperties.State,background:c.fills,table:grid.id,w:grid.width,h:grid.height,headingOutside:c.children.find(n=>n.name==='Title')?.parent.id===c.id});
}
return {createdNodeIds:created,mutatedNodeIds:changed,checks};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
