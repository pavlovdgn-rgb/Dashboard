"""Fix replay form sizing and distinguish playback from recorded-page actions."""
import json
import sys

FONT = r'''
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
'''
FORM = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const n=await figma.getNodeByIdAsync('210:15323');await fonts(n);
if((await n.getMainComponentAsync())?.parent?.id!=='203:4474')throw Error('Expected ProductField');
n.layoutSizingVertical='HUG';
return {mutatedNodeIds:[n.id],height:n.height,sizing:n.layoutSizingVertical};
'''
PLAY = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const color=await figma.variables.getVariableByIdAsync('VariableID:67:118');
const ids=[];
for(const id of ['96:116','96:183','118:120','118:212']){
 const n=await figma.getNodeByIdAsync(id);await fonts(n);
 n.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:98/255,g:110/255,b:50/255}},'color',color)];ids.push(n.id);
}
return {mutatedNodeIds:ids,token:color.name,hex:'#626E32',foreground:'text/inverse'};
'''
AUDIT = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const issues=[],fields=[],players=[];
for(const n of figma.currentPage.findAllWithCriteria({types:['INSTANCE']})){
 if(n.name==='play'){const text=n.findAllWithCriteria({types:['TEXT']}).map(t=>t.characters).join('');if(/Воспроизвести|Пауза/.test(text))players.push({id:n.id,fill:n.fills[0]?.boundVariables?.color?.id});}
 if(!n.componentProperties.Type)continue;
 const m=await n.getMainComponentAsync();if(m?.parent?.id!=='203:4474')continue;
 const bottom=Math.max(...n.children.filter(c=>c.visible).map(c=>c.y+c.height));fields.push(n.id);
 if(bottom>n.height+.5)issues.push({id:n.id,height:n.height,bottom});
}
const form=await figma.getNodeByIdAsync('210:15321');const name=form.children.find(n=>n.name==='Field/Имя'),email=form.children.find(n=>n.name==='Field/Email');
return {fieldCount:fields.length,issues,players,gap:email.y-name.y-name.height,passed:!issues.length&&players.length===4&&players.every(p=>p.fill==='VariableID:67:118')};
'''
if __name__=='__main__':
    print(json.dumps({'code':FONT+{'form':FORM,'play':PLAY,'audit':AUDIT}[sys.argv[1]]}))
