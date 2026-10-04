"""Incremental Figma scripts for the approved interface-only participant flow."""
import argparse
import json

PRELUDE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
const created=[],changed=[],removed=[];
async function fonts(n){for(const t of n.findAllWithCriteria({types:['TEXT']}))for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);}
async function v(id){return await figma.variables.getVariableByIdAsync(id);}
function paint(variable){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:0,g:0,b:0}},'color',variable);}
async function text(parent,sourceId,name,value){const source=await figma.getNodeByIdAsync(sourceId);for(const s of source.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);const t=source.clone();parent.appendChild(t);t.name=name;t.characters=value;t.textAutoResize='HEIGHT';t.layoutSizingHorizontal='FILL';created.push(t.id);return t;}
async function button(parent,name,kind='Secondary'){const master=await figma.getNodeByIdAsync(kind==='Primary'?'125:312':kind==='Tertiary'?'125:326':'125:319');await fonts(master);const b=master.createInstance();parent.appendChild(b);b.name=name;const c=b.children.find(n=>n.name==='Control');c.setProperties({'Text#30956:4':name,'Icon left#30956:3':false,'Icon right#30956:5':false});b.resize(name.length>16?200:152,40);b.layoutSizingHorizontal='FIXED';created.push(b.id,...b.findAll().map(n=>n.id));return b;}
'''

STAGES = {}
STAGES['wrappers'] = r'''
const section=await figma.getNodeByIdAsync('175:613');
const bottom=Math.max(...section.children.map(n=>n.y+n.height));
const canvas=await v('VariableID:273:17939');
const frames=[];
for(const [name,width,height,x] of [['Screen/ParticipantInterfaceOnly',1920,1080,0],['Screen/ParticipantInterfaceOnlyMobile',390,844,2040]]){
 const f=figma.createAutoLayout();section.appendChild(f);f.name=name;f.layoutMode='VERTICAL';f.resize(width,height);f.layoutSizingHorizontal='FIXED';f.layoutSizingVertical='FIXED';f.x=x;f.y=bottom+120;f.fills=[paint(canvas)];f.paddingTop=f.paddingBottom=f.paddingLeft=f.paddingRight=0;f.itemSpacing=0;f.clipsContent=true;created.push(f.id);frames.push({id:f.id,name,width,height});
}
return {createdNodeIds:created,mutatedNodeIds:[section.id],frames};
'''

STAGES['launch'] = r'''
const root=await figma.getNodeByIdAsync('210:11108');await fonts(root);
const workspace=await figma.getNodeByIdAsync('210:11384'),left=await figma.getNodeByIdAsync('210:11385'),panel=await figma.getNodeByIdAsync('210:11409');
left.resize(560,left.height);left.layoutSizingHorizontal='FIXED';panel.layoutSizingHorizontal='FILL';workspace.layoutSizingVertical='HUG';
const keep=['210:11410','210:11411'];
for(const child of [...panel.children])if(!keep.includes(child.id)){removed.push(child.id,...('findAll'in child?child.findAll().map(n=>n.id):[]));child.remove();}
const small=await figma.variables.importVariableByKeyAsync('c6350febff91d7248df73477a27c5387155ac6c2');
const subtle=await v('VariableID:67:110'),border=await v('VariableID:67:111'),radius=await v('VariableID:202:3805');
const links=[];
for(const [mode,title,description,url,preview] of [
 ['guided','С панелью UX-Lab','Задание, выбор результата и переход к следующему шагу.','https://research.example.test/t/catalog-demo?view=guided','Посмотреть с панелью'],
 ['interface','Только интерфейс','Без панели, подсказок и вопросов UX-Lab. Сбор действий продолжается.','https://research.example.test/t/catalog-demo?view=interface','Посмотреть интерфейс']]){
 const card=figma.createAutoLayout();panel.appendChild(card);card.name='InvitationLink / '+mode;card.layoutMode='VERTICAL';card.layoutSizingHorizontal='FILL';card.layoutSizingVertical='HUG';card.fills=[];card.strokes=[paint(border)];card.strokeWeight=1;card.setBoundVariable('cornerRadius',radius);card.setBoundVariable('itemSpacing',small);for(const field of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])card.setBoundVariable(field,small);created.push(card.id);
 await text(card,'209:7205','LinkMode',title);await text(card,'209:7226','LinkDescription',description);
 const row=figma.createAutoLayout();card.appendChild(row);row.name='LinkCopy';row.layoutMode='HORIZONTAL';row.layoutSizingHorizontal='FILL';row.layoutSizingVertical='HUG';row.counterAxisAlignItems='CENTER';row.fills=[paint(subtle)];row.setBoundVariable('itemSpacing',small);for(const field of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])row.setBoundVariable(field,small);created.push(row.id);
 const urlText=await text(row,'210:11878','ParticipantURL',url);const codeStyle=await figma.importStyleByKeyAsync('0984a48b790120b9e37889f886315d9381507421');await figma.loadFontAsync(codeStyle.fontName);await urlText.setTextStyleIdAsync(codeStyle.id);
 const copy=await button(row,'Скопировать');
 const show=await button(card,preview,'Tertiary');show.resize(216,40);
 links.push({mode,card:card.id,url:urlText.id,copy:copy.id,preview:show.id});
}
await text(panel,'209:7226','CaptureNote','Обе ссылки относятся к этому исследованию. Участники входят без регистрации.');
await text(panel,'209:7226','AssessmentNote','Без панели задание выдайте заранее. Результат определяется по настроенным критериям; в свободном изучении оценка не нужна.');
panel.layoutSizingVertical='HUG';changed.push(panel.id,workspace.id,left.id);
return {createdNodeIds:created,mutatedNodeIds:changed,removedNodeIds:removed,links,panel:{width:panel.width,height:panel.height}};
'''

STAGES['before_launch'] = r'''
for(const [id,value] of [
 ['209:7230','После запуска появятся две ссылки: с панелью UX-Lab и только на интерфейс. Выберите подходящую для участников.'],
 ['209:7239','Два способа прохождения'],
 ['209:7240','С панелью UX-Lab · Только интерфейс'],
 ['210:11753','Сервис не подтвердил запуск исследования. Ссылки для участников пока не созданы.']]){
 const n=await figma.getNodeByIdAsync(id);for(const s of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);n.characters=value;changed.push(n.id);
}
const start=await figma.getNodeByIdAsync('209:7231');await fonts(start);start.name='Запустить исследование';start.children[0].setProperties({'Text#30956:4':'Запустить исследование'});changed.push(start.id,...start.findAll().map(n=>n.id));
return {mutatedNodeIds:changed};
'''

STAGES['clean_desktop'] = r'''
const wrapper=await figma.getNodeByIdAsync(WRAPPER);
const source=await figma.getNodeByIdAsync('210:11825');await fonts(source);
const content=source.clone();wrapper.appendChild(content);content.name='NOVA / Product interface';
content.resize(1440,content.height);content.layoutSizingHorizontal='FIXED';content.layoutSizingVertical='HUG';
wrapper.counterAxisAlignItems='CENTER';wrapper.paddingTop=64;
const preview=content.children.find(n=>n.name==='ProductPreview');preview.layoutSizingHorizontal='FILL';preview.layoutSizingVertical='HUG';
const photo=preview.children.find(n=>n.name==='ProductImage');photo.resize(480,480);photo.layoutSizingHorizontal='FIXED';photo.layoutSizingVertical='FIXED';
const details=preview.children.find(n=>n.name==='ProductDetails');details.layoutSizingHorizontal='FILL';
created.push(content.id,...content.findAll().map(n=>n.id));changed.push(wrapper.id);
return {createdNodeIds:created,mutatedNodeIds:changed,frame:wrapper.id,content:content.id};
'''

STAGES['clean_mobile'] = r'''
const wrapper=await figma.getNodeByIdAsync(WRAPPER);
const source=await figma.getNodeByIdAsync('210:17114');await fonts(source);
const content=source.clone();wrapper.appendChild(content);content.name='NOVA / Product interface';content.resize(390,content.height);content.layoutSizingHorizontal='FILL';content.layoutSizingVertical='HUG';
created.push(content.id,...content.findAll().map(n=>n.id));changed.push(wrapper.id);
return {createdNodeIds:created,mutatedNodeIds:changed,frame:wrapper.id};
'''

STAGES['integrate'] = r'''
const note=await figma.getNodeByIdAsync('334:10397');removed.push(note.id);note.remove();
const mobilePhoto=await figma.getNodeByIdAsync('334:10414'),photo=await figma.getNodeByIdAsync('210:11828');
mobilePhoto.fills=photo.fills;for(const child of mobilePhoto.children){child.visible=false;changed.push(child.id);}changed.push(mobilePhoto.id);
for(const [id,destination] of [['333:10391','210:11819'],['333:10414','333:10373'],['209:7231','210:11108']]){
 const n=await figma.getNodeByIdAsync(id);await n.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',destinationId:destination,navigation:'NAVIGATE',transition:null}]}]);changed.push(n.id);
}
const source=await figma.getNodeByIdAsync('210:12490');await fonts(source);
const details=source.clone();const section=await figma.getNodeByIdAsync('175:613');section.appendChild(details);details.name='Screen/ParticipantDetailsInterfaceOnly';details.x=2550;details.y=(await figma.getNodeByIdAsync('333:10373')).y;
for(const t of details.findAllWithCriteria({types:['TEXT']})){
 if(t.characters==='Участник 014')t.characters='Участник 021';
 if(t.characters==='Участники / 014')t.characters='Участники / 021';
 if(t.characters==='Цель не достигнута')t.characters='Нет оценки';
 if(t.characters==='Наблюдение завершено. Запись 04:32 доступна; 4 сигнала затруднений требуют просмотра контекста.')t.characters='Критерий оформления не зафиксирован. Самооценка не запрашивалась; отсутствие события не означает отказ участника.';
}
const main=details.findOne(n=>n.type==='FRAME'&&n.name==='Main');
const meta=await text(main,'209:7226','ParticipationMode','Тип ссылки: Только интерфейс · Задания выданы заранее · Результаты определены по событиям');main.insertChild(1,meta);
const withPanel=await figma.getNodeByIdAsync('210:12751');const guidedMeta=await text(withPanel,'209:7226','ParticipationMode','Тип ссылки: С панелью UX-Lab · Задания и выбор результата показаны участнику');withPanel.insertChild(1,guidedMeta);changed.push(withPanel.id);
created.push(details.id,...details.findAll().map(n=>n.id));
return {createdNodeIds:[...new Set(created)],mutatedNodeIds:changed,removedNodeIds:removed,details:details.id,previewTargets:['210:11819','333:10373']};
'''

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=STAGES);parser.add_argument('--wrapper')
    args=parser.parse_args()
    if args.stage.startswith('clean_') and not args.wrapper:parser.error('--wrapper is required')
    print(json.dumps({'code':PRELUDE+STAGES[args.stage].replace('WRAPPER',json.dumps(args.wrapper))},ensure_ascii=False))
