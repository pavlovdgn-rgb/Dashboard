"""Use linked single-choice cards for the three criterion types in all states."""
import json

CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const set=await figma.getNodeByIdAsync('260:3028');
const spacing=await figma.variables.getVariableByIdAsync('VariableID:723a30bab117da7a71b48251ea5a84eb3614f264/45334:3');
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
await fonts(set);const mutated=[],checks=[];
const titles=['Целевая страница','Целевая кнопка','Последовательность'];
const descriptions=['Открытие заданной страницы','Нажатие выбранной кнопки','Несколько действий по порядку'];
for(const [rowId,selected] of [['210:8131',2],['210:9927',0],['210:10262',1]]){
 const row=await figma.getNodeByIdAsync(rowId);await fonts(row);row.name='CriterionTypeChoices';row.primaryAxisSizingMode='FIXED';row.counterAxisSizingMode='AUTO';
 const width=(row.width-row.itemSpacing*2)/3;
 for(let i=0;i<3;i++){
  const n=row.children[i],master=set.children.find(c=>c.variantProperties.Selected===(i===selected?'True':'False')&&c.variantProperties.State==='Default');
  n.swapComponent(master);n.name='CriterionType/'+titles[i];n.setProperties({'Title#260:0':titles[i],'Description#260:9':descriptions[i]});
  const surface=await figma.variables.getVariableByIdAsync(i===selected?'VariableID:67:117':'VariableID:67:108');
  n.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:1,g:1,b:1}},'color',surface)];
  for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n.setBoundVariable(p,spacing);
  n.resize(width,88);n.layoutSizingHorizontal='FILL';n.layoutSizingVertical='HUG';mutated.push(n.id,...n.findAll().map(c=>c.id));
 }
 mutated.push(row.id);checks.push({row:row.id,height:row.height,choices:row.children.map(n=>({id:n.id,w:n.width,h:n.height,selected:n.variantProperties.Selected}))});
}
return {mutatedNodeIds:mutated,checks};
"""

if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
