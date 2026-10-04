"""Place the funnel heading and denominator note outside the table surface."""
import json
CODE=r"""
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const panel=await figma.getNodeByIdAsync('210:7727'),table=await figma.getNodeByIdAsync('210:7729');
for(const t of panel.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const vars=await figma.variables.getLocalVariablesAsync();
const paint=name=>figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:1,g:1,b:1}},'color',vars.find(v=>v.name===name));
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
const shadow=(await figma.getLocalEffectStylesAsync()).find(s=>s.name==='shadow/card');
panel.fills=[];panel.strokes=[];await panel.setEffectStyleIdAsync('');panel.effects=[];
for(const k of ['paddingLeft','paddingTop','paddingRight','paddingBottom']){panel.setBoundVariable(k,null);panel[k]=0;}
for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])panel.setBoundVariable(k,null);
panel.cornerRadius=0;panel.clipsContent=false;
table.layoutSizingHorizontal='FILL';table.fills=[paint('background/surface')];table.strokes=[paint('border/subtle')];table.strokeWeight=1;table.strokeAlign='INSIDE';table.setBoundVariable('cornerRadius',radius);table.clipsContent=true;await table.setEffectStyleIdAsync(shadow.id);
return {mutatedNodeIds:[panel.id,table.id],panel:{fills:panel.fills,strokes:panel.strokes,effects:panel.effects},children:panel.children.map(n=>({id:n.id,name:n.name,w:n.width,h:n.height}))};
"""
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
