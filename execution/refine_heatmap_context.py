"""Group heatmap scope and sample into a compact, token-bound context panel."""
import argparse
import json

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const created=[],changed=[],removed=[];
const vars={};for(const [key,id] of Object.entries({surface:'67:108',border:'67:111',text:'67:113',muted:'67:114',accent:'67:118',radius:'202:3805'}))vars[key]=await figma.variables.getVariableByIdAsync('VariableID:'+id);
const tokens={};for(const [key,id] of Object.entries({xs:'33cf8d6af437f589eec375f0dba78baab2864cf9',base:'723a30bab117da7a71b48251ea5a84eb3614f264',lg:'e34de5efd30aef81f5d652fe45dc113b59cc6e1a'}))tokens[key]=await figma.variables.importVariableByKeyAsync(id);
const styles={};for(const [key,id] of Object.entries({medium:'f9812c3b501de2fc60a2086c9d855d94e3bd1950',small:'0ffe9932b31ce3305d4041a590cc8ec20d95f4d2'})){styles[key]=await figma.importStyleByKeyAsync(id);await figma.loadFontAsync(styles[key].fontName);}
function paint(k){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',vars[k]);}
async function fonts(root){for(const t of root.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
function frame(parent,name,direction='VERTICAL'){const n=figma.createAutoLayout(direction);parent.appendChild(n);n.name=name;n.fills=[];n.layoutSizingHorizontal='FILL';n.layoutSizingVertical='HUG';n.setBoundVariable('itemSpacing',tokens.xs);created.push(n.id);return n;}
async function text(parent,name,value,style='small',color='muted'){const n=figma.createText();parent.appendChild(n);n.name=name;await n.setTextStyleIdAsync(styles[style].id);n.characters=value;n.fills=[paint(color)];n.textAutoResize='HEIGHT';n.layoutSizingHorizontal='FILL';created.push(n.id);return n;}
const result=[];
for(const id of TARGETS){
 const screen=await figma.getNodeByIdAsync(id);const main=screen.findOne(n=>n.type==='FRAME'&&n.name==='Main');
 if(main.children.some(n=>n.name==='HeatmapOverview')){result.push({id,skipped:true});continue;}
 const context=main.children.find(n=>n.name==='HeatmapContext'),summary=main.children.find(n=>n.name==='DataSummary');
 if(!context||!summary)throw Error('Missing context/summary: '+id);
 await fonts(main);
 const values=context.findAllWithCriteria({types:['TEXT']}).map(n=>n.characters);
 const counts=summary.findAllWithCriteria({types:['TEXT']}).map(n=>n.characters);
 const pick=prefix=>{const v=values.find(v=>v.startsWith(prefix));if(!v)throw Error('Missing '+prefix);return v;};
 const card=frame(main,'HeatmapOverview','HORIZONTAL');main.insertChild(main.children.indexOf(context),card);
 card.fills=[paint('surface')];card.strokes=[paint('border')];card.strokeWeight=1;card.strokeAlign='INSIDE';card.setBoundVariable('itemSpacing',tokens.lg);
 for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])card.setBoundVariable(p,tokens.base);
 for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])card.setBoundVariable(p,vars.radius);
 const scope=frame(card,'ShownContext');
 await text(scope,'Page',pick('Страница:'),'medium','text');
 await text(scope,'Scenario',pick('Сценарий:'));
 const meta=[pick('Состояние:'),pick('Устройство:').replace('Устройство: ','').replace('компьютер','Компьютер'),pick('Окно:').replace('Окно: ',''),pick('Снимок:')].join(' · ');
 await text(scope,'SnapshotParameters',meta);
 const sample=frame(card,'SampleSummary');sample.resize(448,80);sample.layoutSizingHorizontal='FIXED';sample.layoutSizingVertical='HUG';
 sample.strokes=[paint('border')];sample.strokeWeight=1;sample.strokeTopWeight=0;sample.strokeRightWeight=0;sample.strokeBottomWeight=0;sample.strokeLeftWeight=1;sample.setBoundVariable('paddingLeft',tokens.lg);
 await text(sample,'SampleCounts',counts[0],'medium','text');
 await text(sample,'SampleNotes',counts[1]);
 const method=await text(sample,'CalculationLink',counts[2],'small','accent');method.textDecoration='UNDERLINE';
 const heading=main.children.find(n=>n.name==='PageHeading');const back=heading.findOne(n=>n.type==='TEXT'&&n.characters.startsWith('К обзору результатов'));
 if(back){back.characters='К обзору результатов';back.fills=[paint('accent')];changed.push(back.id);}
 removed.push(context.id,...context.findAll().map(n=>n.id),summary.id,...summary.findAll().map(n=>n.id));context.remove();summary.remove();changed.push(main.id);
 result.push({id,panel:card.id,width:card.width,height:card.height,contentBottom:main.y+Math.max(...main.children.map(n=>n.y+n.height)),screenHeight:screen.height});
}
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,screens:result};
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', default=['205:6345','210:14240','210:14633'])
    args = parser.parse_args()
    print(json.dumps({'code': CODE.replace('TARGETS', json.dumps(args.ids))}, ensure_ascii=False))
