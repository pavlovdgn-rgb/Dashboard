"""Bind large UI surfaces to a shared semantic radius, preserving compact controls."""
import json
from pathlib import Path
from build_final_results import BASE
ROOT=Path(__file__).resolve().parents[1]
CODE=BASE+r'''
await figma.setCurrentPageAsync(page);
const collections=await figma.variables.getLocalVariableCollectionsAsync();
const primitives=collections.find(c=>c.name==='UX-Lab · Primitives');
const semantics=await figma.variables.getVariableCollectionByIdAsync(colors['background/surface'].variableCollectionId);
const floats=await figma.variables.getLocalVariablesAsync('FLOAT');
let primitive=floats.find(v=>v.name==='radius/12');
if(!primitive){primitive=figma.variables.createVariable('radius/12',primitives,'FLOAT');primitive.scopes=[];primitive.setValueForMode(primitives.defaultModeId,12);}
let radius=floats.find(v=>v.name==='radius/surface');
if(!radius){radius=figma.variables.createVariable('radius/surface',semantics,'FLOAT');radius.scopes=['CORNER_RADIUS'];radius.setValueForMode(semantics.defaultModeId,{type:'VARIABLE_ALIAS',id:primitive.id});radius.setVariableCodeSyntax('WEB','var(--radius-surface)');}
const names=['SummaryMetric','ScenarioTable','ParticipantsTable','FirstClickTargets','DataCoverage','ReplayControls','HeatmapLegend'];
const sets=page.findAll(n=>n.type==='COMPONENT_SET'&&names.includes(n.name));
for(const set of sets){await fonts(set);for(const c of set.children){for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])c.setBoundVariable(k,radius);mutated.push(c.id);}}
return {radiusId:radius.id,primitiveId:primitive.id,value:12,sets:sets.map(n=>({id:n.id,name:n.name})),mutatedNodeIds:mutated,createdVariableIds:[radius.id,primitive.id]};
'''
if __name__=='__main__':
    (ROOT/'.tmp/final-results/surface-radius.js').write_text(CODE,encoding='utf-8')
    print(json.dumps({'code':CODE},ensure_ascii=False))
