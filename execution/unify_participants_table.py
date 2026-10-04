"""Give ParticipantsTable one continuous rounded grid, retaining row instances."""
import json
import sys
from grow_ui_kit import COMMON
CODE=COMMON+r'''
await figma.setCurrentPageAsync(page);
const root=await figma.getNodeByIdAsync('VARIANT');await fonts(root);root.primaryAxisSizingMode='AUTO';const mutated=[];
const header=root.findOne(n=>n.name==='TableHeader');
const body=root.findOne(n=>n.name==='ParticipantRows'||n.name==='StateMessage');
let surface=root.children.find(n=>n.name==='TableSurface');
if(!surface){surface=frame('TableSurface',null,'VERTICAL',header.width);root.insertChild(root.children.indexOf(header),surface);surface.appendChild(header);surface.appendChild(body);created.push(surface.id);}
surface.layoutSizingHorizontal='FILL';surface.setBoundVariable('itemSpacing',null);surface.itemSpacing=0;surface.paddingLeft=surface.paddingRight=surface.paddingTop=surface.paddingBottom=0;
fill(surface,'background/surface');surface.strokes=[paint('border/subtle')];surface.strokeWeight=1;surface.strokeAlign='INSIDE';surface.strokesIncludedInLayout=false;surface.clipsContent=true;
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])surface.setBoundVariable(k,radius);
header.layoutSizingHorizontal='FILL';body.layoutSizingHorizontal='FILL';fill(header,'background/sidebar');header.strokes=[paint('border/subtle')];header.strokeTopWeight=0;header.strokeLeftWeight=0;header.strokeRightWeight=0;header.strokeBottomWeight=1;header.strokesIncludedInLayout=false;
if(body.name==='ParticipantRows'){
 body.setBoundVariable('itemSpacing',null);body.itemSpacing=0;fill(body,'background/surface');
 for(const row of body.children){
  for(const k of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])row.setBoundVariable(k,null);row.cornerRadius=0;
  row.resize(row.width,80);row.layoutSizingHorizontal='FILL';row.layoutSizingVertical='FIXED';
  row.strokes=[paint('border/subtle')];row.strokeTopWeight=0;row.strokeLeftWeight=0;row.strokeRightWeight=0;row.strokeBottomWeight=1;row.strokesIncludedInLayout=false;mutated.push(row.id);
  const icon=row.findOne(n=>n.type==='INSTANCE'&&n.name==='Icon');if(icon){icon.fills=[];mutated.push(icon.id);}
 }
}else{body.setBoundVariable('paddingLeft',dimensions.base);body.setBoundVariable('paddingRight',dimensions.base);body.setBoundVariable('paddingTop',dimensions.base);body.setBoundVariable('paddingBottom',dimensions.base);}
mutated.push(root.id,surface.id,header.id,body.id);
return {createdNodeIds:created,mutatedNodeIds:mutated,tableVariantId:root.id,tableSurfaceId:surface.id};
'''
if __name__=='__main__':
    ids=['153:702','153:1081','153:1127','153:1170','153:1220']
    print(json.dumps({'code':CODE.replace('VARIANT',ids[int(sys.argv[1])])},ensure_ascii=False))
