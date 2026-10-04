"""Generate geometry repair or a read-only audit for one interaction ComponentSet."""
import json
import sys

SETUP="await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));const set=await figma.getNodeByIdAsync('__ID__');"
REPAIR="await Promise.all(set.findAllWithCriteria({types:['TEXT']}).flatMap(t=>t.getStyledTextSegments(['fontName']).map(s=>figma.loadFontAsync(s.fontName))));const radius=await figma.variables.importVariableByKeyAsync('dd2359cd4743157f5fc30993b8f29368cec946d3');for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])set.setBoundVariable(k,radius);set.counterAxisSizingMode='AUTO';set.clipsContent=false;return {mutatedNodeIds:[set.id,set.parent.id],width:set.width,height:set.height};"
AUDIT=r'''
const issues=[];const nodes=[set,...set.findAll()];
for(const n of nodes){
 for(const field of ['fills','strokes'])if(field in n&&Array.isArray(n[field]))for(const p of n[field])if(p.type==='SOLID'&&!p.boundVariables?.color)issues.push({id:n.id,issue:'unbound '+field});
 if(n.type==='TEXT'&&(!n.textStyleId||typeof n.textStyleId!=='string'))issues.push({id:n.id,issue:'text style missing'});
 for(const f of ['paddingLeft','paddingRight','paddingTop','paddingBottom','itemSpacing','topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])if(f in n&&typeof n[f]==='number'&&n[f]>0&&!n.boundVariables?.[f]&&(!(f.startsWith('padding')||f==='itemSpacing')||('layoutMode'in n&&n.layoutMode!=='NONE')))issues.push({id:n.id,issue:'unbound '+f});
}
const variants=[];
for(const c of set.children){const n=c.findOne(n=>n.name==='Control'&&n.type==='INSTANCE');variants.push({id:c.id,name:c.name,width:c.width,height:c.height,x:c.x,y:c.y,instance:n?{id:n.id,width:n.width,height:n.height,sourceKey:(await n.getMainComponentAsync()).key,exposed:n.isExposedInstance}:null});if(!n)issues.push({id:c.id,issue:'no instance'});if(c.x+c.width>set.width+1||c.y+c.height>set.height+1)issues.push({id:c.id,issue:'set overflow'});}
return {name:set.name,id:set.id,properties:set.componentPropertyDefinitions,variants,issues,passed:issues.length===0,documentation:{id:set.parent.id,y:set.parent.y,height:set.parent.height},size:{width:set.width,height:set.height}};
'''
if __name__=='__main__':print(json.dumps({'code':SETUP.replace('__ID__',sys.argv[2])+(REPAIR if sys.argv[1]=='repair' else AUDIT)}))
