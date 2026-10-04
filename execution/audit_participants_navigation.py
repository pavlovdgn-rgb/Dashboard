"""Inspect current component geometry, token bindings and approved row styling."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const names=['TaskOutcome','RecordingCoverage','AttemptAction','ParticipantRow','ParticipantsTable','NavMenu'];
const report=[];
function shown(n,root){for(let p=n;p&&p!==root.parent;p=p.parent)if('visible'in p&&!p.visible)return false;return true;}
for(const name of names){const s=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name===name);const issues=[];
for(const n of s.findAll()){
for(const field of ['fills','strokes'])if(field in n&&Array.isArray(n[field]))for(const p of n[field])if(p.type==='SOLID'&&!p.boundVariables?.color)issues.push({id:n.id,name:n.name,issue:field+' unbound'});
if(n.type==='TEXT'&&!n.textStyleId)issues.push({id:n.id,issue:'Text style missing'});
if(shown(n,s)&&!['VECTOR','BOOLEAN_OPERATION','ELLIPSE'].includes(n.type)&&n.layoutPositioning!=='ABSOLUTE'&&n.parent&&'width'in n.parent&&(n.x<-.5||n.y<-.5||n.x+n.width>n.parent.width+1||n.y+n.height>n.parent.height+1))issues.push({id:n.id,name:n.name,issue:'Overflow'});
}
report.push({name,id:s.id,type:s.type,variants:s.children.map(n=>({id:n.id,name:n.name,width:n.width,height:n.height})),properties:s.componentPropertyDefinitions,issues});}
const rows=await figma.getNodeByIdAsync('135:1062');const badges=rows.children.map(c=>({id:c.id,selected:c.variantProperties.Selected,hasFill:c.findOne(n=>n.name==='IncompleteBadge').fills.length>0}));
const buttons=await figma.getNodeByIdAsync('125:450');const secondary=buttons.children.filter(c=>c.variantProperties.Kind==='Secondary').map(c=>({id:c.id,state:c.variantProperties.State,fills:c.findOne(n=>n.name==='Control').fills}));
return {report,badges,secondary,passed:report.every(r=>!r.issues.length)&&badges.every(b=>b.hasFill===(b.selected==='False'))};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
