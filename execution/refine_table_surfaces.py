"""Bind consistent cell padding and rounded table clipping to existing tokens."""
import json
import sys

MASTER = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='82:3'));
const set=await figma.getNodeByIdAsync('203:5669');
const spacing=await figma.variables.importVariableByKeyAsync('723a30bab117da7a71b48251ea5a84eb3614f264');
const ids=[];
for(const row of set.children.slice(START,END)){
 for(const t of row.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 for(const cell of row.children){const content=cell.findOne(n=>n.type==='FRAME'&&n.name==='Cell');if(!content)throw Error('Cell content missing');content.setBoundVariable('paddingLeft',spacing);content.setBoundVariable('paddingRight',spacing);ids.push(content.id);}
}
return {mutatedNodeIds:ids};
'''
SURFACES = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');const ids=[];
for(const id of ['210:11005','210:12824','210:14133','210:17934']){
 const n=await figma.getNodeByIdAsync(id);
 for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 for(const field of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(field,radius);
 n.clipsContent=true;n.setBoundVariable('itemSpacing',null);n.itemSpacing=0;ids.push(n.id);
}
return {mutatedNodeIds:ids};
'''
if __name__ == '__main__':
    stage=sys.argv[1]
    code=SURFACES if stage=='surfaces' else MASTER.replace('START',str(int(stage)*7)).replace('END',str(int(stage)*7+7))
    print(json.dumps({'code':code},ensure_ascii=False))
