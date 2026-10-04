"""Replace text crosses with the existing library icon-only Button variant."""
import json

CODE = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const created=[],mutated=[],removed=[];
const cross=await figma.importComponentByKeyAsync('ccaa0c0dfc78be0e85701649b3d8b6393f842c36');
const textToken=await figma.variables.getVariableByIdAsync('VariableID:67:113');
const vars=await figma.variables.getLocalVariablesAsync('COLOR');
const bg=vars.find(v=>v.name==='action/secondary/background');
const paint=v=>figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',v);
for(const id of ['207:6616','210:9628','210:14969']){
 let button=await figma.getNodeByIdAsync(id);
 if(!button&&id==='210:14969'){
  const header=await figma.getNodeByIdAsync('210:14967');
  button=header.children.find(n=>n.type==='INSTANCE'&&n.name==='Закрыть');
 }
 if(!button)throw Error('Missing close target '+id);
 if(button.type==='TEXT'){
  const old=button,parent=old.parent,index=parent.children.indexOf(old);
  const master=await figma.getNodeByIdAsync('125:319');button=master.createInstance();parent.insertChild(index,button);created.push(button.id);removed.push(old.id);old.remove();
 }
 for(const t of button.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 button.name='Закрыть';button.resize(40,40);button.layoutSizingHorizontal='FIXED';button.layoutSizingVertical='FIXED';mutated.push(button.id);
 const control=button.children.find(c=>c.type==='INSTANCE'&&c.name==='Control');
 control.setProperties({'Icon only':'True','⮑  Icon#31150:0':cross.id});
 control.resize(32,32);control.layoutSizingHorizontal='FILL';control.fills=[paint(bg)];control.strokes=[];mutated.push(control.id);
 for(const n of control.findAll(n=>['VECTOR','BOOLEAN_OPERATION','ELLIPSE','RECTANGLE'].includes(n.type))){
  for(const field of ['fills','strokes'])if(Array.isArray(n[field])&&n[field].length)n[field]=n[field].map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',textToken):p);
  mutated.push(n.id);
 }
}
return {createdNodeIds:created,mutatedNodeIds:mutated,removedNodeIds:removed,iconComponentId:cross.id};
'''
if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
