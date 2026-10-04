"""Emit small Figma repair batches using existing components, without recreating artwork."""
import argparse
import json

FONTS = r'''
async function fonts(n){const texts=n.type==='TEXT'?[n]:('findAllWithCriteria'in n?n.findAllWithCriteria({types:['TEXT']}):[]);for(const t of texts)for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const created=[],changed=[],removed=[];
'''

MASTERS = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
''' + FONTS + r'''
const set=await figma.getNodeByIdAsync('153:2777'),logo=await figma.getNodeByIdAsync('289:13519');
const sample=await figma.getNodeByIdAsync('289:13484');
const vector=logo.findOne(n=>n.type==='VECTOR');
const inverse=await figma.variables.getVariableByIdAsync('VariableID:67:115');
vector.fills=vector.fills.map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',inverse):p);changed.push(vector.id);
for(const variant of set.children){await fonts(variant);const old=variant.findOne(n=>n.name==='ProductMark');if(old.findOne(n=>n.type==='INSTANCE'&&n.mainComponent?.id===logo.id))continue;
 const parent=old.parent,index=parent.children.indexOf(old);const mark=sample.clone();parent.insertChild(index,mark);mark.name='ProductMark';created.push(mark.id,...mark.findAll().map(n=>n.id));removed.push(old.id);old.remove();changed.push(parent.id,variant.id);
}
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,variants:set.children.map(n=>({id:n.id,logos:n.findAll(n=>n.type==='INSTANCE'&&n.mainComponent?.id===logo.id).length}))};
'''

SCREENS = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
''' + FONTS + r'''
const targets=[['210:13333',false],['210:18724',true]];
for(const [id,findings] of targets){const group=await figma.getNodeByIdAsync(id);await fonts(group);
 for(const old of [...group.children]){if(old.type!=='INSTANCE')continue;const selected=old.name.startsWith('Находки')?findings:!findings;const master=await figma.getNodeByIdAsync(selected?'128:992':'128:981');await fonts(master);
 if(old.mainComponent?.id===master.id)continue;
 const tab=master.createInstance();group.insertChild(group.children.indexOf(old),tab);tab.name=old.name;await fonts(tab);tab.findOne(n=>n.type==='TEXT'&&n.name==='Tab').characters=old.name;tab.resize(180,40);tab.layoutSizingHorizontal='FIXED';created.push(tab.id,...tab.findAll().map(n=>n.id));removed.push(old.id);old.remove();
 }group.name='SignalsFindingsTabs';changed.push(group.id);
}
const metrics=['210:7672','210:7689','210:7706','210:12773','210:12790','210:12807','210:14082','210:14099','210:14116'];
for(const id of metrics){const n=await figma.getNodeByIdAsync(id);await fonts(n);const t=n.findOne(c=>c.type==='TEXT'&&c.name==='Detail');if(t&&t.characters===''){t.visible=false;changed.push(t.id,n.id);}}
const overlay=await figma.getNodeByIdAsync('210:15000');const before={w:overlay.width,h:overlay.height};overlay.resize(overlay.width,overlay.parent.height-overlay.y);changed.push(overlay.id);
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,groups:targets.map(x=>x[0]),overlay:{id:overlay.id,before,after:{w:overlay.width,h:overlay.height}}};
'''

LEGACY = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('PAGE_ID'));
''' + FONTS + r'''
const source=await figma.getNodeByIdAsync('153:1610');await fonts(source);
const sidebars=figma.currentPage.findAll(n=>n.type==='FRAME'&&n.name==='Sidebar');
const result=[];
for(const sidebar of sidebars){await fonts(sidebar);let brand=sidebar.children.find(n=>n.name==='Brand');if(!brand){brand=source.clone();sidebar.insertChild(0,brand);brand.resize(sidebar.width-sidebar.paddingLeft-sidebar.paddingRight,32);brand.layoutSizingHorizontal='FILL';brand.layoutSizingVertical='FIXED';created.push(brand.id,...brand.findAll().map(n=>n.id));changed.push(sidebar.id);}
 const title=brand.findOne(n=>n.type==='TEXT'&&n.name==='ProductName');if(title){await fonts(title);title.layoutSizingHorizontal='FILL';changed.push(title.id);}
 result.push({id:sidebar.id,brand:brand.id,overflow:Math.max(0,...sidebar.children.filter(n=>n.visible).map(n=>n.y+n.height+sidebar.paddingBottom-sidebar.height))});
}
return {page:'PAGE_ID',createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,sidebars:result};
'''

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['masters','screens','legacy']);parser.add_argument('--page');args=parser.parse_args()
    code={'masters':MASTERS,'screens':SCREENS,'legacy':LEGACY}[args.stage]
    if args.stage=='legacy':
        if args.page not in ['20:2','67:2']:raise SystemExit('Unsupported legacy page')
        code=code.replace('PAGE_ID',args.page)
    print(json.dumps({'code':code},ensure_ascii=False))
