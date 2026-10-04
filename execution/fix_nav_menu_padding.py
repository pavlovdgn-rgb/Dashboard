"""Give menu rows token-bound inline padding and responsive nested controls."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const ids=[];
const pad=await figma.variables.importVariableByKeyAsync('735270ec262d42d1788ddb9a560e026784d69e90');
const gap=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');
for(const id of ['128:563','153:2777']){const s=await figma.getNodeByIdAsync(id);for(const t of s.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);}
const itemSet=await figma.getNodeByIdAsync('128:563');
for(const c of itemSet.children){const ctl=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');ctl.setBoundVariable('minWidth',null);ctl.minWidth=null;ctl.layoutSizingHorizontal='FILL';ids.push(ctl.id);}
const nav=await figma.getNodeByIdAsync('153:2777');
for(const c of nav.children)for(const row of c.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Nav '))){
 row.setBoundVariable('paddingLeft',pad);row.setBoundVariable('paddingRight',pad);row.setBoundVariable('itemSpacing',gap);
 const item=row.findOne(n=>n.type==='INSTANCE'&&n.name==='NavigationItem');item.resize(236,48);item.layoutSizingHorizontal='FILL';ids.push(row.id,item.id);
}
return {mutatedNodeIds:ids,variants:nav.children.length,rule:'12px left and right; 8px icon gap; nested control fills remaining width'};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
