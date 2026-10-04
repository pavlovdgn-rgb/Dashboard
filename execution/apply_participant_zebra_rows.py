"""Apply alternating existing DS surface tokens to participant-table row instances."""
import json
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const table=await figma.getNodeByIdAsync('153:1605');
const vars=Object.fromEntries((await figma.variables.getLocalVariablesAsync('COLOR')).map(v=>[v.name,v]));
const ids=[],rows=[];
for(const variant of table.children)for(const body of variant.findAll(n=>n.name==='ParticipantRows')){
for(let i=0;i<body.children.length;i++){
 const row=body.children[i];const name=i%2?'background/canvas':'background/surface';const v=vars[name];
 if(!v)throw Error('Missing token '+name);const value=Object.values(v.valuesByMode)[0];
 row.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:value.r,g:value.g,b:value.b}},'color',v)];
 ids.push(row.id);rows.push({id:row.id,index:i+1,token:name});
}}
return {mutatedNodeIds:ids,rows};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
