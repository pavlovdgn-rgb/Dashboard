"""Remove inherited button width restriction; bind dormant local nav icon paints."""
import json
CODE=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='82:3'));
figma.skipInvisibleInstanceChildren=false;const ids=[];
const buttons=await figma.getNodeByIdAsync('125:450');
for(const c of buttons.children){for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);const ctl=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');ctl.setBoundVariable('minWidth',null);ctl.minWidth=null;ctl.layoutSizingHorizontal='FILL';ids.push(ctl.id);}
const nav=await figma.getNodeByIdAsync('128:563');
const vars=await figma.variables.getLocalVariablesAsync('COLOR');
for(const c of nav.children){for(const t of c.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);const color=vars.find(v=>v.name===(c.variantProperties.Selected==='True'?'accent/strong':'text/secondary'));for(const n of c.findAll()){for(const k of ['fills','strokes'])if(k in n&&Array.isArray(n[k])&&n[k].some(p=>p.type==='SOLID'&&!p.boundVariables?.color)){n[k]=n[k].map(p=>p.type==='SOLID'&&!p.boundVariables?.color?figma.variables.setBoundVariableForPaint(p,'color',color):p);ids.push(n.id);}}}
return {mutatedNodeIds:[...new Set(ids)]};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
