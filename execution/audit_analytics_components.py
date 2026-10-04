"""Inspect all five analytical component matrices and their display geometry."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));figma.skipInvisibleInstanceChildren=false;
const names=['SuccessMetric','FirstClickTargetRow','FirstClickTargets','ScenarioRow','ScenarioTable'];const report=[];
function shown(n,root){for(let p=n;p&&p!==root.parent;p=p.parent)if('visible'in p&&!p.visible)return false;return true;}
for(const name of names){const set=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name===name);if(!set){report.push({name,missing:true});continue;}
 const issues=[];for(const n of [set,...set.findAll()]){
  for(const f of ['fills','strokes'])if(f in n&&Array.isArray(n[f]))for(const p of n[f])if(p.type==='SOLID'&&!p.boundVariables?.color)issues.push({id:n.id,name:n.name,issue:'unbound '+f});
  if(n.type==='TEXT'&&(!n.textStyleId||typeof n.textStyleId!=='string'))issues.push({id:n.id,name:n.name,issue:'text style missing'});
  for(const f of ['paddingLeft','paddingRight','paddingTop','paddingBottom','itemSpacing','topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])if(f in n&&typeof n[f]==='number'&&n[f]>0&&!n.boundVariables?.[f]&&(!(f.startsWith('padding')||f==='itemSpacing')||('layoutMode'in n&&n.layoutMode!=='NONE')))issues.push({id:n.id,name:n.name,issue:'unbound '+f});
  if(shown(n,set)&&n!==set&&n.type!=='VECTOR'&&n.type!=='BOOLEAN_OPERATION'&&n.type!=='ELLIPSE'&&n.parent&&'width'in n.parent&&n.layoutPositioning!=='ABSOLUTE'){
   const p=n.parent;if(n.x<-.5||n.y<-.5||n.x+n.width>p.width+1||n.y+n.height>p.height+1)issues.push({id:n.id,name:n.name,issue:'overflow',size:[n.x,n.y,n.width,n.height],parent:[p.name,p.width,p.height]});
  }
 }
 report.push({name,id:set.id,properties:set.componentPropertyDefinitions,variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height})),documentation:{id:set.parent.id,x:set.parent.x,y:set.parent.y,width:set.parent.width,height:set.parent.height},issues});
}
const table=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='ScenarioTable');const ready=table.children.find(n=>n.variantProperties.State==='Ready');
const ratios=ready.findAll(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric').map(n=>({id:n.id,fraction:n.findOne(t=>t.name==='Fraction').characters,percent:n.findOne(t=>t.name==='Percent').characters,fillWidth:n.findOne(t=>t.name==='RatioFill').width,trackWidth:n.findOne(t=>t.name==='SuccessTrack').width}));
const progress=figma.currentPage.findOne(n=>n.type==='COMPONENT_SET'&&n.name==='SuccessMetric');
const metricStates=progress.children.map(c=>({name:c.name,trackVisible:c.findOne(n=>n.name==='SuccessTrack').visible,fillVisible:c.findOne(n=>n.name==='RatioFill').visible}));
const ratioIssues=ratios.filter(r=>{const [n,d]=r.fraction.split('/').map(Number);return Math.abs(r.fillWidth/r.trackWidth-n/d)>.001||r.percent!==Math.round(n/d*100)+'%';});
return {report,ratios,ratioIssues,metricStates,passed:report.every(r=>!r.missing&&r.issues.length===0)&&ratioIssues.length===0};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
