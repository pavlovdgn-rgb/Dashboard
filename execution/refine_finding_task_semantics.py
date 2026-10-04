"""Emit repeatable Figma corrections: actions, editable metadata, task vs criterion."""
import json

CODE = r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const changed=new Set(), created=[];
const get=id=>figma.getNodeByIdAsync(id);
async function fonts(n){const ts=n.type==='TEXT'?[n]:n.findAllWithCriteria({types:['TEXT']});for(const t of ts)for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
function mark(n){changed.add(n.id);if('findAll'in n)for(const c of n.findAll())changed.add(c.id);}
async function label(n,value){await fonts(n);if(n.type==='TEXT')n.characters=value;else {const c=n.findOne(x=>x.type==='INSTANCE'&&Object.keys(x.componentProperties).some(k=>k.startsWith('Text#')));if(!c)throw Error('No text property: '+n.id);const key=Object.keys(c.componentProperties).find(k=>k.startsWith('Text#'));c.setProperties({[key]:value});}mark(n);}
const tertiary=await get('125:326'),select=await get('203:4240');await fonts(tertiary);await fonts(select);
const secondaryAction=await get('210:19751');await fonts(secondaryAction);secondaryAction.swapComponent(tertiary);await label(secondaryAction,'Добавить к существующей находке');secondaryAction.resize(300,40);secondaryAction.name='Добавить к существующей находке';mark(secondaryAction);
const metadata=await get('210:19758');metadata.name='FindingMetadataFields';metadata.primaryAxisSizingMode='FIXED';metadata.counterAxisSizingMode='AUTO';metadata.resize(688,76);metadata.layoutSizingHorizontal='FILL';
for(const [id,title,value] of [['210:19759','Приоритет','Не задан'],['210:19766','Статус проверки','Нужно проверить']]){const n=await get(id);await fonts(n);n.swapComponent(select);n.setProperties({'Label#203:42':title,'ShowHelp#203:84':false});n.name='Field/'+title;n.resize((metadata.width-metadata.itemSpacing)/2,76);n.layoutSizingHorizontal='FILL';await fonts(n);const t=n.findOne(x=>x.type==='TEXT'&&x.name==='InputValue');if(!t)throw Error('No InputValue');t.characters=value;mark(n);}mark(metadata);
const drawer=await get('210:19682');await fonts(drawer);drawer.clipsContent=true;drawer.overflowDirection='VERTICAL';mark(drawer);
for(const ids of [['210:9281','210:9244','210:9261','210:9293','210:9285'],['210:9604','210:9567','210:9584','210:9616','210:9608']]){
 const [card,form,heading,choose,note]=await Promise.all(ids.map(get));await fonts(card);await fonts(form);
 choose.swapComponent(tertiary);await label(choose,'Выбрать задание из списка');choose.resize(236,40);
 let row=form.children.find(n=>n.name==='TaskTextHeading');if(!row){row=figma.createAutoLayout();created.push(row.id);row.name='TaskTextHeading';row.layoutMode='HORIZONTAL';row.fills=[];row.primaryAxisSizingMode='FIXED';row.counterAxisSizingMode='AUTO';row.primaryAxisAlignItems='SPACE_BETWEEN';row.counterAxisAlignItems='CENTER';const pos=form.children.indexOf(heading);form.insertChild(pos,row);row.layoutSizingHorizontal='FILL';row.appendChild(heading);heading.layoutSizingHorizontal='FILL';row.setBoundVariable('itemSpacing',await figma.variables.getVariableByIdAsync('VariableID:723a30bab117da7a71b48251ea5a84eb3614f264/45334:3'));}
 row.appendChild(choose);choose.layoutSizingHorizontal='FIXED';
 await label(note,'Задание выполнено, когда участник открывает целевую страницу.');
 card.primaryAxisSizingMode='AUTO';card.layoutSizingVertical='HUG';form.primaryAxisSizingMode='AUTO';form.layoutSizingVertical='HUG';const workspace=card.parent;workspace.primaryAxisSizingMode='FIXED';workspace.counterAxisSizingMode='AUTO';workspace.counterAxisAlignItems='MIN';mark(workspace);mark(row);
}
return {createdNodeIds:created,mutatedNodeIds:[...changed],screens:['210:19268'],panels:['210:19682','210:9243',(await get('210:9604')).parent.id],metadata:metadata.children.map(n=>({id:n.id,type:n.variantProperties,w:n.width,h:n.height}))};
"""

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
