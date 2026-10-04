"""Restore the warm data-visualization palette requested from wireframe 22:101."""
import json
import sys
from pathlib import Path
from build_final_results import BASE
ROOT=Path(__file__).resolve().parents[1]
TOKENS=r'''
await figma.setCurrentPageAsync(page);
const cols=await figma.variables.getLocalVariableCollectionsAsync();const primitives=cols.find(c=>c.name==='UX-Lab · Primitives');const collection=cols.find(c=>c.name==='UX-Lab · Heatmap');
const existing=await figma.variables.getLocalVariablesAsync('COLOR');const updated=[];
function color(hex,a=1){return {r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255,a};}
function token(name,value){let p=existing.find(v=>v.name==='thermal/'+name);if(!p){p=figma.variables.createVariable('thermal/'+name,primitives,'COLOR');p.scopes=[];}p.setValueForMode(primitives.defaultModeId,value);let semantic=existing.find(v=>v.name==='heatmap/'+name);if(!semantic){semantic=figma.variables.createVariable('heatmap/'+name,collection,'COLOR');semantic.scopes=['FRAME_FILL','SHAPE_FILL'];}semantic.setValueForMode(collection.defaultModeId,{type:'VARIABLE_ALIAS',id:p.id});updated.push({id:semantic.id,name:semantic.name,primitiveId:p.id,value});return semantic;}
const hexes=['#FFF8DF','#FFF0B8','#FFE788','#FFDB36','#FFC630','#FFAC29','#FF8C22','#F77323','#ED5525','#E33C26'];
for(let i=0;i<hexes.length;i++)token('intensity/'+(i+1),color(hexes[i]));
token('spot/core',color('#E33C26',.7));token('spot/middle',color('#FF8C22',.56));token('spot/outer',color('#FFDA36',.3));token('spot/edge',color('#FFDF38',0));
return {variables:updated,mutatedVariableIds:updated.flatMap(x=>[x.id,x.primitiveId])};
'''
APPLY=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const stopNames=['heatmap/spot/core','heatmap/spot/middle','heatmap/spot/outer','heatmap/spot/edge'];
const positions=[0,.36,.72,1];
const stops=stopNames.map((name,i)=>({position:positions[i],color:resolved(colors[name]),boundVariables:{color:{type:'VARIABLE_ALIAS',id:colors[name].id}}}));
const ids=[];
for(const layer of figma.currentPage.findAll(n=>n.name==='Demo click layer'))for(const [i,n]of layer.children.entries()){
 if(n.type!=='ELLIPSE')continue;n.fills=[{type:'GRADIENT_RADIAL',gradientTransform:[[1,0,0],[0,1,0]],gradientStops:stops}];n.opacity=1;const size=[120,86,100,90,76][i%5];n.resize(size,size);ids.push(n.id);
}
return {mutatedNodeIds:ids,stops:stopNames};
'''
if __name__=='__main__':
    stage=sys.argv[1];code=BASE+{'tokens':TOKENS,'apply':APPLY}[stage]
    (ROOT/'.tmp/final-pack'/f'heatmap-{stage}.js').write_text(code,encoding='utf-8')
    print(json.dumps({'code':code},ensure_ascii=False))
