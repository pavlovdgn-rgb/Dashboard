"""Prepare reproducible heatmap/replay visual overlays and small review corrections."""
from pathlib import Path
import json
from build_wireframes import RENDER,product,t,box,row,button

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.tmp/complete-wireframes'
HELPERS=RENDER[RENDER.index('await figma.loadFontAsync'):RENDER.index('const title=')]
PRE="const p=await figma.getNodeByIdAsync('20:2');await figma.setCurrentPageAsync(p);\n"
CODE=r'''
const f=p.findAllWithCriteria({types:['FRAME']}).find(n=>n.name===TARGET.name);
if(!f)throw new Error('Missing target '+TARGET.name);
const changed=[],removed=[];
for(const n of f.findAllWithCriteria({types:['TEXT']}))for(const s of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
function get(name){return f.findAllWithCriteria({types:['FRAME']}).find(n=>n.name===name);}
function svg(parent,name,markup,x=0,y=0){const n=figma.createNodeFromSvg(markup);parent.appendChild(n);n.name=name;n.layoutPositioning='ABSOLUTE';n.x=x;n.y=y;ids.push(n.id,...n.findAll(()=>true).map(c=>c.id));return n;}
if(TARGET.mode==='heat'||TARGET.mode==='first'||TARGET.mode==='dynamic'){
 const map=get('PrototypePlaceholder');if(map.children.some(n=>n.name==='HeatLayer'))throw new Error('Heat layer already present');
 if(TARGET.mode==='dynamic'){
  for(const c of [...map.children]){removed.push(c.id,...('children' in c?c.findAll(()=>true).map(n=>n.id):[]));c.remove();}
  for(const d of TARGET.base.children)make(map,d);
  const bg=track(figma.createRectangle());map.appendChild(bg);bg.name='PrototypeModalBackdrop';bg.layoutPositioning='ABSOLUTE';bg.resize(map.width,map.height);bg.x=bg.y=0;bg.fills=[{type:'SOLID',color:ink,opacity:0.35}];
  const modal=make(map,TARGET.modal);modal.layoutPositioning='ABSOLUTE';modal.fills=[{type:'SOLID',color:{r:1,g:1,b:1}}];modal.x=(map.width-modal.width)/2;modal.y=(map.height-modal.height)/2;
 }
 const texts=map.findAllWithCriteria({types:['TEXT']});
 const anchor=texts.find(n=>TARGET.mode==='dynamic'?n.characters==='M · выбран':n.characters==='Добавить в корзину');
 const a=anchor.parent;const ax=a.absoluteTransform[0][2]-map.absoluteTransform[0][2]+a.width*.55,ay=a.absoluteTransform[1][2]-map.absoluteTransform[1][2]+a.height*.5;
 const pts=TARGET.mode==='dynamic'?[[ax,ay,62],[ax-145,ay,40],[ax+155,ay,30]]:TARGET.mode==='first'?[[ax,ay,60],[155,190,55],[430,90,43],[ax-15,ay-66,36],[260,270,26],[720,200,24]]:[[ax,ay,78],[155,180,95],[445,100,85],[ax-20,ay-67,70],[230,280,58],[740,220,45]];
 const markup='<svg xmlns="http://www.w3.org/2000/svg" width="'+map.width+'" height="'+map.height+'" viewBox="0 0 '+map.width+' '+map.height+'"><defs><radialGradient id="heat"><stop offset="0" stop-color="#e33c26" stop-opacity="0.70"/><stop offset="0.36" stop-color="#ff8c22" stop-opacity="0.56"/><stop offset="0.72" stop-color="#ffda36" stop-opacity="0.30"/><stop offset="1" stop-color="#ffdf38" stop-opacity="0"/></radialGradient></defs>'+pts.map(([x,y,r])=>'<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="url(#heat)"/>').join('')+'<rect x="'+(a.absoluteTransform[0][2]-map.absoluteTransform[0][2]-4)+'" y="'+(a.absoluteTransform[1][2]-map.absoluteTransform[1][2]-4)+'" width="'+(a.width+8)+'" height="'+(a.height+8)+'" fill="none" stroke="#1a1a1a" stroke-dasharray="5 4"/></svg>';
 svg(map,'HeatLayer',markup);changed.push(map.id);
 const legend=get('MapPanel').children.find(n=>n.type==='TEXT'&&n.characters.includes('Меньше кликов'));
 if(legend){legend.characters='Меньше кликов → больше кликов · тёплые зоны интенсивнее · данные демонстрационные';changed.push(legend.id);}
 for(const tx of texts)if(tx.characters.includes('Слой тепловой карты')){tx.characters='Демонстрационное распределение кликов';changed.push(tx.id);}
}
if(TARGET.mode==='replay'||TARGET.mode==='incomplete'){
 const proto=get('PrototypePlaceholder');if(proto.children.some(n=>n.name==='ReplayCursor'))throw new Error('Replay cursor already present');
 const txtNode=proto.findAllWithCriteria({types:['TEXT']}).find(n=>n.characters==='Отправить заказ');const a=txtNode.parent;
 const x=a.absoluteTransform[0][2]-proto.absoluteTransform[0][2]+a.width*.7,y=a.absoluteTransform[1][2]-proto.absoluteTransform[1][2]+10;
 svg(proto,'ReplayCursor','<svg xmlns="http://www.w3.org/2000/svg" width="24" height="30" viewBox="0 0 24 30"><path d="M2 2 L2 24 L8 18 L13 28 L18 26 L13 16 L22 16 Z" fill="#1a1a1a" stroke="white" stroke-width="1.5"/></svg>',x,y);
 const trackNode=get('TimelineTrack');
 let markup='<svg xmlns="http://www.w3.org/2000/svg" width="1184" height="12" viewBox="0 0 1184 12"><rect width="600" height="12" fill="#1a1a1a" opacity="0.20"/>';
 for(const time of [48,96,126,138])markup+='<circle cx="'+(1184*time/272)+'" cy="6" r="4" fill="#1a1a1a"/>';
 if(TARGET.mode==='incomplete'){markup+='<rect x="435" width="109" height="12" fill="white" stroke="#1a1a1a"/>';for(let x=435;x<544;x+=12)markup+='<path d="M'+x+' 12 l12 -12" stroke="#1a1a1a"/>';const ep=get('EventsPanel');for(const n of [...ep.children])if(n.type==='TEXT'&&n.characters.startsWith('01:52')){removed.push(n.id);n.remove();}}
 markup+='<rect x="599" width="3" height="12" fill="#1a1a1a"/></svg>';
 svg(trackNode,'TimelineMarkers',markup);changed.push(trackNode.id);
}
if(TARGET.mode==='pdf'){
 const preview=get('PDFHeatmap');if(preview.children.some(n=>n.name==='MiniHeatmap'))throw new Error('PDF map present');
 const markup='<svg xmlns="http://www.w3.org/2000/svg" width="310" height="100" viewBox="0 0 310 100"><rect x="0" y="0" width="309" height="99" fill="white" stroke="#1a1a1a"/><rect x="12" y="12" width="85" height="76" fill="#e5e5e5"/><path d="M113 20 H275 M113 36 H200 M113 52 H230" stroke="#1a1a1a"/><rect x="112" y="65" width="150" height="23" fill="#e5e5e5" stroke="#1a1a1a"/><ellipse cx="174" cy="76" rx="40" ry="20" fill="#ffcf33" opacity="0.5"/><ellipse cx="174" cy="76" rx="24" ry="13" fill="#ed5b29" opacity="0.6"/><circle cx="54" cy="45" r="28" fill="#ffcf33" opacity="0.4"/></svg>';
 svg(preview,'MiniHeatmap',markup,preview.width-326,54);changed.push(preview.id);
}
const overflow=[];for(const n of [f,...f.findAllWithCriteria({types:['FRAME']})])for(const c of n.children)if(c.visible&&(c.x<0||c.y<0||c.x+c.width>n.width+1||c.y+c.height>n.height+1))overflow.push({parent:n.name,child:c.name,id:c.id});
return {frameId:f.id,createdNodeIds:ids,mutatedNodeIds:changed,removedNodeIds:removed,overflow};
'''
def main():
    modal=box('PrototypeSizeModal',640,[row('PrototypeModalHeader',592,[t('Выберите размер',528,25,True),t('×',40,22)],40,gap=24),t('Городской рюкзак',592,17),row('SizeOptions',592,[button('S',170),button('M · выбран',220),button('L',170)],48,gap=16),button('Подтвердить размер',592)],gap=16,pad=24,border=True)
    for name,mode in [('Heatmaps','heat'),('HeatmapsFirstClick','first'),('HeatmapsDynamicState','dynamic'),('Replay','replay'),('ReplayIncomplete','incomplete'),('Report','pdf'),('ReportReady','pdf')]:
        target=dict(name=name,mode=mode,base=product(1240,500),modal=modal)
        (OUT/f'detail-{name}.js').write_text(PRE+HELPERS+'const TARGET='+json.dumps(target,ensure_ascii=False)+';\n'+CODE,encoding='utf-8')
    print('Prepared 7 targeted visual detail scripts.')
if __name__=='__main__':main()
