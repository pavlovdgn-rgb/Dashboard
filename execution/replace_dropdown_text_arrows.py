"""Replace text triangles with bound library icons in product UI-kit controls."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const icon=await figma.importComponentByKeyAsync('ad886ce4521200a238ffe46f2c3be231e9925c81');
const color=await figma.variables.getVariableByIdAsync('VariableID:67:113');
const ids=[],controls=[];
for(const t of figma.currentPage.findAllWithCriteria({types:['TEXT']}).filter(t=>/[▾▿▼⌄]/.test(t.characters))){
let c=t.parent;while(c&&!(c.type==='INSTANCE'&&c.name==='Control'))c=c.parent;if(!c)continue;
for(const tx of c.findAllWithCriteria({types:['TEXT']}))for(const s of tx.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
c.setProperties({'Text#30956:4':t.characters.replace(/[▾▿▼⌄]/g,'').trim(),'Icon right#30956:5':true,'⮑  Icon right#31056:0':icon.id});ids.push(c.id);
for(const n of c.findAll(n=>['VECTOR','BOOLEAN_OPERATION'].includes(n.type))){for(const p of ['fills','strokes'])if(n[p].length)n[p]=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:34/255,g:36/255,b:31/255}},'color',color)];ids.push(n.id);}
controls.push(c.id);
}
return {mutatedNodeIds:ids,controls,remaining:figma.currentPage.findAllWithCriteria({types:['TEXT']}).filter(t=>/[▾▿▼⌄]/.test(t.characters)).map(t=>({id:t.id,text:t.characters}))};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
