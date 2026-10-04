"""Read-only evidence collector for all six screens_audit checks.

Only local intermediate evidence is written. Generated Figma code never mutates nodes.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.tmp/screens-audit-2026-09-23'

FOUNDATION=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
const sets=figma.currentPage.findAll(n=>n.type==='COMPONENT_SET').slice(OFFSET,OFFSET+LIMIT);
return {sections:figma.currentPage.findAll(n=>n.type==='SECTION').map(n=>({id:n.id,name:n.name})),sets:sets.map(s=>({id:s.id,name:s.name,variants:s.children.map(c=>({id:c.id,name:c.name,w:c.width,h:c.height,props:c.variantProperties,types:c.children.map(n=>n.type),fill:c.fills.filter(p=>p.type==='SOLID').map(p=>({color:p.color,variable:p.boundVariables?.color?.id})),texts:c.findAllWithCriteria({types:['TEXT']}).length}))})),effectStyles:(await figma.getLocalEffectStylesAsync()).map(s=>({id:s.id,name:s.name,effects:s.effects}))};
'''

VARIABLES=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('82:3'));
return {collections:(await figma.variables.getLocalVariableCollectionsAsync()).map(c=>({id:c.id,name:c.name,modes:c.modes})),variables:(await figma.variables.getLocalVariablesAsync()).map(v=>({id:v.id,name:v.name,type:v.resolvedType,collection:v.variableCollectionId,values:v.valuesByMode}))};
'''

SCAN=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
figma.skipInvisibleInstanceChildren=false;
const section=await figma.getNodeByIdAsync('175:613');
const all=section.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Screen/'));
const sets=SET_IDS;const refs=REFERENCE_VARIANTS;
const external=new Set(['205:6763','209:6649','210:11825','210:14538','210:14931','210:15318','210:17114','210:19541','210:20078']);
function visible(n,root){for(let p=n;p&&p!==root;p=p.parent)if(p.visible===false)return false;return true;}
function inExternal(n,root){for(let p=n;p&&p!==root;p=p.parent)if(external.has(p.id))return true;return false;}
function inInstance(n,root){for(let p=n.parent;p&&p!==root;p=p.parent)if(p.type==='INSTANCE')return true;return false;}
function path(n,root){let p=n,a=[];while(p&&p!==root){a.push(p.name);p=p.parent;}return a.reverse().join('/');}
function near(a,b){return ['r','g','b'].every(k=>Math.abs(a[k]-b[k])<=5/255);}
const screens=[];
for(const root of all.slice(OFFSET,OFFSET+LIMIT)){
 const nodes=root.findAll(),usage={},colors=[],geometry=[],candidates=[],hidden=[],effects={},blocks=[],textStyles=[];
 const rb=root.absoluteBoundingBox;
 for(const n of nodes){const vis=visible(n,root),ext=inExternal(n,root);
  if(n.type==='INSTANCE'){
   const m=n.mainComponent;const owner=m?.parent?.type==='COMPONENT_SET'?m.parent.id:m?.id;
   if(sets.includes(owner)){const k=owner;usage[k]??={count:0,visible:0,variants:{},examples:[]};const u=usage[k];u.count++;if(vis)u.visible++;u.variants[m.id]??={all:0,visible:0};u.variants[m.id].all++;if(vis)u.variants[m.id].visible++;if(u.examples.length<3)u.examples.push(n.id);}
  }
  if(n.visible===false&&!inInstance(n,root))hidden.push({id:n.id,name:n.name,parent:n.parent.name});
  for(const field of ['fills','strokes'])if(field in n&&Array.isArray(n[field]))for(const [index,p] of n[field].entries()){
   if(p.visible===false||p.opacity===0)continue;
   if(p.type==='SOLID'&&!p.boundVariables?.color)colors.push({id:n.id,name:n.name,field,index,color:p.color,visible:vis,external:ext,style:field==='fills'?n.fillStyleId:n.strokeStyleId});
   if(p.type.startsWith('GRADIENT'))for(const [stop,s] of p.gradientStops.entries())if(!s.boundVariables?.color)colors.push({id:n.id,name:n.name,field,index,stop,color:s.color,visible:vis,external:ext});
  }
  if('effects'in n&&Array.isArray(n.effects))for(const e of n.effects){if(e.visible===false||!('color'in e))continue;if(!e.boundVariables?.color&&!n.effectStyleId){const key=JSON.stringify(e);effects[key]??={effect:e,count:0,visible:0,examples:[]};const issue=effects[key];issue.count++;if(vis)issue.visible++;if(issue.examples.length<5)issue.examples.push({id:n.id,name:n.name,external:ext});}}
  if(!vis)continue;
  if(n.type==='TEXT'&&!n.textStyleId)textStyles.push({id:n.id,name:n.name,text:n.characters.slice(0,90),external:ext});
  if(['TEXT','FRAME','INSTANCE'].includes(n.type)&&n.rotation===0&&n.parent&&'height'in n.parent){
   const ox=Math.max(0,-n.x,n.x+n.width-n.parent.width),oy=Math.max(0,-n.y,n.y+n.height-n.parent.height);
   if(ox>1||oy>1)geometry.push({id:n.id,name:n.name,path:path(n,root),x:n.x,y:n.y,w:n.width,h:n.height,parent:n.parent.id,parentName:n.parent.name,pw:n.parent.width,ph:n.parent.height,ox,oy,clip:n.parent.clipsContent,scroll:n.parent.overflowDirection,external:ext,nestedInstance:inInstance(n,root)});
  }
  if(['FRAME','GROUP','RECTANGLE'].includes(n.type)&&!inInstance(n,root)&&!ext&&'children'in n&&n.children.length){
   const paints=Array.isArray(n.fills)?n.fills.filter(p=>p.type==='SOLID'&&p.visible!==false):[];
   const matches=refs.filter(r=>Math.abs(r.w-n.width)<=10&&Math.abs(r.h-n.height)<=10&&r.fill.some(f=>paints.some(p=>near(f.color,p.color))));
   if(matches.length)candidates.push({id:n.id,name:n.name,path:path(n,root),w:n.width,h:n.height,types:n.children.map(c=>c.type),text:n.findAllWithCriteria({types:['TEXT']}).map(t=>t.characters).join(' | ').slice(0,220),matches:matches.map(r=>({id:r.id,set:r.set,name:r.name}))});
  }
 }
 const main=root.findOne(n=>n.type==='FRAME'&&n.name==='Main');
 for(const n of (main?.children??root.children))blocks.push({id:n.id,name:n.name,type:n.type,visible:n.visible,x:n.x,y:n.y,w:n.width,h:n.height,scroll:'overflowDirection'in n?n.overflowDirection:null,clip:'clipsContent'in n?n.clipsContent:null,children:'children'in n?n.children.map(c=>({id:c.id,name:c.name,type:c.type,visible:c.visible})):[],text:'findAllWithCriteria'in n?n.findAllWithCriteria({types:['TEXT']}).filter(t=>visible(t,root)).map(t=>t.characters).filter(t=>/ошиб|пуст|загруз|сохран|обнов|доступ|истек|истёк|отправ|данных|провер|длин|вход/i.test(t)).slice(0,24):[]});
 screens.push({id:root.id,name:root.name,width:root.width,height:root.height,clip:root.clipsContent,scroll:root.overflowDirection,nodeCount:nodes.length,visibleCount:nodes.filter(n=>visible(n,root)).length,usage,colors,effects:Object.values(effects),geometry,candidates,hidden,textStyles,blocks});
}
return {section:section.id,total:all.length,offset:OFFSET,screens};
'''

def inputs():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=[ROOT/'ds/components.md',ROOT/'ds/foundation.md',ROOT/'ds/scan-status.json',*sorted((ROOT/'ds/screens').glob('*'))]
    files=[];paragraphs={};screens=[]
    for p in paths:
        if not p.is_file():continue
        text=p.read_text(encoding='utf-8-sig');files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(text.encode()).hexdigest()})
        if p.suffix=='.json':json.loads(text)
        if p.suffix=='.md' and p.parent.name=='screens' and not p.name.startswith('_'):
            screens.append({'path':str(p.relative_to(ROOT)),'name':text.splitlines()[0],'text':text})
            for par in text.split('\n\n'):
                if any(w in par.lower() for w in ['состояни','композици','фактически использ','ошибк','загруз','переполн','доступ','отлож','edge']):paragraphs.setdefault(par,[]).append(p.stem)
    idx=json.loads((ROOT/'ds/index.json').read_text(encoding='utf-8-sig'))
    result={'files':files,'screens':screens,'catalog':idx.get('productExtensions',{}),'uniqueRelevantParagraphs':[{'text':p,'files':v} for p,v in paragraphs.items()]}
    (OUT/'inputs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'filesRead':len(files),'screenSpecs':len(screens),'uniqueRelevantParagraphs':result['uniqueRelevantParagraphs']},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['inputs','foundation','variables','scan']);p.add_argument('--offset',type=int,default=0);p.add_argument('--limit',type=int,default=10);a=p.parse_args()
    if a.stage=='inputs':inputs()
    else:
        code={'foundation':FOUNDATION,'variables':VARIABLES,'scan':SCAN}[a.stage]
        if a.stage=='scan':
            f=json.loads((OUT/'foundation.json').read_text(encoding='utf-8'))
            refs=[dict(id=v['id'],name=v['name'],w=v['w'],h=v['h'],fill=v['fill'],set=s['name']) for s in f['sets'] for v in s['variants'] if v['fill']]
            code=code.replace('SET_IDS',json.dumps([s['id'] for s in f['sets']])).replace('REFERENCE_VARIANTS',json.dumps(refs)).replace('OFFSET',str(a.offset)).replace('LIMIT',str(a.limit))
        code=code.replace('OFFSET',str(a.offset)).replace('LIMIT',str(a.limit))
        print(json.dumps({'code':code},ensure_ascii=False))
