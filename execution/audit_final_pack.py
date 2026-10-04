"""Read-only audit of every final screen; never marks visual review complete."""
import json
CODE=r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
figma.skipInvisibleInstanceChildren=false;
const roots=figma.currentPage.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Screen/'));
function visible(n,root){for(let p=n;p&&p!==root;p=p.parent)if(p.visible===false)return false;return true;}
const screens=[];
for(const root of roots){const issues=[];const nodes=root.findAll();
 for(const n of nodes){if(!visible(n,root))continue;
  if(n.type==='TEXT'&&!n.textStyleId)issues.push({kind:'textStyle',id:n.id,name:n.name});
  if(n.type==='INSTANCE'&&n.componentProperties.Type&&n.children.some(c=>c.name==='Control')&&n.children.some(c=>c.name==='Label')){
   const bottom=Math.max(...n.children.filter(c=>c.visible).map(c=>c.y+c.height));
   if(bottom>n.height+.5)issues.push({kind:'fieldHeight',id:n.id,name:n.name,height:n.height,contentBottom:bottom});
  }
  for(const field of ['fills','strokes'])if(field in n&&Array.isArray(n[field]))for(const p of n[field]){
   if(p.type==='SOLID'&&p.visible!==false&&p.opacity!==0&&!p.boundVariables?.color)issues.push({kind:'color',id:n.id,name:n.name,field});
   if(p.type.startsWith('GRADIENT')&&p.visible!==false&&p.gradientStops.some(s=>!s.boundVariables?.color))issues.push({kind:'gradient',id:n.id,name:n.name});
  }
  if(['TEXT','FRAME','INSTANCE'].includes(n.type)&&n.parent&&'width'in n.parent&&n.width>0&&(n.x< -1||n.x+n.width>n.parent.width+1))issues.push({kind:'width',id:n.id,name:n.name,x:n.x,w:n.width,parentW:n.parent.width,parent:n.parent.name});
 }
 screens.push({name:root.name.slice(7),id:root.id,width:root.width,height:root.height,nodeCount:nodes.length,issues});
}
return {pageId:figma.currentPage.id,screenCount:screens.length,screens,passed:screens.length===55&&screens.every(s=>!s.issues.length)};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
