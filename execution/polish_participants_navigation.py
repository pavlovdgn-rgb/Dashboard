"""Fix composition geometry and inherited source fills without detaching instances."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const ids=[];const sets=['128:563','153:2777','153:1605','152:996'];
for(const id of sets){const n=await figma.getNodeByIdAsync(id);for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const navItem=await figma.getNodeByIdAsync('128:563');
for(const c of navItem.children){const ctl=c.findOne(n=>n.name==='Control');for(const n of ctl.findAll(x=>x.type==='FRAME'||x.type==='INSTANCE')){n.fills=[];ids.push(n.id);}}
const nav=await figma.getNodeByIdAsync('153:2777');const gap=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');const inlinePad=await figma.variables.importVariableByKeyAsync('735270ec262d42d1788ddb9a560e026784d69e90');
for(const c of navItem.children){const ctl=c.findOne(n=>n.name==='Control');ctl.setBoundVariable('minWidth',null);ctl.minWidth=null;ctl.layoutSizingHorizontal='FILL';ids.push(ctl.id);}
for(const c of nav.children){for(const row of c.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Nav '))){for(const k of ['paddingLeft','paddingRight'])row.setBoundVariable(k,inlinePad);for(const k of ['paddingTop','paddingBottom']){row.setBoundVariable(k,null);row[k]=0;}row.setBoundVariable('itemSpacing',gap);const item=row.findOne(n=>n.type==='INSTANCE'&&n.name==='NavigationItem');item.resize(236,48);item.layoutSizingHorizontal='FILL';ids.push(row.id,item.id);}
const t=c.findOne(n=>n.name==='StudyStatus');t.componentPropertyReferences={};t.characters=c.variantProperties.Active==='Projects'?'Рабочее пространство команды':c.variantProperties.Active==='Studies'?'Все исследования проекта':'● Готово к тестированию';ids.push(t.id);}
const hint=await figma.getNodeByIdAsync('152:980');hint.visible=false;ids.push(hint.id);
const table=await figma.getNodeByIdAsync('153:1605');
for(const t of table.findAllWithCriteria({types:['TEXT']}).filter(n=>n.name==='Column3')){t.characters='ВРЕМЯ';ids.push(t.id);}
const f=table.findOne(n=>n.name==='Footer');const range=f.findOne(n=>n.name==='Range');range.resize(208,range.height);ids.push(range.id);
for(const b of f.children.filter(n=>n.type==='INSTANCE')){b.resize(180,40);ids.push(b.id);}
return {mutatedNodeIds:ids};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
