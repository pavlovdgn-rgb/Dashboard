"""Read-only audit payload for the delivered ResultsOverview and its states."""
import json

CODE = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
figma.skipInvisibleInstanceChildren=false;
const root=await figma.getNodeByIdAsync('175:614');const nodes=[root,...root.findAll()];
const unbound=[],unstyled=[],overflow=[];
for(const n of nodes){
for(const k of ['fills','strokes'])if(k in n&&Array.isArray(n[k]))for(const p of n[k])if(p.type==='SOLID'&&p.visible!==false&&p.opacity!==0&&!p.boundVariables?.color)unbound.push({id:n.id,name:n.name,field:k});
if(n.type==='TEXT'&&!n.textStyleId)unstyled.push({id:n.id,name:n.name});
// Vector subpaths can have group-local transformed coordinates; assess layout boxes.
if(n!==root&&['TEXT','FRAME','INSTANCE','COMPONENT'].includes(n.type)&&n.visible!==false&&n.parent&&'width'in n.parent&&(n.x < -1||n.x+n.width>n.parent.width+1))overflow.push({id:n.id,name:n.name,x:n.x,w:n.width,parentW:n.parent.width});
}
const main=root.findOne(n=>n.name==='Main');const states=main.children.filter(n=>n.name.startsWith('State/')).map(s=>({id:s.id,name:s.name,visible:s.visible,width:s.width,height:s.height}));
const ratios=[];for(const state of main.children.filter(n=>['State/Ready','State/Selected'].includes(n.name))){for(const m of state.findAll(n=>n.type==='INSTANCE'&&n.name==='SuccessMetric')){const bar=m.findOne(n=>n.name==='RatioFill');const fraction=m.findOne(n=>n.name==='Fraction');const [a,b]=fraction.characters.split('/').map(Number);ratios.push({state:state.name,fraction:fraction.characters,width:bar.width,expected:200*a/b,passed:Math.abs(bar.width-200*a/b)<0.02});}}
const components=[];for(const id of ['171:1801','136:715']){const s=await figma.getNodeByIdAsync(id);components.push({id:s.id,name:s.name,type:s.type,variants:s.children.map(c=>({id:c.id,name:c.name,width:c.width,height:c.height})),properties:s.componentPropertyDefinitions});}
const vars=await figma.variables.getLocalVariablesAsync('COLOR');const vm=Object.fromEntries(vars.map(v=>[v.id,v]));function resolve(v){const c=Object.values(v.valuesByMode)[0];return c.type==='VARIABLE_ALIAS'?resolve(vm[c.id]):c;}function lum(c){return[c.r,c.g,c.b].map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);}function contrast(a,b){const x=lum(resolve(vars.find(v=>v.name===a))),y=lum(resolve(vars.find(v=>v.name===b)));return(Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
return {screenId:root.id,width:root.width,height:root.height,states,unbound,unstyled,horizontalOverflow:overflow,fonts:[...new Set(nodes.filter(n=>n.type==='TEXT').map(n=>n.fontName.family))],ratios,components,contrast:{active:contrast('accent/strong','accent/soft'),body:contrast('text/primary','background/surface'),secondary:contrast('text/secondary','background/surface')},effects:(await figma.getLocalEffectStylesAsync()).filter(s=>s.name==='shadow/card').map(s=>({id:s.id,name:s.name,effects:s.effects})),passed:root.width===1920&&root.height===1080&&!unbound.length&&!unstyled.length&&!overflow.length&&ratios.every(r=>r.passed)};
'''
if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
