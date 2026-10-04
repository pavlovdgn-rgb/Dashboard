"""Use contextual text actions on tinted DataCoverage surfaces."""
import argparse
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(PAGE));
const changed=[],checks=[];
const roots=PAGE==='82:3'?[await figma.getNodeByIdAsync('86:331'),await figma.getNodeByIdAsync('86:344')]:figma.currentPage.findAll(n=>n.type==='INSTANCE'&&['86:331','86:344'].includes(n.mainComponent?.id));
for(const root of roots){
 for(const t of root.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const header=root.children.find(n=>n.name==='StatusHeader');const title=header.findOne(n=>n.type==='TEXT');
 const token=await figma.variables.getVariableByIdAsync(title.fills[0].boundVariables.color.id);
 const action=root.children.find(n=>n.name==='OptionalAction');const button=action.children.find(n=>n.type==='INSTANCE');
 button.setProperties({'Style':'Empty','Icon right#30956:5':true,'⮑  Icon right#31056:0':'95:6'});
 button.fills=[];button.strokes=[];button.paddingLeft=0;button.paddingRight=0;button.layoutSizingHorizontal='HUG';
 for(const n of button.findAll()){
  if(['FRAME','INSTANCE'].includes(n.type)){n.fills=[];n.strokes=[];}
  if(['TEXT','VECTOR','BOOLEAN_OPERATION','ELLIPSE','RECTANGLE'].includes(n.type))for(const f of ['fills','strokes'])if(Array.isArray(n[f])&&n[f].length)n[f]=n[f].map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',token):p);
  if(n.type==='TEXT')n.textDecoration='UNDERLINE';
 }
 changed.push(button.id,...button.findAll().map(n=>n.id));checks.push({card:root.id,button:button.id,fillCount:button.fills.length,style:button.componentProperties.Style.value,color:token.id,width:button.width,height:button.height});
}
return {mutatedNodeIds:changed,checks};
'''
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('page',choices=['82:3','191:847']);a=p.parse_args()
    print(json.dumps({'code':CODE.replace('PAGE',json.dumps(a.page))},ensure_ascii=False))
