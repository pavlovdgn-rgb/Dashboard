"""Remove icon-instance backgrounds while retaining white playback glyphs."""
import argparse
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync(PAGE));
const changed=[],checks=[];
const buttons=figma.currentPage.findAll(n=>n.type==='INSTANCE'&&n.name==='play'&&n.findAllWithCriteria({types:['TEXT']}).some(t=>/^(Пауза|Воспроизвести)$/.test(t.characters)));
for(const b of buttons){
 for(const t of b.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 const icons=b.children.filter(n=>n.type==='INSTANCE'&&/^Icon/.test(n.name));
 for(const icon of icons){icon.fills=[];icon.strokes=[];changed.push(icon.id);}
 checks.push({button:b.id,icons:icons.map(n=>({id:n.id,backgroundCount:n.fills.length})),buttonFill:b.fills[0]?.boundVariables?.color?.id});
}
return {mutatedNodeIds:changed,checks};
'''
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('page',choices=['82:3','191:847']);args=p.parse_args()
    print(json.dumps({'code':CODE.replace('PAGE',json.dumps(args.page))},ensure_ascii=False))
