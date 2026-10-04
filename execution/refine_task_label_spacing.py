"""Keep the task label visually attached to its input in both Figma states."""
import json

CODE = r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const created=[],mutated=[],checks=[];
const gap=await figma.variables.getVariableByIdAsync('VariableID:c6350febff91d7248df73477a27c5387155ac6c2/45334:7');
for(const [formId,rowId,labelId,inputId] of [['210:9244','345:10738','210:9261','210:9262'],['210:9567','345:10745','210:9584','210:9585']]){
 const [form,row,label,input]=await Promise.all([formId,rowId,labelId,inputId].map(id=>figma.getNodeByIdAsync(id)));
 for(const t of form.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 let block=form.children.find(n=>n.name==='TaskTextField');
 if(!block){block=figma.createAutoLayout();created.push(block.id);block.name='TaskTextField';block.layoutMode='VERTICAL';block.fills=[];block.primaryAxisSizingMode='AUTO';block.counterAxisSizingMode='FIXED';form.insertChild(form.children.indexOf(row),block);block.layoutSizingHorizontal='FILL';block.appendChild(row);block.appendChild(input);}
 block.setBoundVariable('itemSpacing',gap);
 row.layoutSizingHorizontal='FILL';input.layoutSizingHorizontal='FILL';
 row.counterAxisAlignItems='MAX';label.textAutoResize='HEIGHT';label.layoutSizingVertical='HUG';label.textAlignVertical='BOTTOM';
 mutated.push(form.id,block.id,...block.findAll().map(n=>n.id));
 checks.push({form:form.id,block:block.id,gap:input.y-(row.y+label.y+label.height),labelHeight:label.height});
}
return {createdNodeIds:created,mutatedNodeIds:mutated,checks};
"""

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
