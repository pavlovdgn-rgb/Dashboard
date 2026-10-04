"""Replace ad-hoc task options with linked TaskChoiceCard instances."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const parent=await figma.getNodeByIdAsync('210:9625'),set=await figma.getNodeByIdAsync('260:3028');
const created=[],mutated=[],removed=[];
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
await fonts(parent);await fonts(set);
for(const [oldId,selected,title,description]of[
 ['210:9636','True','Найти товар','Найдите подходящий товар и откройте его карточку.'],
 ['210:9639','False','Добавить товар в корзину','Выберите товар и добавьте его в корзину.'],
 ['210:9642','False','Оформить заказ','Оформите заказ на выбранный товар.']
]){
 const old=await figma.getNodeByIdAsync(oldId);if(!old)continue;
 const m=set.children.find(n=>n.variantProperties.Selected===selected&&n.variantProperties.State==='Default');const n=m.createInstance();created.push(n.id);parent.insertChild(parent.children.indexOf(old),n);n.name='TaskChoice/'+title;
 n.setProperties({'Title#260:0':title,'Description#260:9':description});n.resize(old.width,n.height);n.layoutSizingHorizontal='FILL';n.layoutSizingVertical='HUG';removed.push(old.id);old.remove();
}
parent.y=(parent.parent.height-parent.height)/2;mutated.push(parent.id);
return {createdNodeIds:created,mutatedNodeIds:mutated,removedNodeIds:removed,modalHeight:parent.height,modalY:parent.y};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
