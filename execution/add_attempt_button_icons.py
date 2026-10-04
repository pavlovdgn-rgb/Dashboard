"""Use real library icons in the attempt-selection control; keep instances intact."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const ids=[];
const set=await figma.getNodeByIdAsync('125:450');
for(const c of set.children){for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);const ctl=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');ctl.layoutSizingHorizontal='FILL';ids.push(ctl.id);}
const action=await figma.getNodeByIdAsync('152:981');
for(const t of action.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const ctl=action.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');
const layers=await figma.importComponentByKeyAsync('43b59a8c9e5da6a2f603a2c3d9f08d06aea2eba7');
const down=await figma.importComponentByKeyAsync('ad886ce4521200a238ffe46f2c3be231e9925c81');
ctl.setProperties({'Text#30956:4':'Выбрать попытку','Icon left#30956:3':true,'Icon right#30956:5':true,'⮑  Icon left#30964:4':layers.id,'⮑  Icon right#31056:0':down.id});ids.push(ctl.id);
const token=await figma.variables.getVariableByIdAsync('VariableID:67:113');
for(const n of ctl.findAll(n=>['VECTOR','BOOLEAN_OPERATION','ELLIPSE'].includes(n.type))){for(const p of ['fills','strokes'])if(n[p].length)n[p]=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:34/255,g:36/255,b:31/255}},'color',token)];ids.push(n.id);}
return {mutatedNodeIds:ids,buttonId:action.id};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
