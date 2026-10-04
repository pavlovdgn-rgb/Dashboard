"""Use instance variable modes for sample ratios instead of unsupported geometry overrides."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const table=await figma.getNodeByIdAsync('136:477');for(const t of table.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const col=await figma.variables.getVariableCollectionByIdAsync('VariableCollectionId:139:593');col.renameMode(col.modes[0].modeId,'14 of 18');
const variable=await figma.variables.getVariableByIdAsync('VariableID:139:594');variable.name='success-width';variable.setVariableCodeSyntax('WEB','var(--demo-success-width)');
const modes=[];for(const [name,value]of [['14 of 18',200*14/18],['12 of 17',200*12/17],['10 of 15',200*10/15]]){let mode=col.modes.find(m=>m.name===name)?.modeId;if(!mode)mode=col.addMode(name);variable.setValueForMode(mode,value);modes.push({modeId:mode,name,value});}
const metrics=table.findAll(n=>n.type==='INSTANCE'&&/^Scenario [123]$/.test(n.name));for(let i=0;i<metrics.length;i++)metrics[i].setExplicitVariableModeForCollection(col.id,modes[i].modeId);
return {mutatedNodeIds:metrics.map(n=>n.id),collectionId:col.id,variableId:variable.id,modes};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
