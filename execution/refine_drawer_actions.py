"""Apply the existing modal close pattern and library action icons to drawers."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const changed=[],created=[];
const cross=await figma.getNodeByIdAsync('106:617');
const pencil=await figma.importComponentByKeyAsync('93dde859b5a9c097f16db65da9f320265bb4422d');
const document=await figma.getNodeByIdAsync('153:1809');
const color=await figma.variables.getVariableByIdAsync('VariableID:67:113');
const bg=await figma.variables.getVariableByIdAsync('VariableID:252:3');
function paint(v){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',v);}
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
function theme(n){for(const c of n.findAll(x=>['VECTOR','BOOLEAN_OPERATION','ELLIPSE','RECTANGLE'].includes(x.type)))for(const p of ['fills','strokes'])if(Array.isArray(c[p])&&c[p].length)c[p]=c[p].map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',color):p);changed.push(n.id,...n.findAll().map(x=>x.id));}
const closes=figma.currentPage.findAll(n=>n.type==='INSTANCE'&&n.name==='Закрыть'&&/DrawerHeading|ModalHeader/.test(n.parent.name));
for(const b of closes){await fonts(b);b.resize(40,40);b.layoutSizingHorizontal='FIXED';b.layoutSizingVertical='FIXED';b.name='Закрыть';const c=b.children.find(n=>n.name==='Control');c.setProperties({'Icon only':'True','⮑  Icon#31150:0':cross.id});c.resize(32,32);c.layoutSizingHorizontal='FILL';c.fills=[paint(bg)];c.strokes=[];theme(b);}
for(const [id,icon] of [['210:19254',pencil],['210:19261',document]]){const b=await figma.getNodeByIdAsync(id);await fonts(b);const c=b.children.find(n=>n.name==='Control');c.setProperties({'Icon left#30956:3':true,'⮑  Icon left#30964:4':icon.id});b.resize(184,40);b.layoutSizingHorizontal='FIXED';c.layoutSizingHorizontal='FILL';theme(b);}
return {createdNodeIds:created,mutatedNodeIds:[...new Set(changed)],closeButtons:closes.map(n=>n.id),actionButtons:['210:19254','210:19261'],pencilId:pencil.id};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
