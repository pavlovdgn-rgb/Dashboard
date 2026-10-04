"""Align project-count metadata with the input, excluding its label."""
import json
CODE=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const created=[],mutated=[];
for(const id of ['203:7351','207:6522']){
 const t=await figma.getNodeByIdAsync(id);for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 if(t.parent.name==='SearchMetadata')continue;
 const row=t.parent;const width=t.width;const slot=figma.createAutoLayout('HORIZONTAL');slot.name='SearchMetadata';slot.fills=[];slot.resize(width,40);slot.primaryAxisSizingMode='FIXED';slot.counterAxisSizingMode='FIXED';slot.counterAxisAlignItems='CENTER';slot.itemSpacing=0;
 row.insertChild(row.children.indexOf(t),slot);slot.layoutSizingHorizontal='FILL';slot.layoutSizingVertical='FIXED';slot.appendChild(t);t.layoutSizingHorizontal='FILL';t.textAutoResize='HEIGHT';row.counterAxisAlignItems='MAX';
 created.push(slot.id);mutated.push(t.id,row.id);
}
return {createdNodeIds:created,mutatedNodeIds:mutated};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
