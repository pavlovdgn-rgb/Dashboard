"""Finish the approved participant flow using existing Figma components."""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const created=[],changed=[],removed=[];
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const outcome=await figma.getNodeByIdAsync('I337:10428;203:5139;15038:108422');await fonts(outcome);outcome.setProperties({'Text#32296:32':'Нет оценки'});changed.push(outcome.id,...outcome.findAll().map(n=>n.id));
const panel=await figma.getNodeByIdAsync('210:17096');await fonts(panel);
const old=await figma.getNodeByIdAsync('210:17099');if(old){removed.push(old.id,...old.findAll().map(n=>n.id));old.remove();}
for(const id of ['330:10366','210:11864']){const source=await figma.getNodeByIdAsync(id);if(panel.children.some(n=>n.name===source.name))continue;await fonts(source);const n=source.clone();panel.appendChild(n);n.layoutSizingHorizontal='FILL';created.push(n.id,...n.findAll().map(n=>n.id));}
const body=await figma.getNodeByIdAsync('210:17093');body.clipsContent=true;body.overflowDirection='VERTICAL';changed.push(panel.id,body.id);
const sourcePhoto=await figma.getNodeByIdAsync('210:11828'),photo=await figma.getNodeByIdAsync('210:17116');photo.fills=sourcePhoto.fills;for(const n of photo.children){n.visible=false;changed.push(n.id);}changed.push(photo.id);
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,mobile:'210:17090',outcome:'337:10406'};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
