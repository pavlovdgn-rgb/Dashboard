"""Separate ScenarioTable grid from its surrounding white card, using existing tokens."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const table=await figma.getNodeByIdAsync('136:715');
const vars=await figma.variables.getLocalVariablesAsync();const byName=name=>vars.find(v=>v.name===name);
const paint=name=>figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',byName(name));
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
const created=[],mutated=[],checks=[];
for(const c of table.children){
 const header=c.findOne(n=>n.name==='TableHeader'),body=c.findOne(n=>n.name==='ScenarioRows');
 if(!header||!body)continue;
 for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 let grid=c.children.find(n=>n.name==='TableGrid');
 if(!grid){grid=figma.createAutoLayout();created.push(grid.id);grid.name='TableGrid';grid.layoutMode='VERTICAL';grid.primaryAxisSizingMode='AUTO';grid.counterAxisSizingMode='FIXED';grid.itemSpacing=0;c.insertChild(c.children.indexOf(header),grid);grid.layoutSizingHorizontal='FILL';grid.appendChild(header);grid.appendChild(body);}
 grid.fills=[paint('background/surface')];grid.strokes=[paint('border/subtle')];grid.strokeWeight=1;grid.strokeAlign='INSIDE';grid.clipsContent=true;grid.setBoundVariable('cornerRadius',radius);
 header.layoutSizingHorizontal='FILL';body.layoutSizingHorizontal='FILL';
 header.fills=[paint('background/sidebar')];header.strokes=[paint('border/subtle')];header.strokeTopWeight=0;header.strokeLeftWeight=0;header.strokeRightWeight=0;header.strokeBottomWeight=1;header.strokeAlign='INSIDE';
 const rows=body.children.filter(n=>n.type==='INSTANCE');
 if(!body.children.some(n=>n.name==='RowDivider'))for(let i=rows.length-1;i>0;i--){const line=figma.createAutoLayout();created.push(line.id);line.name='RowDivider';line.fills=[paint('border/subtle')];line.primaryAxisSizingMode='FIXED';line.counterAxisSizingMode='FIXED';line.resize(body.width,1);body.insertChild(body.children.indexOf(rows[i]),line);line.layoutSizingHorizontal='FILL';}
 mutated.push(c.id,grid.id,header.id,body.id,...body.children.map(n=>n.id));checks.push({id:c.id,state:c.variantProperties.State,grid:grid.id,w:grid.width,h:grid.height,dividers:body.children.filter(n=>n.name==='RowDivider').length});
}
return {createdNodeIds:created,mutatedNodeIds:mutated,checks};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
