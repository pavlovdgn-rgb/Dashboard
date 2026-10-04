"""Remove latent text and pin icon-only geometry on master and final instances."""
import argparse
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(PAGE));
const changed=[],checks=[];
for(const p of figma.currentPage.findAll(n=>n.type==='FRAME'&&n.name==='CompactPagination')){
 for(const b of p.children.filter(n=>n.type==='INSTANCE')){
  for(const t of b.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
  const c=b.children.find(n=>n.type==='INSTANCE'&&n.name==='Control');
  if(!c)throw Error('Missing control '+b.id);
  const icon=b.name==='Предыдущая страница'?'95:4':b.name==='Следующая страница'?'95:6':null;
  if(!icon)throw Error('Unexpected pager action '+b.name);
  c.setProperties({'Icon only':'True','Text#30956:4':'','Icon left#30956:3':false,'Icon right#30956:5':false,'⮑  Icon#31150:0':icon});
  b.resize(40,40);b.layoutSizingHorizontal='FIXED';b.layoutSizingVertical='FIXED';
  c.resize(32,32);c.layoutSizingHorizontal='FILL';c.layoutSizingVertical='FIXED';
  changed.push(b.id,c.id,...c.findAll().map(n=>n.id));
 }
 checks.push({id:p.id,width:p.width,height:p.height,buttons:p.children.filter(n=>n.type==='INSTANCE').map(b=>({id:b.id,width:b.width,controlWidth:b.children[0].width,text:b.children[0].componentProperties['Text#30956:4'].value,iconOnly:b.children[0].componentProperties['Icon only'].value}))});
}
return {mutatedNodeIds:[...new Set(changed)],checks};
'''
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('page',choices=['82:3','191:847'])
    args=parser.parse_args()
    print(json.dumps({'code':CODE.replace('PAGE',json.dumps(args.page))},ensure_ascii=False))
