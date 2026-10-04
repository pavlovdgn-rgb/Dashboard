"""Refine numerical demo bindings, selected radio colours and target-list action."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const colors=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.name,v]));
function paint(key){const v=colors[key],x=Object.values(v.valuesByMode)[0];return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
const changed=[],created=[],variables=[];
let col=(await figma.variables.getLocalVariableCollectionsAsync()).find(c=>c.name==='UX-Lab · Demo data');if(!col){col=figma.variables.createVariableCollection('UX-Lab · Demo data');col.renameMode(col.modes[0].modeId,'Example');created.push(col.id);}
const data={};for(const [name,value]of Object.entries({'success-width/14-of-18':200*14/18,'success-width/12-of-17':200*12/17,'success-width/10-of-15':200*10/15})){let v=(await figma.variables.getLocalVariablesAsync('FLOAT')).find(v=>v.name===name&&v.variableCollectionId===col.id);if(!v){v=figma.variables.createVariable(name,col,'FLOAT');created.push(v.id);}v.scopes=['WIDTH_HEIGHT'];v.setValueForMode(col.modes[0].modeId,value);v.description='Illustrative data geometry at track width 200. Not a design-system spacing token or live metric.';data[name]=v;variables.push({id:v.id,name,value});}
const metric=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SuccessMetric');for(const c of metric.children){const f=c.findOne(n=>n.name==='RatioFill');f.setBoundVariable('width',data['success-width/14-of-18']);changed.push(f.id);}
const table=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ScenarioTable');const ready=table.children.find(c=>c.variantProperties.State==='Ready');
const metrics=ready.findAll(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric');for(let k=0;k<metrics.length;k++){const f=metrics[k].findOne(n=>n.name==='RatioFill');f.setBoundVariable('width',data[['success-width/14-of-18','success-width/12-of-17','success-width/10-of-15'][k]]);changed.push(f.id);}
const rows=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ScenarioRow');for(const c of rows.children){const r=c.findOne(n=>n.name==='ScenarioSelection');for(const n of r.findAll()){if(n.type==='FRAME'&&n.name==='Radio State'){n.fills=[];changed.push(n.id);}if(n.type==='ELLIPSE'){n.fills=[paint(n.width<10?'accent/strong':'background/surface')];if(n.width>=10){n.strokes=[paint(c.variantProperties.Selected==='True'?'accent/strong':'border/control')];n.strokeWeight=1.5;}changed.push(n.id);}}}
return {mutatedNodeIds:changed,createdNodeIds:created,demoCollection:col.id,demoVariables:variables};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
