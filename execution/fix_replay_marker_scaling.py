"""Scale timeline positions via anchors while preserving circle geometry."""
import json
import sys
CODE=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='82:3'));
const variant=await figma.getNodeByIdAsync('VARIANT');const created=[],mutated=[];
for(const t of variant.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
const track=variant.findOne(n=>n.name==='TimeTrackArea');
for(const marker of [...track.children].filter(n=>n.type==='ELLIPSE'||n.name==='PlayheadAt138')){
 const {x,y,width,height}=marker;const at=track.children.indexOf(marker);
 const anchor=figma.createFrame();anchor.name=marker.name+'Position';anchor.fills=[];anchor.clipsContent=false;anchor.resize(width,height);
 track.insertChild(at,anchor);anchor.layoutPositioning='ABSOLUTE';anchor.x=x;anchor.y=y;anchor.constraints={horizontal:'SCALE',vertical:'MIN'};
 anchor.appendChild(marker);marker.x=0;marker.y=0;marker.constraints={horizontal:'CENTER',vertical:'MIN'};
 created.push(anchor.id);mutated.push(marker.id);
}
for(const anchor of track.children.filter(n=>n.type==='FRAME'&&n.name.endsWith('Position'))){
 const marker=anchor.children[0];const time=marker.name==='PlayheadHandle'?138:Number(marker.name.match(/At(\d+)/)[1]);
 anchor.layoutPositioning='ABSOLUTE';anchor.resize(40,marker.height);anchor.x=track.width*time/272-20;anchor.y=marker.type==='ELLIPSE'?(marker.name==='PlayheadHandle'?-8:12):0;
 marker.x=(40-marker.width)/2;marker.y=0;marker.constraints={horizontal:'CENTER',vertical:'MIN'};anchor.constraints={horizontal:'SCALE',vertical:'MIN'};mutated.push(anchor.id,marker.id);
}
const labels=variant.findOne(n=>n.name==='TimeLabels');
for(const label of [...labels.children].filter(n=>n.type==='TEXT')){
 const time=Number(label.name.match(/Tick(\d+)/)[1]);label.resize(60,24);label.textAutoResize='NONE';
 if(time===0||time===272){label.constraints={horizontal:time===0?'MIN':'MAX',vertical:'MIN'};label.x=time===0?0:labels.width-60;label.textAlignHorizontal=time===0?'LEFT':'RIGHT';}
 else {const anchor=figma.createFrame();anchor.name=label.name+'Position';anchor.fills=[];anchor.clipsContent=false;anchor.resize(96,24);labels.insertChild(labels.children.indexOf(label),anchor);anchor.layoutPositioning='ABSOLUTE';anchor.x=labels.width*time/272-48;anchor.y=0;anchor.constraints={horizontal:'SCALE',vertical:'MIN'};anchor.appendChild(label);label.x=18;label.y=0;label.constraints={horizontal:'CENTER',vertical:'MIN'};label.textAlignHorizontal='CENTER';created.push(anchor.id);}
 mutated.push(label.id);
}
return {variantId:variant.id,createdNodeIds:created,mutatedNodeIds:[...new Set(mutated)]};
'''
if __name__=='__main__':
    ids=['84:642','84:678','118:98','118:168']
    print(json.dumps({'code':CODE.replace('VARIANT',ids[int(sys.argv[1])])}))
