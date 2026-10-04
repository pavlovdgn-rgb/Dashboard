"""Align ParticipantsTable toolbar to its surface and group related filters."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const created=[],changed=[],variants=[];
const set=await figma.getNodeByIdAsync('153:1605');
const tokens={};for(const [k,key] of Object.entries({sm:'c6350febff91d7248df73477a27c5387155ac6c2',base:'723a30bab117da7a71b48251ea5a84eb3614f264',lg:'e34de5efd30aef81f5d652fe45dc113b59cc6e1a'}))tokens[k]=await figma.variables.importVariableByKeyAsync(key);
function group(parent,name,gap){const n=figma.createAutoLayout('HORIZONTAL');parent.appendChild(n);n.name=name;n.fills=[];n.setBoundVariable('itemSpacing',tokens[gap]);n.counterAxisAlignItems='CENTER';n.layoutSizingHorizontal='HUG';n.layoutSizingVertical='HUG';created.push(n.id);return n;}
for(const variant of set.children){
 const bar=variant.children.find(n=>n.name==='Toolbar');
 if(!bar)continue;
 for(const t of bar.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const count=bar.children.find(n=>n.name==='Count');
 let controls=bar.children.find(n=>n.name==='SearchAndFilters');
 if(!controls){
  const search=bar.children.find(n=>n.name==='SearchByParticipantId');const filters=bar.children.filter(n=>n.type==='INSTANCE'&&n!==search);
  if(!search||filters.length!==2)throw Error('Unexpected toolbar structure: '+bar.id);
  controls=group(bar,'SearchAndFilters','base');controls.appendChild(search);
  search.resize(360,40);search.layoutSizingHorizontal='FIXED';search.layoutSizingVertical='FIXED';search.primaryAxisAlignItems='CENTER';changed.push(search.id);
  const fg=group(controls,'OutcomeAndDataFilters','sm');
  for(const [index,b] of filters.entries()){
   fg.appendChild(b);b.name=index===0?'OutcomeFilter':'DataCompletenessFilter';b.resize(168,40);b.layoutSizingHorizontal='FIXED';b.layoutSizingVertical='FIXED';
   const control=b.children.find(n=>n.name==='Control');control.layoutSizingHorizontal='FILL';changed.push(b.id,control.id);
  }
 }
 bar.layoutSizingHorizontal='FILL';bar.layoutSizingVertical='HUG';bar.counterAxisAlignItems='CENTER';bar.setBoundVariable('itemSpacing',tokens.lg);
 count.layoutSizingHorizontal='FILL';count.textAutoResize='HEIGHT';changed.push(bar.id,count.id);
 variants.push({id:variant.id,toolbar:bar.id,controls:controls.id,width:bar.width,height:bar.height});
}
return {createdNodeIds:created,mutatedNodeIds:changed,variants};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
