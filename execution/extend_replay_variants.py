"""Generate the approved four-cell ReplayControls matrix, preserving existing IDs."""
import json
from pathlib import Path
from grow_ui_kit import COMMON, BUILD_COMMON

ROOT = Path(__file__).resolve().parents[1]
THEME = BUILD_COMMON[BUILD_COMMON.index('async function theme'):BUILD_COMMON.index('const buttonSet=')]
CODE = COMMON + THEME + r'''
await figma.setCurrentPageAsync(page);
const set=await figma.getNodeByIdAsync('84:713');
if(set.type!=='COMPONENT_SET')throw Error('ReplayControls set missing');
const pause=await figma.importComponentByKeyAsync('0f9760af5435093c90505e29a081461e27a5ae69');
await fonts(set);await fonts(pause);
const originalIds=['84:642','84:678'];
const mutations=[set.id];
for(const id of originalIds){
 const base=await figma.getNodeByIdAsync(id);
 if(base.parent.id!==set.id)throw Error('Original variant moved');
 const coverage=id==='84:642'?'Complete':'Gap';
 base.name=`Coverage=${coverage}, Playback=Paused`;mutations.push(base.id);
 let playing=set.children.find(c=>c.name===`Coverage=${coverage}, Playback=Playing`);
 if(!playing){playing=base.clone();set.appendChild(playing);created.push(playing.id);}
 playing.name=`Coverage=${coverage}, Playback=Playing`;
 await fonts(playing);
 const btn=playing.findOne(n=>n.type==='INSTANCE'&&n.name==='play');
 if(!btn)throw Error('Play control missing');
 btn.setProperties({'Text#30956:4':'Пауза','Icon left#30956:3':true,'⮑  Icon left#30964:4':pause.id});
 await theme(btn,'text/inverse','action/primary');
 const baseButton=base.findOne(n=>n.type==='INSTANCE'&&n.name==='play');
 btn.setBoundVariable('minWidth',null);btn.minWidth=baseButton.width;
 btn.primaryAxisSizingMode='FIXED';btn.resizeWithoutConstraints(baseButton.width,baseButton.height);
 playing.findOne(n=>n.name==='PositionLabel').componentPropertyReferences={characters:'PositionLabel#84:2'};
 mutations.push(playing.id,...playing.findAll().map(n=>n.id));
}
const tile=set.parent,wrap=tile.parent,section=wrap.parent;
section.resizeWithoutConstraints(section.width,wrap.height+112);
set.description='Session replay transport. Coverage: Complete or Gap; Playback: Paused or Playing. Playing displays Pause; Paused displays Play. Preserves proportional timeline, red replay/playhead, data-gap hatching and bound Elastic UI controls. Static UI states; no playback implementation.';
mutations.push(tile.id,wrap.id,section.id);
return {createdNodeIds:[...new Set(created.concat(set.children.filter(c=>!originalIds.includes(c.id)).flatMap(c=>c.findAll().map(n=>n.id))))],mutatedNodeIds:[...new Set(mutations)],id:set.id,name:set.name,properties:set.componentPropertyDefinitions,variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height,properties:c.variantProperties})),section:{id:section.id,width:section.width,height:section.height},pauseKey:pause.key};
'''

if __name__ == '__main__':
    out = ROOT / '.tmp/component-variants'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'extend-replay.js').write_text(CODE, encoding='utf-8')
    print(json.dumps({'code': CODE}, ensure_ascii=False))
