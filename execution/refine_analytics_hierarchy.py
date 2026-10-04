"""Apply semantic action hierarchy and separate success metric values in Figma."""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
figma.skipInvisibleInstanceChildren=false;
const changed=[],created=[],removed=[];
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
function paint(v){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',v);}
const primary=await figma.getNodeByIdAsync('125:312'),tertiary=await figma.getNodeByIdAsync('125:326');
const fg=await figma.variables.getVariableByIdAsync('VariableID:67:118');
const muted=await figma.variables.getVariableByIdAsync('VariableID:67:114');
async function kind(n,master){await fonts(n);await fonts(master);if((await n.getMainComponentAsync()).id!==master.id)n.swapComponent(master);changed.push(n.id,...n.findAll().map(x=>x.id));}
const retry=await figma.getNodeByIdAsync('210:15759');await kind(retry,primary);
const groups=figma.currentPage.findAll(n=>n.type==='FRAME'&&n.name==='Actions'&&n.children.some(c=>c.name==='Находки · 2'));
const screens=[];
for(const group of groups){let screen=group;while(screen.parent&&!screen.name.startsWith('Screen/'))screen=screen.parent;screens.push(screen);
 const findings=/Screen\/Finding/.test(screen.name);
 for(const old of [...group.children]){
  const selected=old.name.startsWith('Находки')?findings:!findings;
  const master=await figma.getNodeByIdAsync(selected?'128:992':'128:981');await fonts(master);
  const tab=master.createInstance();group.insertChild(group.children.indexOf(old),tab);tab.name=old.name;await fonts(tab);
  const label=tab.findOne(n=>n.type==='TEXT'&&n.name==='Tab');label.characters=old.name;
  tab.resize(180,40);tab.layoutSizingHorizontal='FIXED';
  removed.push(old.id);old.remove();created.push(tab.id,...tab.findAll().map(n=>n.id));
 }
 group.name='SignalsFindingsTabs';changed.push(group.id);
 for(const n of screen.findAll(n=>n.type==='INSTANCE'&&n.name==='Сбросить фильтры')){await kind(n,tertiary);const txt=n.findOne(x=>x.type==='TEXT'&&x.visible);txt.fills=[paint(fg)];}
 for(const n of screen.findAll(n=>n.type==='INSTANCE'&&n.name==='Включить находки в PDF'))await kind(n,primary);
 for(const n of screen.findAll(n=>n.type==='INSTANCE'&&n.name==='Открыть сигналы')){removed.push(n.id);n.remove();}
 for(const n of screen.findAll(n=>n.type==='INSTANCE'&&n.name==='К сводке страниц')){await kind(n,tertiary);const txt=n.findOne(x=>x.type==='TEXT'&&x.visible);txt.characters='← К сводке страниц';txt.fills=[paint(fg)];}
}
for(const n of figma.currentPage.findAll(n=>n.type==='INSTANCE'&&n.name==='Сбросить фильтры')){await kind(n,tertiary);const txt=n.findOne(x=>x.type==='TEXT');if(txt)txt.fills=[paint(fg)];}
const metric=await figma.getNodeByIdAsync('210:7689');await fonts(metric);
const props=metric.componentProperties;const key=p=>Object.keys(props).find(k=>k.startsWith(p+'#'));
metric.setProperties({[key('Value')]:'10 из 15',[key('Badge')]:'67%',[key('ShowBadge')]:true});
const value=metric.findOne(n=>n.type==='TEXT'&&n.name==='Value');
const label=metric.findOne(n=>n.type==='TEXT'&&n.name==='Label');
await value.setRangeTextStyleIdAsync(3,value.characters.length,label.textStyleId);
value.setRangeFills(3,value.characters.length,[paint(muted)]);
changed.push(metric.id,...metric.findAll().map(n=>n.id));
return {mutatedNodeIds:[...new Set(changed)],createdNodeIds:created,removedNodeIds:removed,screenIds:screens.map(s=>s.id),metricId:metric.id,retryId:retry.id};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
