"""Restyle product secondary controls with existing warm neutral tokens."""
import json
from remove_incomplete_badge_fill import CODE as BADGES

CODE = BADGES[:BADGES.index('return {mutatedNodeIds:')] + r'''
const buttons=await figma.getNodeByIdAsync('125:450');
const tokens=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.name,v]));
const byId=Object.fromEntries(Object.values(tokens).map(v=>[v.id,v]));
function resolve(v){const x=Object.values(v.valuesByMode)[0];return x.type==='VARIABLE_ALIAS'?resolve(byId[x.id]):x;}
function paint(name){const v=tokens[name],x=resolve(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
for(const c of buttons.children){
 const {Kind,State}=c.variantProperties;
 if(!['Secondary','Tertiary'].includes(Kind))continue;
 for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const ctl=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');
 if(Kind==='Secondary')ctl.fills=[paint(State==='Hover'?'action/secondary/hover':State==='Pressed'?'action/secondary/pressed':'action/secondary/background')];
 else if(!['Hover','Pressed'].includes(State))ctl.fills=[];
 ctl.strokes=[];ids.push(ctl.id);
}
return {mutatedNodeIds:ids,badgeRule:'Background only for Selected=False',secondary:'Warm gray; darker hover; olive pressed; focus ring retained'};
'''
if __name__=='__main__':
    print(json.dumps({'code': CODE}))
