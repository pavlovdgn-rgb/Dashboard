"""Improve Studies summary detail and align its search/status filters."""
import json
import sys

COMMON=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const ids=[],created=[];
'''
FILTERS=r'''
const row=await figma.getNodeByIdAsync('205:6211'),search=await figma.getNodeByIdAsync('205:6220');await fonts(row);
const master=await figma.getNodeByIdAsync('203:4240');await fonts(master);
let status=row.children.find(n=>n.name==='Field/Статус исследования');
if(!status){status=master.createInstance();row.appendChild(status);created.push(status.id);}
await fonts(status);status.name='Field/Статус исследования';
status.setProperties({'Label#203:42':'Статус исследования','ShowHelp#203:84':false});
status.findOne(n=>n.type==='TEXT'&&n.name==='InputValue').characters='Все статусы';
status.resize(240,status.height);status.layoutSizingHorizontal='FIXED';status.layoutSizingVertical='HUG';
row.insertChild(0,search);search.resize(row.width-row.itemSpacing-240,search.height);search.layoutSizingHorizontal='FILL';search.layoutSizingVertical='HUG';
row.counterAxisAlignItems='MAX';row.primaryAxisSizingMode='FIXED';
const old=row.children.find(n=>n.id==='205:6212');const removed=[];if(old){removed.push(old.id);old.remove();}
ids.push(row.id,search.id,status.id,...status.findAll().map(n=>n.id));
return {createdNodeIds:created,mutatedNodeIds:ids,removedNodeIds:removed,statusId:status.id};
'''
METRICS=r'''
const configs=[
 ['205:6160','Всего исследований','3','1 идёт сбор · 1 черновик · 1 завершено','2 с заданиями · 1 в свободном режиме',false,''],
 ['205:6177','Идёт сбор','1 из 3','Доля исследований с открытым сбором','20 участников в активном исследовании',true,'33%'],
 ['205:6194','Черновики','1 из 3','Доля исследований, ожидающих запуска','«Навигация каталога» · 2 сценария',true,'33%']
];
for(const [id,label,value,hint,detail,showBadge,badge]of configs){
 const n=await figma.getNodeByIdAsync(id);await fonts(n);
 n.setProperties({'Label#171:0':label,'Value#171:4':value,'Hint#171:8':hint,'Detail#202:0':detail,'ShowBadge#202:8':showBadge,'Badge#202:4':badge,'ShowProgress#202:12':false,'ShowLink#171:12':false});
 n.resize(n.width,208);n.layoutSizingVertical='FIXED';ids.push(n.id,...n.findAll().map(c=>c.id));
}
return {mutatedNodeIds:ids};
'''
AUDIT=r'''
const row=await figma.getNodeByIdAsync('205:6211');const fields=row.children.filter(n=>n.type==='INSTANCE');
const positions=fields.map(n=>{const c=n.children.find(x=>x.name==='Control');return {id:n.id,name:n.name,x:n.x,w:n.width,top:n.y+c.y,height:c.height,bottom:n.y+c.y+c.height};});
const metrics=[];for(const id of ['205:6160','205:6177','205:6194']){const n=await figma.getNodeByIdAsync(id);metrics.push({id,height:n.height,text:n.findAllWithCriteria({types:['TEXT']}).filter(n=>n.visible).map(n=>n.characters),overflow:n.children.filter(c=>c.visible&&c.y+c.height>n.height).map(c=>c.id)});}
return {positions,metrics,aligned:positions.length===2&&positions[0].top===positions[1].top&&positions[0].height===positions[1].height};
'''
if __name__=='__main__':
    print(json.dumps({'code':COMMON+{'filters':FILTERS,'metrics':METRICS,'audit':AUDIT}[sys.argv[1]]}))
