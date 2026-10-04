"""Replace static evidence button instances with text metadata in FindingDetails."""
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const created=[],changed=[],removed=[],results=[];
const reference=await figma.getNodeByIdAsync('210:19248');
for(const s of reference.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
for(const id of ['210:19204','210:19219','210:19234']) {
  const old=await figma.getNodeByIdAsync(id);
  if(!old)continue;
  const row=old.parent,source=old.findOne(n=>n.type==='TEXT');
  for(const s of source.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
  const match=source.characters.match(/^(\d+) · попытка (\d+) · (\d+:\d+)$/);
  if(!match)throw Error('Unexpected evidence label: '+source.characters);
  const meta=figma.createAutoLayout();meta.name='EvidenceMetadata / '+match[1];
  meta.layoutMode='VERTICAL';meta.fills=[];meta.strokes=[];
  meta.paddingTop=meta.paddingBottom=meta.paddingLeft=meta.paddingRight=0;
  meta.itemSpacing=0;meta.resize(old.width,44);
  row.insertChild(row.children.indexOf(old),meta);
  meta.layoutSizingHorizontal='FIXED';meta.layoutSizingVertical='HUG';
  const title=source.clone();meta.appendChild(title);title.name='Participant';title.characters='Участник '+match[1];
  title.textAutoResize='HEIGHT';title.layoutSizingHorizontal='FILL';
  const detail=reference.clone();meta.appendChild(detail);detail.name='Attempt and timestamp';
  detail.characters='Попытка '+match[2]+' · '+match[3];detail.textAutoResize='HEIGHT';detail.layoutSizingHorizontal='FILL';
  created.push(meta.id,title.id,detail.id);changed.push(row.id);
  removed.push(old.id);old.remove();
  row.layoutSizingVertical='HUG';row.counterAxisAlignItems='CENTER';
  results.push({row:row.id,metadata:meta.id,width:meta.width,height:meta.height,text:[title.characters,detail.characters],button:row.children.find(n=>n.type==='INSTANCE').id});
}
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,rows:results};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE}, ensure_ascii=False))
