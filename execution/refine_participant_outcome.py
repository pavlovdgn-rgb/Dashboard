"""Separate participant outcome selection from the next-step action."""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const panel=await figma.getNodeByIdAsync('210:11860');
const radio=await figma.getNodeByIdAsync('260:2937');
const source=await figma.getNodeByIdAsync('260:2944');
const instruction=await figma.getNodeByIdAsync('210:11863');
const next=await figma.getNodeByIdAsync('210:11864');
const old=await figma.getNodeByIdAsync('210:11871');
const disabled=await figma.getNodeByIdAsync('125:396');
for(const root of [panel,disabled])for(const t of root.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
for(const s of source.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
instruction.characters='Отметьте результат задания, затем нажмите «Далее».';
const group=figma.createAutoLayout();group.name='TaskOutcomeSelection';group.layoutMode='VERTICAL';group.fills=[];
group.itemSpacing=8;group.paddingTop=group.paddingBottom=group.paddingLeft=group.paddingRight=0;
panel.insertChild(panel.children.indexOf(next),group);group.layoutSizingHorizontal='FILL';group.layoutSizingVertical='HUG';
const gap=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');group.setBoundVariable('itemSpacing',gap);
const created=[group.id];
for(const [name,label] of [['Completed','Выполнил задание'],['Unable','Не удалось выполнить']]){
  const row=figma.createAutoLayout();group.appendChild(row);row.name='OutcomeOption / '+name;
  row.layoutMode='HORIZONTAL';row.fills=[];row.resize(group.width,40);row.layoutSizingHorizontal='FILL';row.layoutSizingVertical='FIXED';
  row.counterAxisAlignItems='CENTER';row.setBoundVariable('itemSpacing',gap);
  row.paddingTop=row.paddingBottom=row.paddingLeft=row.paddingRight=0;
  const control=radio.clone();row.appendChild(control);control.name='Radio';control.resize(16,16);control.layoutSizingHorizontal='FIXED';control.layoutSizingVertical='FIXED';
  const title=source.clone();row.appendChild(title);title.name='OutcomeLabel';title.characters=label;title.textAutoResize='HEIGHT';title.layoutSizingHorizontal='FILL';
  created.push(row.id,control.id,...control.findAll().map(n=>n.id),title.id);
}
next.swapComponent(disabled);next.name='Далее';next.resize(panel.width-panel.paddingLeft-panel.paddingRight,40);next.layoutSizingHorizontal='FILL';
const c=next.children.find(n=>n.name==='Control');c.setProperties({'Text#30956:4':'Далее','Icon left#30956:3':false,'Icon right#30956:5':false});
const removed=[old.id,...old.findAll().map(n=>n.id)];old.remove();panel.layoutSizingVertical='HUG';
return {createdNodeIds:created,mutatedNodeIds:[panel.id,instruction.id,next.id,...next.findAll().map(n=>n.id)],removedNodeIds:removed,panel:{id:panel.id,w:panel.width,h:panel.height},selection:group.id,nextButton:next.id};
'''

if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
