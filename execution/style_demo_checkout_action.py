"""Use a separate demo-storefront colour for order submission inside replay."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
let collection=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name==='Demo storefront · independent palette');
const created=[];
if(!collection){collection=figma.variables.createVariableCollection('Demo storefront · independent palette');collection.renameMode(collection.defaultModeId,'Light');created.push(collection.id);}
let token=(await figma.variables.getLocalVariablesAsync('COLOR')).find(v=>v.variableCollectionId===collection.id&&v.name==='demo/storefront/action');
if(!token){token=figma.variables.createVariable('demo/storefront/action',collection,'COLOR');created.push(token.id);}
token.scopes=['FRAME_FILL','SHAPE_FILL'];token.setVariableCodeSyntax('WEB','var(--demo-storefront-action)');
token.setValueForMode(collection.defaultModeId,{r:124/255,g:58/255,b:237/255,a:1});
const ids=[],checks=[];
for(const id of ['209:6687','210:15356','210:19579','210:20116']){
 const b=await figma.getNodeByIdAsync(id);if(b.name!=='Отправить заказ'||b.parent.name!=='FormPreview')throw Error('Unexpected target '+id);
 for(const t of b.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const c=b.children.find(n=>n.name==='Control');c.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:124/255,g:58/255,b:237/255}},'color',token)];ids.push(c.id);
 checks.push({buttonId:b.id,controlId:c.id,background:c.fills[0].boundVariables.color.id,text:c.findAllWithCriteria({types:['TEXT']}).filter(t=>t.visible).map(t=>({label:t.characters,fill:t.fills}))});
}
return {createdVariableIds:created,mutatedNodeIds:ids,collectionId:collection.id,tokenId:token.id,token:token.name,hex:'#7C3AED',checks};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
