"""Restyle existing ReplayControls from the approved visual reference."""
import json
import sys
from pathlib import Path
from grow_ui_kit import COMMON, BUILD_COMMON

ROOT=Path(__file__).resolve().parents[1]
HELPERS=BUILD_COMMON[BUILD_COMMON.index('async function theme'):]
START=COMMON+HELPERS+r'''
await figma.setCurrentPageAsync(page);
const set=await figma.getNodeByIdAsync('84:713');
const mutations=[set.id,set.parent.id,set.parent.parent.id,set.parent.parent.parent.id];
const nodeIds=[];
function fixed(n,w,h){n.resize(w,h);n.primaryAxisSizingMode='FIXED';n.counterAxisSizingMode='FIXED';}
function absolute(n,parent,x,y,w,h){parent.appendChild(n);n.layoutPositioning='ABSOLUTE';n.resize(w,h);n.x=x;n.y=y;created.push(n.id);return n;}
async function labelAt(parent,name,value,x,y,w,align='LEFT'){
const t=figma.createText();await t.setTextStyleIdAsync(styles.medium.id);t.name=name;t.characters=value;fill(t,'text/primary');absolute(t,parent,x,y,w,24);t.textAlignHorizontal=align;return t;
}
function rect(parent,name,x,y,w,h,color){const n=figma.createRectangle();n.name=name;absolute(n,parent,x,y,w,h);fill(n,color);return n;}
const iconKeys={play:'5cb7c210018c156f0e0c55d85905612a8ce32045',back:'9539ad04428de87dc05b2f6cdd12806e59e7d265',forward:'aab3fa3fb3ff2fe05ebb2afe9f301b057f086502',fit:'28f003b8bdae6531af0a23cd0813d04d3a59590c',fullscreen:'790c72588ad68e1b160f3b391f5bb4c725be390e',info:'249f36e0388fb7334418d80d6a6f56a12b734c1b'};
'''

TIMELINE=r'''
set.parent.resize(1360,set.parent.height);
for(const c of set.children){
 await fonts(c);for(const child of [...c.children])child.remove();
 c.resize(1360,240);c.primaryAxisSizingMode='AUTO';spacing(c,'md','base');radii(c);mutations.push(c.id);
 const isGap=c.variantProperties.Coverage==='Gap';
 const ticks=frame('TimeLabels',c,'VERTICAL',1328);fixed(ticks,1328,24);
 for(const [seconds,value]of [[0,'00:00'],[48,'00:48'],[96,'01:36'],[144,'02:24'],[192,'03:12'],[272,'04:32']]){const x=seconds/272*1328;await labelAt(ticks,'Tick'+seconds,value,seconds===0?0:seconds===272?1268:x-30,0,60,seconds===0?'LEFT':seconds===272?'RIGHT':'CENTER');}
 const track=frame('TimeTrackArea',c,'VERTICAL',1328);fixed(track,1328,40);fill(track,'background/sidebar');radii(track);track.clipsContent=false;
 const played=rect(track,'PlayedInterval',0,0,138/272*1328,40,'accent/soft');radii(played);
 if(isGap){
  const gap=frame('GapRange100to125',track,'VERTICAL',25/272*1328);gap.layoutPositioning='ABSOLUTE';fixed(gap,25/272*1328,40);gap.x=100/272*1328;gap.y=0;gap.clipsContent=true;fill(gap,'border/subtle');
  for(let x=-40;x<gap.width+40;x+=10){const v=figma.createVector();gap.appendChild(v);created.push(v.id);v.name='GapHatching';v.layoutPositioning='ABSOLUTE';v.vectorPaths=[{windingRule:'NONE',data:`M ${x} 40 L ${x+40} 0`}];v.fills=[];v.strokes=[paint('border/control')];v.opacity=.28;}
 }
 for(const seconds of [48,96,126,144]){const dot=figma.createEllipse();dot.name='EventAt'+seconds;absolute(dot,track,seconds/272*1328-8,12,16,16);fill(dot,'background/surface');dot.strokes=[paint('accent/strong')];dot.strokeWeight=2;}
 const needle=rect(track,'PlayheadAt138',138/272*1328-1,0,2,40,'replay/playhead');
 const head=figma.createEllipse();head.name='PlayheadHandle';absolute(head,track,138/272*1328-8,-8,16,16);fill(head,'replay/playhead');head.strokes=[paint('background/surface')];head.strokeWeight=2;
 const note=frame('CoverageLegend',c,'HORIZONTAL',1328);spacing(note,'sm');
 const swatch=frame('LegendSwatch',note,'VERTICAL',16);fixed(swatch,16,16);fill(swatch,isGap?'border/subtle':'accent/soft');radii(swatch);
 await text(note,'CoverageNote',isGap?'Нет данных с 01:40 до 02:05 · разрыв записи сессии':'Запись доступна на всём интервале','body','text/secondary');
 const divider=frame('Divider',c,'HORIZONTAL',1328);fixed(divider,1328,1);fill(divider,'border/subtle');
}
set.resize(1360,set.height);set.primaryAxisSizingMode='AUTO';set.counterAxisSizingMode='AUTO';
return {createdNodeIds:created,mutatedNodeIds:mutations,variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height}))};
'''

CONTROLS=r'''
const icons={};for(const [name,key]of Object.entries(iconKeys))icons[name]=await figma.importComponentByKeyAsync(key);
async function action(parent,label,iconName,primary=false){const n=await button(parent,label,primary);if(iconName){await fonts(n);n.setProperties({'Icon left#30956:3':true,'⮑  Icon left#30964:4':icons[iconName].id});await theme(n,primary?'text/inverse':'text/primary',primary?'accent/strong':'background/surface');}n.name=iconName||label;return n;}
for(const c of set.children){
await fonts(c);for(const child of [...c.children])if(['PlaybackActions','PrivacyNote'].includes(child.name))child.remove();
const controls=frame('PlaybackActions',c,'HORIZONTAL',1328);spacing(controls,'lg');
const left=frame('Transport',controls,'HORIZONTAL',642);spacing(left,'md');left.counterAxisAlignItems='CENTER';
const playing=c.variantProperties.Playback==='Playing';
if(playing)icons.pause=await figma.importComponentByKeyAsync('0f9760af5435093c90505e29a081461e27a5ae69');
const transportButton=await action(left,'Воспроизвести','play',true);
if(playing){const originalWidth=transportButton.width;transportButton.setProperties({'Text#30956:4':'Пауза','⮑  Icon left#30964:4':icons.pause.id});await theme(transportButton,'text/inverse','accent/strong');transportButton.setBoundVariable('minWidth',null);transportButton.minWidth=originalWidth;transportButton.primaryAxisSizingMode='FIXED';transportButton.resizeWithoutConstraints(originalWidth,32);}
await action(left,'−5 с','back');await action(left,'+5 с','forward');
const pos=await text(left,'PositionLabel','02:18 / 04:32','medium');pos.componentPropertyReferences={characters:Object.keys(set.componentPropertyDefinitions).find(k=>k.startsWith('PositionLabel#'))};
const right=frame('DisplayControls',controls,'HORIZONTAL',662);spacing(right,'md');right.primaryAxisAlignItems='MAX';right.counterAxisAlignItems='CENTER';
const speed=frame('SpeedControl',right,'HORIZONTAL',270,'xs');spacing(speed,'xs','xs');radii(speed);fill(speed,'background/subtle');speed.counterAxisAlignItems='CENTER';
const speedLabel=await text(speed,'SpeedLabel','Скорость:','small','text/secondary');speedLabel.layoutSizingHorizontal='FIXED';speedLabel.resize(80,24);
for(const s of ['1×','1.5×','2×']){const b=await button(speed,s);b.setBoundVariable('minWidth',dimensions.xl);b.resizeWithoutConstraints(48,32);b.primaryAxisSizingMode='FIXED';b.name='Speed'+s;if(s==='1×'){fill(b,'accent/soft');for(const t of b.findAllWithCriteria({types:['TEXT']}))fill(t,'accent/strong');}}
await action(right,'Вписать','fit');const full=await action(right,'На весь экран','fullscreen');
const privacy=frame('PrivacyNote',c,'HORIZONTAL',1328);spacing(privacy,'sm');
const info=icons.info.createInstance();privacy.appendChild(info);created.push(info.id);info.resize(16,16);await theme(info,'text/secondary');
await text(privacy,'PrivacyText','Содержимое полей — демонстрационные данные. Камера и голос не записываются.','small','text/secondary');
mutations.push(c.id);
}
const tile=set.parent,wrap=tile.parent,section=wrap.parent;
tile.resize(1360,tile.height);wrap.resize(1436,wrap.height);section.resizeWithoutConstraints(1500,wrap.height+112);
set.description='Replay controls restyled from user reference: proportional time labels, event rings, red playhead, hatched data gap, ±5 second transport, speed presets, fit and full-screen. Uses Elastic UI instances and bound product variables. Both coverage variants preserved. Static design specification, not an implemented player.';
return {createdNodeIds:[...new Set([...created,...set.findAll().map(n=>n.id)])],mutatedNodeIds:mutations,variants:set.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height}))};
'''

def main():
    stage=sys.argv[1]
    payload=START+{'timeline':TIMELINE,'controls':CONTROLS}[stage]
    out=ROOT/'.tmp/replay-reference';out.mkdir(parents=True,exist_ok=True)
    (out/(stage+'.js')).write_text(payload,encoding='utf-8')
    print(json.dumps({'code':payload},ensure_ascii=False))

if __name__=='__main__':main()
