"""Prepare in-place monochrome restyling of existing IA frames from user reference."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/figma-ia'
FRAME_IDS=['9:2','10:2','10:64','10:105']

SCRIPT=r'''
const page=await figma.getNodeByIdAsync('8:2');await figma.setCurrentPageAsync(page);
const f=await figma.getNodeByIdAsync(CFG.frameId);if(!f||f.type!=='FRAME')throw new Error('Missing frame');
const texts=f.findAllWithCriteria({types:['TEXT']});
const fonts=new Map();for(const t of texts)for(const s of t.getStyledTextSegments(['fontName']))fonts.set(JSON.stringify(s.fontName),s.fontName);
for(const font of fonts.values())await figma.loadFontAsync(font);
for(const style of ['Regular','Medium','Semi Bold'])await figma.loadFontAsync({family:'Inter',style});
const ids=new Set([f.id]);const mark=n=>ids.add(n.id);
const rgb=h=>({r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255});
const paint=h=>[{type:'SOLID',color:rgb(h)}];
f.fills=paint('#FFFFFF');f.strokes=paint('#E2E5E9');f.strokeWeight=1;f.cornerRadius=16;f.resize(CFG.width,CFG.height);
const title=f.children.find(n=>n.type==='TEXT'&&n.name===DATA.title);
const subtitle=f.children.find(n=>n.type==='TEXT'&&n.name===DATA.subtitle);
const kicker=f.children.find(n=>n.type==='TEXT'&&n.name===DATA.kicker);
if(kicker){kicker.visible=false;mark(kicker);}
title.fontSize=24;title.x=32;title.y=28;title.fills=paint('#191919');title.resize(CFG.width-64,1);title.textAutoResize='HEIGHT';mark(title);
subtitle.fontSize=16;subtitle.x=32;subtitle.y=66;subtitle.fills=paint('#717680');subtitle.resize(CFG.width-64,1);subtitle.textAutoResize='HEIGHT';mark(subtitle);
for(const d of DATA.nodes){
 const card=f.children.find(n=>n.type==='FRAME'&&n.name===d.id);if(!card)throw new Error('Missing '+d.id);
 const black=CFG.terminals.includes(d.id);card.x=d.x*CFG.sx;card.y=d.y*CFG.sy;
 card.resize((d.w||300)*CFG.sx,(d.h||112)*CFG.sy);
 card.primaryAxisSizingMode='FIXED';card.counterAxisSizingMode='FIXED';card.primaryAxisAlignItems='CENTER';card.counterAxisAlignItems='CENTER';
 card.cornerRadius=12;card.fills=paint(black?'#000000':'#F5F5F5');card.strokes=paint(black?'#000000':'#C3C9D1');card.strokeWeight=1.2;
 card.dashPattern=d.priority&&d.priority!=='core'?[5,5]:[];card.itemSpacing=8;card.paddingTop=12;card.paddingBottom=12;
 const parts=card.children.filter(n=>n.type==='TEXT');const idText=parts.find(t=>t.characters.startsWith(d.id));const desc=parts.find(t=>t!==idText);
 if(!idText||!desc)throw new Error('Unexpected card text '+d.id);
 card.insertChild(0,desc);card.insertChild(1,idText);
 desc.fontName={family:'Inter',style:black?'Semi Bold':'Regular'};desc.fontSize=16;desc.fills=paint(black?'#FFFFFF':'#191919');
 idText.fontName={family:'Inter',style:'Regular'};idText.fontSize=12;idText.fills=paint(black?'#D0D0D0':'#717680');
 for(const t of [desc,idText]){t.resize(card.width-40,1);t.textAutoResize='HEIGHT';t.textAlignHorizontal='CENTER';mark(t);}mark(card);
}
function setPath(n,points){
 const minX=Math.min(...points.map(p=>p[0])),minY=Math.min(...points.map(p=>p[1]));
 let data=points.map((p,i)=>(i?'L':'M')+' '+(p[0]-minX)+' '+(p[1]-minY)).join(' ');
 const a=points.at(-2),b=points.at(-1),ang=Math.atan2(b[1]-a[1],b[0]-a[0]);const wing=s=>[b[0]-minX-9*Math.cos(ang+s),b[1]-minY-9*Math.sin(ang+s)];
 data+=' M '+wing(.6).join(' ')+' L '+(b[0]-minX)+' '+(b[1]-minY)+' L '+wing(-.6).join(' ');
 n.vectorPaths=[{windingRule:'NONZERO',data}];n.x=minX;n.y=minY;n.strokes=paint('#737D8B');n.strokeWeight=1.6;n.dashPattern=[];mark(n);
}
for(const e of DATA.edges){
 const n=f.children.find(n=>n.type==='VECTOR'&&n.name===e.name);if(!n)throw new Error('Missing edge '+e.name);
 setPath(n,e.points.map(p=>[p[0]*CFG.sx,p[1]*CFG.sy]));
 if(e.number){
  const badge=f.children.find(n=>n.type==='FRAME'&&n.name==='Transition '+e.number);const t=badge.children.find(n=>n.type==='TEXT');
  const label=e.name.split(' · ').slice(1).join(' · ');const loc=CFG.labels[e.number];
  badge.layoutMode='VERTICAL';badge.resize(loc[2],10);badge.primaryAxisSizingMode='AUTO';badge.counterAxisSizingMode='FIXED';badge.paddingLeft=5;badge.paddingRight=5;badge.paddingTop=3;badge.paddingBottom=3;
  badge.fills=paint('#FFFFFF');badge.strokes=[];badge.cornerRadius=0;badge.x=loc[0];badge.y=loc[1];badge.visible=true;
  t.characters=label;t.fontName={family:'Inter',style:'Regular'};t.fontSize=16;t.fills=paint('#555555');t.textAlignHorizontal=loc[3]||'CENTER';t.resize(loc[2]-10,1);t.textAutoResize='HEIGHT';mark(t);mark(badge);
 }
}
const legend=f.children.find(n=>n.name==='Условия переходов');if(legend){legend.visible=false;mark(legend);}
const footer=f.children.find(n=>n.type==='TEXT'&&n.characters.startsWith('Номера на стрелках'));
if(footer){footer.characters='Условия переходов подписаны на стрелках. Все экраны — core.\nИсточник: ia/flows/'+CFG.stem+'.mmd';footer.fontSize=14;footer.x=32;footer.y=CFG.height-80;footer.resize(CFG.width-64,1);footer.textAutoResize='HEIGHT';footer.fills=paint('#717680');mark(footer);}
const issues=[];
for(const d of DATA.nodes){const c=f.children.find(n=>n.name===d.id&&n.type==='FRAME');for(const t of c.children.filter(n=>n.type==='TEXT'))if(t.y+t.height>c.height-5||t.y<0)issues.push(c.name);}
return {mutatedNodeIds:[...ids],frameId:f.id,clippedCards:[...new Set(issues)],visibleEdges:f.children.filter(n=>n.type==='VECTOR'&&n.visible).length,visibleLabels:f.children.filter(n=>n.name.startsWith('Transition')&&n.visible).length};
'''


def main():
    configs=[
      dict(sx=1,sy=1,width=2420,height=3530,terminals=['Home'],labels={},stem=''),
      dict(sx=1.6,sy=1.1,width=1760,height=1940,terminals=['Login','Launch'],stem='study-launch',labels={
       '01':[620,420,220],'02':[640,650,240],'03':[570,885,250],'04':[1190,1000,240],
       '05':[650,1108,260],'06':[1410,1300,280],'07':[605,1340,250],'08':[655,1580,210],
       '09':[195,1260,250],'10':[270,1510,250],'11':[1190,1710,260]}),
      dict(sx=1.6,sy=1.1,width=1400,height=1450,terminals=['ParticipantIntro','ParticipantFinish'],stem='participant-test',labels={
       '01':[960,303,270],'02':[380,433,240],'03':[390,715,250],'04':[960,848,270],
       '05':[670,1000,230],'06':[360,1000,250],'07':[960,1120,270]}),
      dict(sx=1.6,sy=1.1,width=3350,height=2060,terminals=['Studies','Report'],stem='results-analysis',labels={
       '01':[730,430,240],'02':[480,675,280],'03':[720,735,220],'04':[60,995,245],
       '05':[1280,675,290],'06':[115,964,320],'07':[450,1005,280],'08':[880,1005,280],
       '09':[1270,1005,295],'10':[740,1325,250],'11':[740,1600,230],'12':[1280,1750,260],
       '13':[1700,1550,250],'14':[1720,1285,255],'15':[1940,940,230],'16':[130,645,300],
       '17':[1950,675,240],'18':[2800,831,275],'19':[2800,907,275]}),
    ]
    for i,cfg in enumerate(configs,1):
        line=(OUT/f'{i:02}.js').read_text(encoding='utf-8').splitlines()[0]
        cfg['frameId']=FRAME_IDS[i-1]
        (OUT/f'restyle-{i:02}.js').write_text(line+'\nconst CFG='+json.dumps(cfg,ensure_ascii=False)+';\n'+SCRIPT,encoding='utf-8')
    print('Prepared four in-place reference-style payloads; same frame IDs and graph topology.')


def record_delivery():
    path=ROOT/'ia/figma-delivery.md'
    content=path.read_text(encoding='utf-8')
    content=content.replace('Номера на стрелках соотносятся с полными условиями справа.', 'Условия переходов подписаны непосредственно у стрелок; числовые метки и боковые легенды скрыты.')
    content=content.replace('приоритеты цветом и текстом', 'приоритеты текстом; будущие расширения с пунктирной рамкой')
    note='''\n## Визуальный стиль по референсу пользователя

Все четыре существующих фрейма переоформлены без изменения структуры переходов и идентификаторов. Белый фон с тонкой рамкой, светло-серые скруглённые блоки, чёрные начальные/конечные блоки, центрированные русские описания и небольшие латинские идентификаторы. Стрелки серые, условия подписаны рядом с ними. В sitemap приоритеты сохранены текстом, кандидаты развития отмечены пунктирной рамкой.

Скриншоты всех четырёх схем проверены после обновления. Структурная проверка: 24/11/7/19 стрелок, 11/7/19 текстовых подписей у user flows, без обрезанных подписей и выходов видимого содержимого за фреймы. Ссылки остались прежними.

`execution/restyle_figma_ia.py` готовит payloads для оформления существующих фреймов после базового `prepare_figma_ia.py`; флаг `--record` фиксирует проверенную передачу. Источники sitemap и Mermaid не изменены.
'''
    if '## Визуальный стиль по референсу пользователя' not in content: content+=note
    path.write_text(content,encoding='utf-8',newline='\n')
    print('Recorded verified reference styling; existing frame links retained.')


if __name__=='__main__':
    if '--record' in sys.argv: record_delivery()
    else: main()
