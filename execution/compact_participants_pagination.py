"""Compact the pagination in the existing ParticipantsTable master."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const created=[],changed=[],removed=[];
const footer=await figma.getNodeByIdAsync('153:1050');
if(footer.children.some(n=>n.name==='CompactPagination'))return {skipped:true,footer:footer.id};
for(const t of footer.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const color=await figma.variables.getVariableByIdAsync('VariableID:67:113');
const gap=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');
const style=await figma.importStyleByKeyAsync('0ffe9932b31ce3305d4041a590cc8ec20d95f4d2');await figma.loadFontAsync(style.fontName);
const prev=await figma.getNodeByIdAsync('153:1053'),old=await figma.getNodeByIdAsync('153:1062'),next=await figma.getNodeByIdAsync('153:1073');
const pager=figma.createAutoLayout('HORIZONTAL');footer.appendChild(pager);pager.name='CompactPagination';pager.fills=[];pager.setBoundVariable('itemSpacing',gap);pager.counterAxisAlignItems='CENTER';pager.layoutSizingHorizontal='HUG';pager.layoutSizingVertical='HUG';created.push(pager.id);
const counter=figma.createText();pager.appendChild(counter);counter.name='PageCounter';await counter.setTextStyleIdAsync(style.id);counter.characters='1 из 4';counter.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',color)];counter.textAlignHorizontal='CENTER';counter.resize(60,24);counter.textAutoResize='HEIGHT';counter.layoutSizingHorizontal='FIXED';created.push(counter.id);
for(const [b,icon,name] of [[prev,'95:4','Предыдущая страница'],[next,'95:6','Следующая страница']]){pager.appendChild(b);b.name=name;b.resize(40,40);b.layoutSizingHorizontal='FIXED';b.layoutSizingVertical='FIXED';const c=b.children.find(n=>n.type==='INSTANCE'&&n.name==='Control');c.setProperties({'Icon only':'True','⮑  Icon#31150:0':icon});c.resize(32,32);c.layoutSizingHorizontal='FILL';for(const n of c.findAll(n=>['VECTOR','BOOLEAN_OPERATION','RECTANGLE','ELLIPSE'].includes(n.type)))for(const p of ['fills','strokes'])if(Array.isArray(n[p])&&n[p].length)n[p]=n[p].map(v=>v.type==='SOLID'?figma.variables.setBoundVariableForPaint(v,'color',color):v);changed.push(b.id,...b.findAll().map(n=>n.id));}
pager.insertChild(0,prev);pager.insertChild(1,counter);
removed.push(old.id,...old.findAll().map(n=>n.id));old.remove();
const scope=await figma.getNodeByIdAsync('153:1052');scope.layoutSizingHorizontal='FILL';footer.layoutSizingHorizontal='FILL';const range=await figma.getNodeByIdAsync('153:1051');range.resize(208,24);range.layoutSizingHorizontal='FIXED';changed.push(scope.id,footer.id,range.id);
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,pager:pager.id,counter:counter.id,width:pager.width,height:pager.height};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
