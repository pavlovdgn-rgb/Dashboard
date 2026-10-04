"""Replace legacy text-button wrappers with direct icon-only library instances.

Do not reuse nested ProductButton text-to-icon overrides: the live canvas can
retain old label/width overrides although the MCP export renders them correctly.
"""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
figma.skipInvisibleInstanceChildren=false;
const pager=await figma.getNodeByIdAsync('294:11750');
const master=await figma.getNodeByIdAsync('84:372');
const created=[],changed=[],removed=[];
for(const old of [...pager.children].filter(n=>n.type==='INSTANCE')){
  const control=old.children.find(n=>n.name==='Control');
  for(const t of old.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
  const icon=old.name==='Предыдущая страница'?'95:4':'95:6';
  const wrapper=figma.createAutoLayout();wrapper.name=old.name;
  wrapper.layoutMode='HORIZONTAL';wrapper.fills=[];wrapper.strokes=[];
  wrapper.resize(40,40);wrapper.primaryAxisAlignItems='CENTER';wrapper.counterAxisAlignItems='CENTER';
  wrapper.paddingTop=wrapper.paddingBottom=wrapper.paddingLeft=wrapper.paddingRight=4;
  wrapper.itemSpacing=0;wrapper.clipsContent=false;wrapper.opacity=old.opacity;
  pager.insertChild(pager.children.indexOf(old),wrapper);
  wrapper.layoutSizingHorizontal='FIXED';wrapper.layoutSizingVertical='FIXED';
  for(const key of ['paddingTop','paddingBottom','paddingLeft','paddingRight']){
    if(old.boundVariables[key])wrapper.setBoundVariable(key,await figma.variables.getVariableByIdAsync(old.boundVariables[key].id));
  }
  const button=master.createInstance();wrapper.appendChild(button);
  button.name=old.name+' / IconButton';button.setProperties({'⮑  Icon#31150:0':icon,'Text#30956:4':''});
  button.resize(32,32);button.layoutSizingHorizontal='FIXED';button.layoutSizingVertical='FIXED';
  button.fills=control.fills;button.strokes=control.strokes;button.effects=control.effects;
  button.opacity=control.opacity;button.cornerRadius=control.cornerRadius;
  for(const key of ['cornerRadius','topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])if(control.boundVariables[key])button.setBoundVariable(key,await figma.variables.getVariableByIdAsync(control.boundVariables[key].id));
  const oldGlyphs=control.findAll(n=>n.type==='VECTOR'),newGlyphs=button.findAll(n=>n.type==='VECTOR');
  for(let i=0;i<newGlyphs.length;i++)if(oldGlyphs[i]){newGlyphs[i].fills=oldGlyphs[i].fills;newGlyphs[i].strokes=oldGlyphs[i].strokes;newGlyphs[i].opacity=oldGlyphs[i].opacity;}
  created.push(wrapper.id,button.id,...button.findAll().map(n=>n.id));
  removed.push(old.id,...old.findAll().map(n=>n.id));old.remove();
}
pager.clipsContent=false;changed.push(pager.id);
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,children:pager.children.map(n=>({id:n.id,name:n.name,type:n.type,x:n.x,w:n.width,h:n.height}))};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
