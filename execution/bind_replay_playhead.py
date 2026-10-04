"""Preserve the user's red playhead with a dedicated product token."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const set=await figma.getNodeByIdAsync('84:713');
const targets=set.findAll(n=>n.name.startsWith('Playhead'));
const color=targets[0].fills.find(p=>p.type==='SOLID').color;
if(targets.length!==set.children.length*2)throw Error('Expected two playhead shapes per variant');
const col=await figma.variables.getVariableCollectionByIdAsync('VariableCollectionId:67:106');
let v=(await figma.variables.getLocalVariablesAsync('COLOR')).find(v=>v.name==='replay/playhead');
const createdVariableIds=[];
if(!v){v=figma.variables.createVariable('replay/playhead',col,'COLOR');createdVariableIds.push(v.id);}
v.scopes=['SHAPE_FILL','FRAME_FILL'];v.description='Current playback position. User-selected red; not an error status.';
for(const mode of col.modes)v.setValueForMode(mode.modeId,{...color,a:1});
for(const n of targets)n.fills=[figma.variables.setBoundVariableForPaint({type:'SOLID',color},'color',v)];
return {createdVariableIds,mutatedNodeIds:targets.map(n=>n.id),variable:{id:v.id,name:v.name,collectionId:col.id,values:v.valuesByMode},hex:'#'+[color.r,color.g,color.b].map(c=>Math.round(c*255).toString(16).padStart(2,'0')).join('').toUpperCase()};
'''

def main():
    tmp=ROOT/'.tmp/replay-reference';tmp.mkdir(parents=True,exist_ok=True)
    if len(sys.argv)>1 and sys.argv[1]=='sync':
        record=json.loads((tmp/'red-token.json').read_text(encoding='utf-8'))
        p=ROOT/'ds/product-palette.json';data=json.loads(p.read_text(encoding='utf-8'))
        data['colors']['replay/playhead']=record['hex'];data['playheadToken']=record
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for name in ['index.json','grow-ui-kit-status.json']:
            p=ROOT/'ds'/name;data=json.loads(p.read_text(encoding='utf-8'));data['replayPlayheadToken']=record
            p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        p=ROOT/'execution/restyle_replay_controls.py';text=p.read_text(encoding='utf-8')
        text=text.replace("2,40,'accent/strong'","2,40,'replay/playhead'").replace("fill(head,'accent/strong')","fill(head,'replay/playhead')").replace('olive playhead','red playhead')
        p.write_text(text,encoding='utf-8')
        for name in ['foundation.md','product-palette.md','replay-reference-update.md']:
            p=ROOT/'ds'/name;text=p.read_text(encoding='utf-8')
            marker='## Красный ползунок — 22 сентября 2026'
            if marker not in text:
                text+='\n\n'+marker+'\n\n`replay/playhead` = `'+record['hex']+'` ('+record['variable']['id']+'). Цвет пользователя сохранён; линия и кружок обоих вариантов привязаны к отдельному токену позиции воспроизведения. Цвета ошибок и маркеров событий не менялись. Эта правка заменяет прежнее описание оливкового ползунка.\n'
                p.write_text(text,encoding='utf-8')
        print(json.dumps({'synced':True,'hex':record['hex']}))
    else:
        (tmp/'bind-red.js').write_text(CODE,encoding='utf-8');print(json.dumps({'code':CODE}))

if __name__=='__main__':main()
