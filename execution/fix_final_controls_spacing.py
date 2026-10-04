"""Keep selected button backgrounds and contiguous table rows consistent."""
import json
import sys

COMMON = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const mutated=[];
'''
BUTTONS = r'''
const ids=IDS;
for(const id of ids){
 const n=await figma.getNodeByIdAsync(id);
 const master=await n.getMainComponentAsync();
 if(!master||master.parent?.id!=='125:450')throw Error('Expected ProductButton: '+id);
 for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 // The 40px wrapper is a hit area; the 32px Control carries the fill.
 n.fills=[];mutated.push(id);
}
return {mutatedNodeIds:mutated};
'''
TABLES = r'''
for(const id of ['210:11005','210:12824','210:14133','210:17934']){
 const n=await figma.getNodeByIdAsync(id);
 if(n.type!=='FRAME'||n.children.filter(c=>/^TableRow\d/.test(c.name)).length<2)throw Error('Expected table rows');
 for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 n.setBoundVariable('itemSpacing',null);n.itemSpacing=0;mutated.push(id);
}
return {mutatedNodeIds:mutated};
'''
IDS = ['205:5716','210:8146','210:8596','210:8933','210:9928','210:10270','210:10628','210:13376','210:14529','210:14979','210:17454']
if __name__ == '__main__':
    stage = sys.argv[1]
    code = TABLES if stage == 'tables' else BUTTONS.replace('IDS', json.dumps(IDS[:8] if stage == 'buttons1' else IDS[8:]))
    print(json.dumps({'code': COMMON + code}, ensure_ascii=False))
