"""Compose visible installation code with adjacent copy action from existing kit."""
import json

CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
figma.skipInvisibleInstanceChildren=false;
const created=[],changed=[],removed=[];
const vars={};for(const [k,id] of Object.entries({surface:'67:108',subtle:'67:109',border:'67:111',text:'67:113',muted:'67:114',radius:'202:3805'}))vars[k]=await figma.variables.getVariableByIdAsync('VariableID:'+id);
const pad=await figma.variables.importVariableByKeyAsync('723a30bab117da7a71b48251ea5a84eb3614f264');
const gap=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');
function paint(k){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',vars[k]);}
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
const titleSource=await figma.importStyleByKeyAsync('f9812c3b501de2fc60a2086c9d855d94e3bd1950'),hintSource=await figma.importStyleByKeyAsync('0ffe9932b31ce3305d4041a590cc8ec20d95f4d2');
await figma.loadFontAsync(titleSource.fontName);await figma.loadFontAsync(hintSource.fontName);
const titleStyle=titleSource.id,hintStyle=hintSource.id;
const primary=await figma.getNodeByIdAsync('125:312');await fonts(primary);
const codeMaster=await figma.getNodeByIdAsync('276:10375');await fonts(codeMaster);
const mono=codeMaster.findOne(n=>n.type==='TEXT'&&n.name==='Code').textStyleId;
async function label(parent,name,text,style,color='text'){const t=figma.createText();parent.appendChild(t);t.name=name;await figma.loadFontAsync({family:'Inter',style:'Regular'});await t.setTextStyleIdAsync(style);t.characters=text;t.fills=[paint(color)];t.textAutoResize='HEIGHT';t.layoutSizingHorizontal='FILL';created.push(t.id);return t;}
function frame(parent,name,direction='VERTICAL'){const n=figma.createAutoLayout(direction);parent.appendChild(n);n.name=name;n.fills=[];n.layoutSizingHorizontal='FILL';n.setBoundVariable('itemSpacing',gap);created.push(n.id);return n;}
for(const [panelId,copyId,checkId] of [['205:5794','205:5801','205:5808'],['210:10706','210:10712','210:10719']]){
 const panel=await figma.getNodeByIdAsync(panelId);if(panel.children.some(n=>n.name==='CodeCopyBlock'))continue;
 await fonts(panel);const copy=await figma.getNodeByIdAsync(copyId);
 const prior=panel.children.find(n=>n.name==='CodePlaceholder');const position=prior?panel.children.indexOf(prior):panel.children.indexOf(copy);
 const card=frame(panel,'CodeCopyBlock');panel.insertChild(position,card);card.fills=[paint('subtle')];
 for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])card.setBoundVariable(p,pad);
 for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])card.setBoundVariable(p,vars.radius);
 const header=frame(card,'CodeCopyHeader','HORIZONTAL');header.counterAxisAlignItems='CENTER';
 await label(header,'Title','Код подключения',titleStyle);
 header.appendChild(copy);copy.resize(152,40);copy.layoutSizingHorizontal='FIXED';changed.push(copy.id);
 const ct=copy.findOne(n=>n.type==='TEXT'&&n.visible);ct.characters='Скопировать код';changed.push(ct.id);
 const code=codeMaster.createInstance();card.appendChild(code);created.push(code.id);code.name='CodeBlock/Installation';await fonts(code);
 const props={};for(const key of Object.keys(code.componentProperties))if(/lineNumbers|overflowHeight|isCopiable|scrollbar/.test(key))props[key]=false;else if(/transparentBackground/.test(key))props[key]=true;code.setProperties(props);
 code.resize(card.width-32,88);code.layoutSizingHorizontal='FILL';code.layoutSizingVertical='FIXED';
 for(const n of [code,...code.findAll()]){if(n.type==='TEXT'){n.fills=[paint('text')];}else if('fills'in n)n.fills=[];if('strokes'in n)n.strokes=[];}
 const text=code.findOne(n=>n.type==='TEXT'&&n.name==='Code');text.characters='<script defer\n  src="https://research.example.test/sdk.js"\n  data-study="catalog-demo"></script>';text.textAutoResize='HEIGHT';text.layoutSizingHorizontal='FILL';
 created.push(...code.findAll().map(n=>n.id));
 await label(card,'DemoNote','Пример для макета. Рабочий код выдаст сервис.',hintStyle,'muted');
 if(prior){removed.push(prior.id);prior.remove();}
 const check=await figma.getNodeByIdAsync(checkId);check.swapComponent(primary);changed.push(check.id,...check.findAll().map(n=>n.id));
}
const field=await figma.getNodeByIdAsync('210:11412');const button=await figma.getNodeByIdAsync('210:11428');const panel=await figma.getNodeByIdAsync('210:11409');
if(!panel.children.some(n=>n.name==='ParticipantLinkCopy')){
 await fonts(panel);const row=frame(panel,'ParticipantLinkCopy','HORIZONTAL');panel.insertChild(panel.children.indexOf(field),row);row.counterAxisAlignItems='CENTER';row.fills=[paint('subtle')];for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])row.setBoundVariable(p,gap);
 for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])row.setBoundVariable(p,vars.radius);
 const url=field.findOne(n=>n.type==='TEXT'&&n.name==='InputValue').characters;
 const text=await label(row,'ParticipantURL',url,mono);text.textAutoResize='HEIGHT';
 row.appendChild(button);button.resize(144,40);button.layoutSizingHorizontal='FIXED';button.findOne(n=>n.type==='TEXT'&&n.visible).characters='Скопировать';changed.push(button.id,...button.findAll().map(n=>n.id));
 removed.push(field.id);field.remove();
}
const group=await figma.getNodeByIdAsync('216:10171');
if(!group.parent.children.some(n=>n.name==='ReportSelectionHint')){const t=await label(group.parent,'ReportSelectionHint','Выберите, что включить в отчёт',hintStyle,'muted');group.parent.insertChild(group.parent.children.indexOf(group),t);}
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,codePanels:['205:5794','210:10706'],linkPanel:panel.id};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
